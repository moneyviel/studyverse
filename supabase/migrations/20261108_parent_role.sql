-- Parent accounts: a role on the profile, codes made on the CHILD's phone, and email invites from the parent
alter table studyverse.profiles add column if not exists role text check (role in ('student', 'parent'));

create or replace function studyverse.set_my_role(p_role text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); cur text;
begin
  if uid is null or p_role not in ('student', 'parent') then return jsonb_build_object('ok', false); end if;
  select role into cur from studyverse.profiles where user_id = uid;
  if cur is not null and cur <> p_role then return jsonb_build_object('ok', false, 'role', cur, 'msg', 'This account is already set up as a ' || cur || '.'); end if;
  insert into studyverse.profiles(user_id, role) values (uid, p_role) on conflict (user_id) do update set role = excluded.role;
  return jsonb_build_object('ok', true, 'role', p_role);
end $$;
revoke all on function studyverse.set_my_role(text) from public, anon;
grant execute on function studyverse.set_my_role(text) to authenticated;

create or replace function studyverse.my_role() returns text language sql stable security definer set search_path = '' as $$
  select role from studyverse.profiles where user_id = auth.uid();
$$;
revoke all on function studyverse.my_role() from public, anon;
grant execute on function studyverse.my_role() to authenticated;

-- code shown in the child's app; the parent types it in Parent Hub
create table if not exists studyverse.child_codes (code text primary key, child_id uuid not null references auth.users(id) on delete cascade, expires_at timestamptz not null default now() + interval '1 day');
alter table studyverse.child_codes enable row level security;   -- only through the functions below
grant all on studyverse.child_codes to service_role;

create or replace function studyverse.create_child_code() returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); k text; alph text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  if uid is null then return jsonb_build_object('ok', false, 'msg', 'Please sign in first.'); end if;
  if (select role from studyverse.profiles where user_id = uid) = 'parent' then return jsonb_build_object('ok', false, 'msg', 'Parent accounts link children from Parent Hub.'); end if;
  delete from studyverse.child_codes where child_id = uid or expires_at < now();
  loop
    k := ''; for i in 1..6 loop k := k || substr(alph, 1 + floor(random() * length(alph))::int, 1); end loop;
    exit when not exists (select 1 from studyverse.child_codes where code = k) and not exists (select 1 from studyverse.link_codes where code = k);
  end loop;
  insert into studyverse.child_codes(code, child_id) values (k, uid);
  return jsonb_build_object('ok', true, 'code', k, 'expires_at', now() + interval '1 day');
end $$;
revoke all on function studyverse.create_child_code() from public, anon;
grant execute on function studyverse.create_child_code() to authenticated;

create or replace function studyverse.redeem_child_code(p_code text, p_child_name text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c studyverse.child_codes%rowtype; nm text;
begin
  if uid is null then return jsonb_build_object('ok', false, 'msg', 'Please sign in first.'); end if;
  select * into c from studyverse.child_codes where code = upper(trim(coalesce(p_code, ''))) and expires_at > now();
  if not found then return jsonb_build_object('ok', false, 'msg', 'This code is not valid or has expired. Ask your child to make a new one in their app (Me → Link to my parent).'); end if;
  if c.child_id = uid then return jsonb_build_object('ok', false, 'msg', 'This code must be entered on the parent''s account.'); end if;
  if (select count(*) from studyverse.parent_links where parent_id = uid) >= 6 then return jsonb_build_object('ok', false, 'msg', 'You can link up to 6 children.'); end if;
  nm := left(nullif(trim(p_child_name), ''), 40);
  insert into studyverse.parent_links(parent_id, child_id, child_name) values (uid, c.child_id, nm)
    on conflict (parent_id, child_id) do update set child_name = coalesce(excluded.child_name, studyverse.parent_links.child_name);
  delete from studyverse.child_codes where code = c.code;
  insert into studyverse.profiles(user_id, role) values (uid, 'parent') on conflict (user_id) do update set role = coalesce(studyverse.profiles.role, 'parent');
  return jsonb_build_object('ok', true);
end $$;
revoke all on function studyverse.redeem_child_code(text, text) from public, anon;
grant execute on function studyverse.redeem_child_code(text, text) to authenticated;

-- email invites: the parent enters the child's email; when that email signs in, the link is made
create table if not exists studyverse.parent_invites (
  id uuid primary key default gen_random_uuid(),
  parent_id uuid not null references auth.users(id) on delete cascade,
  email text not null, child_name text, created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '30 days', accepted_at timestamptz);
create index if not exists parent_invites_email on studyverse.parent_invites (email) where accepted_at is null;
alter table studyverse.parent_invites enable row level security;
create policy parent_invites_own on studyverse.parent_invites for select to authenticated using (parent_id = (select auth.uid()));
grant select on studyverse.parent_invites to authenticated;
grant all on studyverse.parent_invites to service_role;

-- service only (called by the parent-invite function after checking the parent)
create or replace function studyverse.add_invite(p_parent uuid, p_email text, p_name text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare e text := lower(trim(coalesce(p_email, ''))); pe text;
begin
  select lower(email) into pe from auth.users where id = p_parent;
  if e !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' then return jsonb_build_object('ok', false, 'msg', 'Please enter a valid email.'); end if;
  if e = pe then return jsonb_build_object('ok', false, 'msg', 'Use your child''s own email, not yours.'); end if;
  if (select count(*) from studyverse.parent_links where parent_id = p_parent) >= 6 then return jsonb_build_object('ok', false, 'msg', 'You can link up to 6 children.'); end if;
  if (select count(*) from studyverse.parent_invites where parent_id = p_parent and created_at > now() - interval '1 day') >= 10 then return jsonb_build_object('ok', false, 'msg', 'You have sent many invites today. Please try again tomorrow.'); end if;
  delete from studyverse.parent_invites where parent_id = p_parent and email = e and accepted_at is null;
  insert into studyverse.parent_invites(parent_id, email, child_name) values (p_parent, e, left(nullif(trim(p_name), ''), 40));
  insert into studyverse.profiles(user_id, role) values (p_parent, 'parent') on conflict (user_id) do update set role = coalesce(studyverse.profiles.role, 'parent');
  return jsonb_build_object('ok', true, 'exists', exists (select 1 from auth.users where lower(email) = e));
end $$;
revoke all on function studyverse.add_invite(uuid, text, text) from public, anon, authenticated;
grant execute on function studyverse.add_invite(uuid, text, text) to service_role;

-- the child's app calls this after every sign-in: open invites for this (confirmed) email become links
create or replace function studyverse.claim_invites() returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); e text; n int := 0; r record;
begin
  if uid is null then return jsonb_build_object('ok', false); end if;
  select lower(email) into e from auth.users where id = uid and email_confirmed_at is not null;
  if e is null then return jsonb_build_object('ok', true, 'linked', 0); end if;
  if (select role from studyverse.profiles where user_id = uid) = 'parent' then return jsonb_build_object('ok', true, 'linked', 0); end if;
  for r in select * from studyverse.parent_invites where email = e and accepted_at is null and expires_at > now() and parent_id <> uid loop
    if (select count(*) from studyverse.parent_links where parent_id = r.parent_id) < 6 then
      insert into studyverse.parent_links(parent_id, child_id, child_name) values (r.parent_id, uid, r.child_name)
        on conflict (parent_id, child_id) do nothing;
      n := n + 1;
    end if;
    update studyverse.parent_invites set accepted_at = now() where id = r.id;
  end loop;
  if n > 0 then insert into studyverse.profiles(user_id, role) values (uid, 'student') on conflict (user_id) do update set role = coalesce(studyverse.profiles.role, 'student'); end if;
  return jsonb_build_object('ok', true, 'linked', n);
end $$;
revoke all on function studyverse.claim_invites() from public, anon;
grant execute on function studyverse.claim_invites() to authenticated;
