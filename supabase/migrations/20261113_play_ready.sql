-- ============================================================================================
-- StudyVerse — Google Play readiness (Families policy, account deletion, consent records). Schema studyverse.
--   1. Consent records: studyverse.legal_settings (one row: current policy version) + studyverse.consents (append-only).
--      legal_status() / accept_terms() — the app shows a one-time "We've updated our terms" gate when the caller has not
--      accepted the current version. Sign-up sends { sv_consent: { v, g } } in the user metadata; legal_status() records
--      it as a 'signup' row the first time (so a sign-up confirmed on another phone still counts).
--   2. Adults-only handwriting reading: profiles.adult_confirmed_at, set by confirm_adult() when a student answers "I'm 18
--      or older" in the "Read my handwriting?" prompt. read_allowed(p_user) (service role only) is checked by the Edge
--      Function studyverse-read: refused if not confirmed, or if the account is a student in a SCHOOL class.
--   3. Parent controls (Families): studyverse.child_social — friends & cheers / live game rooms / friend news, each
--      on (default) or off. Written ONLY by a linked parent (set_child_social), read by the parent (child_social) and by
--      the child (my_social). Enforced HERE, on the server: squad_home, squad_add_friend, squad_answer (accept),
--      squad_cheer, create_room and join_room are wrapped (same names and signatures; the original bodies are renamed to
--      _pr_base_<name> and can no longer be called by clients). Settings apply only while a parent is linked.
--   4. Report & block: studyverse.reports (preset reasons only; free text only for confirmed adults; rate-limited) via
--      report_user(); studyverse.blocks via squad_block() (removes the friendship; blocked people cannot send requests,
--      cheer or appear in each other's Squad). Owner: owner_reports(), owner_report_set(), and Pulse Coach items of kind
--      'report' (owner_dash_smart is wrapped the same way).
--   5. Account deletion: _pr_delete_user_data(p_user) (service role only), called by the Edge Function delete-account
--      before it deletes the auth user (which cascades almost everything). Payments are KEPT for tax records with
--      user_id set to NULL (the payments FK becomes ON DELETE SET NULL).
-- Needs (already in the project): every earlier migration (squad, live games, puzzle race, owner dashboard).
-- Idempotent: safe to run again. If an earlier migration that defines a wrapped function is run AGAIN later, run this
-- file again afterwards (it detects a fresh original and re-wraps it).
-- ============================================================================================

-- ---------- 1. tables ----------
create table if not exists studyverse.legal_settings (
  id             int primary key default 1 check (id = 1),
  version        text not null default '2.0',              -- = SV_LEGAL.version in legal/legal.js
  effective_on   date not null default date '2026-11-09',
  summary        text,                                     -- "What changed", shown on the gate
  needs_reaccept boolean not null default true             -- false = small change: no gate for people who accepted before
);
insert into studyverse.legal_settings (id, version, effective_on, summary, needs_reaccept)
values (1, '2.0', date '2026-11-09', 'New pages for children, parents and schools; clearer rules for friends, game rooms, handwriting reading (adults only) and deleting your account.', true)
on conflict (id) do nothing;

create table if not exists studyverse.consents (
  id             bigint generated always as identity primary key,
  subject_id     uuid not null references auth.users(id) on delete cascade,  -- whose data (the learner)
  actor_id       uuid references auth.users(id) on delete set null,          -- who agreed
  kind           text not null check (kind in ('terms', 'parental', 'school_upload', 'social', 'ai_reading', 'marketing')),
  version        text not null check (length(version) between 1 and 20),
  granted        boolean not null default true,                              -- false = withdrawal (a new row; never update)
  how            text not null check (how in ('signup', 'gate', 'app', 'parent_hub', 'school_upload', 'existing', 'support')),
  verify         text check (verify is null or length(verify) <= 30),
  institution_id uuid,
  user_agent     text check (user_agent is null or length(user_agent) <= 200),
  at             timestamptz not null default now()
);
create index if not exists consents_subject on studyverse.consents (subject_id, kind, at desc);

alter table studyverse.profiles add column if not exists adult_confirmed_at timestamptz;

create table if not exists studyverse.child_social (
  child_id   uuid primary key references auth.users(id) on delete cascade,
  friends    boolean not null default true,        -- 👫 friends & cheers (incl. the friends league)
  rooms      boolean not null default true,        -- 🎮 live game rooms
  news       boolean not null default true,        -- 🔔 friend news
  updated_by uuid references auth.users(id) on delete set null,
  updated_at timestamptz not null default now()
);

create table if not exists studyverse.reports (
  id              bigint generated always as identity primary key,
  reporter        uuid references auth.users(id) on delete set null,
  reported        uuid references auth.users(id) on delete set null,
  reported_name   text check (reported_name is null or length(reported_name) <= 40),
  reporter_name   text check (reporter_name is null or length(reporter_name) <= 40),
  context         text not null check (context in ('friend', 'request', 'room')),
  room_code       text check (room_code is null or room_code ~ '^[A-Z]{6}$'),
  reason          text not null check (reason in ('unkind', 'cheating', 'name', 'other')),
  detail          text check (detail is null or length(detail) <= 300),       -- adults only
  status          text not null default 'open' check (status in ('open', 'done')),
  created_at      timestamptz not null default now(),
  done_at         timestamptz
);
create index if not exists reports_open on studyverse.reports (status, created_at desc);
create index if not exists reports_by on studyverse.reports (reporter, created_at desc);

create table if not exists studyverse.blocks (
  blocker    uuid not null references auth.users(id) on delete cascade,
  blocked    uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (blocker, blocked),
  check (blocker <> blocked)
);
create index if not exists blocks_blocked on studyverse.blocks (blocked);

alter table studyverse.legal_settings enable row level security;
alter table studyverse.consents enable row level security;
alter table studyverse.child_social enable row level security;
alter table studyverse.reports enable row level security;
alter table studyverse.blocks enable row level security;
-- no policies: everything goes through the SECURITY DEFINER functions below
revoke all on studyverse.legal_settings, studyverse.consents, studyverse.child_social, studyverse.reports, studyverse.blocks from anon, authenticated;
grant all on studyverse.legal_settings, studyverse.consents, studyverse.child_social, studyverse.reports, studyverse.blocks to service_role;

-- payments are kept after an account is deleted (tax / accounting records), without the person: user_id → NULL
alter table studyverse.payments alter column user_id drop not null;
alter table studyverse.payments drop constraint if exists payments_user_id_fkey;
alter table studyverse.payments add constraint payments_user_id_fkey foreign key (user_id) references auth.users(id) on delete set null;

-- ---------- 2. helpers ----------
create or replace function studyverse._pr_err(p_msg text, p_code text default null) returns jsonb language sql immutable set search_path = '' as $$
  select jsonb_build_object('ok', false, 'msg', p_msg) || case when p_code is null then '{}'::jsonb else jsonb_build_object('code', p_code) end $$;
-- a parent control is on unless a LINKED parent turned it off
create or replace function studyverse._pr_on(p_uid uuid, p_kind text) returns boolean language sql stable security definer set search_path = '' as $$
  select coalesce((select case p_kind when 'friends' then s.friends when 'rooms' then s.rooms else s.news end
                   from studyverse.child_social s where s.child_id = p_uid
                     and exists (select 1 from studyverse.parent_links l where l.child_id = p_uid)), true) $$;
create or replace function studyverse._pr_blocked(x uuid, y uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.blocks where (blocker = x and blocked = y) or (blocker = y and blocked = x)) $$;
-- may x and y see / befriend / cheer each other?
create or replace function studyverse._pr_pair_ok(x uuid, y uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select not studyverse._pr_blocked(x, y) and studyverse._pr_on(y, 'friends') and studyverse._pr_on(x, 'friends') $$;
create or replace function studyverse._pr_school_student(p_uid uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.institution_members m join studyverse.inst_classes c on c.id = m.class_id
                 where m.user_id = p_uid and m.role = 'student' and c.course like 'school-%') $$;
create or replace function studyverse._pr_linked(p_parent uuid, p_child uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.parent_links where parent_id = p_parent and child_id = p_child) $$;
create or replace function studyverse._pr_clean(p text, n int) returns text language sql immutable set search_path = '' as $$
  select nullif(left(trim(regexp_replace(coalesce(p, ''), '[[:cntrl:]<>]', ' ', 'g')), n), '') $$;
revoke all on function studyverse._pr_err(text, text), studyverse._pr_on(uuid, text), studyverse._pr_blocked(uuid, uuid), studyverse._pr_pair_ok(uuid, uuid),
  studyverse._pr_school_student(uuid), studyverse._pr_linked(uuid, uuid), studyverse._pr_clean(text, int) from public, anon, authenticated;

-- ---------- 3. consent: status + accept ----------
create or replace function studyverse.legal_status() returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); s studyverse.legal_settings; m jsonb; acc boolean; par boolean;
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  select * into s from studyverse.legal_settings where id = 1;
  if not found then return jsonb_build_object('ok', true, 'accepted', true, 'parental', true); end if;
  -- the tick boxes on the sign-up form travel in the user metadata: record them once
  if not exists (select 1 from studyverse.consents where subject_id = uid and kind = 'terms' and version = s.version) then
    begin
      select u.raw_user_meta_data -> 'sv_consent' into m from auth.users u where u.id = uid;
    exception when others then m := null; end;
    if jsonb_typeof(m) = 'object' and m ->> 'v' = s.version then
      insert into studyverse.consents (subject_id, actor_id, kind, version, how) values (uid, uid, 'terms', s.version, 'signup');
      if coalesce(m ->> 'g', '') in ('true', '1') and not exists (select 1 from studyverse.consents where subject_id = uid and kind = 'parental' and granted) then
        insert into studyverse.consents (subject_id, actor_id, kind, version, how, verify) values (uid, uid, 'parental', s.version, 'signup', 'declared');
      end if;
    end if;
  end if;
  acc := exists (select 1 from studyverse.consents where subject_id = uid and kind = 'terms' and granted and version = s.version)
      or (not s.needs_reaccept and exists (select 1 from studyverse.consents where subject_id = uid and kind = 'terms' and granted));
  par := coalesce((select c.granted from studyverse.consents c where c.subject_id = uid and c.kind = 'parental' order by c.at desc, c.id desc limit 1), false)
      or exists (select 1 from studyverse.parent_links where child_id = uid);
  return jsonb_build_object('ok', true, 'version', s.version, 'effective_on', s.effective_on, 'summary', s.summary, 'accepted', acc, 'parental', par,
    'school', studyverse._pr_school_student(uid));
end $$;

create or replace function studyverse.accept_terms(p_version text, p_guardian boolean default false, p_how text default 'gate', p_agent text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); v text; h text := case when p_how in ('signup', 'gate') then p_how else 'gate' end;
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  select version into v from studyverse.legal_settings where id = 1;
  if v is null or p_version is distinct from v then return studyverse._pr_err('Our terms were just updated. Please read them again.', 'version') || jsonb_build_object('version', v); end if;
  if not exists (select 1 from studyverse.consents where subject_id = uid and kind = 'terms' and granted and version = v) then
    insert into studyverse.consents (subject_id, actor_id, kind, version, how, user_agent) values (uid, uid, 'terms', v, h, studyverse._pr_clean(p_agent, 200));
  end if;
  if coalesce(p_guardian, false) and not coalesce((select c.granted from studyverse.consents c where c.subject_id = uid and c.kind = 'parental' order by c.at desc, c.id desc limit 1), false) then
    insert into studyverse.consents (subject_id, actor_id, kind, version, how, verify, user_agent) values (uid, uid, 'parental', v, h, 'declared', studyverse._pr_clean(p_agent, 200));
  end if;
  return jsonb_build_object('ok', true, 'version', v);
end $$;

-- ---------- 4. adults-only handwriting reading ----------
create or replace function studyverse.confirm_adult() returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); v text;
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  if studyverse._pr_school_student(uid) then return studyverse._pr_err('Photo reading is only for adult CA students.', 'school'); end if;
  insert into studyverse.profiles (user_id, adult_confirmed_at) values (uid, now())
    on conflict (user_id) do update set adult_confirmed_at = coalesce(studyverse.profiles.adult_confirmed_at, now());
  if not exists (select 1 from studyverse.consents where subject_id = uid and kind = 'ai_reading' and granted) then
    select version into v from studyverse.legal_settings where id = 1;
    insert into studyverse.consents (subject_id, actor_id, kind, version, how, verify) values (uid, uid, 'ai_reading', coalesce(v, '2.0'), 'app', 'declared_18');
  end if;
  return jsonb_build_object('ok', true);
end $$;

-- called by the Edge Function studyverse-read with the service role
create or replace function studyverse.read_allowed(p_user uuid) returns jsonb
language sql stable security definer set search_path = '' as $$
  select case
    when p_user is null then jsonb_build_object('ok', false, 'why', 'signin')
    when studyverse._pr_school_student(p_user) then jsonb_build_object('ok', false, 'why', 'school')
    when (select adult_confirmed_at from studyverse.profiles where user_id = p_user) is null then jsonb_build_object('ok', false, 'why', 'adult')
    else jsonb_build_object('ok', true) end $$;

-- ---------- 5. parent controls ----------
create or replace function studyverse.set_child_social(p_child uuid, p_friends boolean default null, p_rooms boolean default null, p_news boolean default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); r studyverse.child_social;
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  if p_child is null or not studyverse._pr_linked(uid, p_child) then return studyverse._pr_err('Only a linked parent can change this.', 'not_parent'); end if;
  insert into studyverse.child_social (child_id, friends, rooms, news, updated_by, updated_at)
  values (p_child, coalesce(p_friends, true), coalesce(p_rooms, true), coalesce(p_news, true), uid, now())
  on conflict (child_id) do update set friends = coalesce(p_friends, studyverse.child_social.friends), rooms = coalesce(p_rooms, studyverse.child_social.rooms),
    news = coalesce(p_news, studyverse.child_social.news), updated_by = uid, updated_at = now()
  returning * into r;
  return jsonb_build_object('ok', true, 'friends', r.friends, 'rooms', r.rooms, 'news', r.news, 'updated_at', r.updated_at);
end $$;

create or replace function studyverse.child_social(p_child uuid) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare uid uuid := auth.uid(); r studyverse.child_social;
begin
  if uid is null or p_child is null or not studyverse._pr_linked(uid, p_child) then return studyverse._pr_err('Only a linked parent can see this.', 'not_parent'); end if;
  select * into r from studyverse.child_social where child_id = p_child;
  return jsonb_build_object('ok', true, 'friends', coalesce(r.friends, true), 'rooms', coalesce(r.rooms, true), 'news', coalesce(r.news, true), 'updated_at', r.updated_at);
end $$;

create or replace function studyverse.my_social() returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  return jsonb_build_object('ok', true, 'friends', studyverse._pr_on(uid, 'friends'), 'rooms', studyverse._pr_on(uid, 'rooms'), 'news', studyverse._pr_on(uid, 'news'),
    'parents', (select count(*) from studyverse.parent_links where child_id = uid));
end $$;

-- ---------- 6. report + block ----------
create or replace function studyverse.report_user(p_user uuid, p_reason text, p_context text, p_room text default null, p_detail text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); rc text := upper(trim(coalesce(p_room, ''))); nm text; me_nm text; adult boolean;
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  if p_user is null or p_user = uid then return studyverse._pr_err('Choose who you want to report.'); end if;
  if p_reason is null or p_reason not in ('unkind', 'cheating', 'name', 'other') then return studyverse._pr_err('Pick a reason.'); end if;
  if p_context is null or p_context not in ('friend', 'request', 'room') then return studyverse._pr_err('Pick a reason.'); end if;
  if p_context = 'room' then
    select rp.name into nm from studyverse.room_players rp where rp.code = rc and rp.user_id = p_user;
    if nm is null or not exists (select 1 from studyverse.room_players where code = rc and user_id = uid) then return studyverse._pr_err('You can report only players in your room.'); end if;
    select rp.name into me_nm from studyverse.room_players rp where rp.code = rc and rp.user_id = uid;
  else
    if not exists (select 1 from studyverse.squad_friends where a = least(uid, p_user) and b = greatest(uid, p_user))
       and not studyverse._pr_blocked(uid, p_user) then return studyverse._pr_err('You can report only your friends or friend requests.'); end if;
    select name into nm from studyverse.squad_profile where user_id = p_user;
    select name into me_nm from studyverse.squad_profile where user_id = uid;
    rc := null;
  end if;
  if exists (select 1 from studyverse.reports where reporter = uid and reported = p_user and created_at > now() - interval '1 day') then
    return jsonb_build_object('ok', true, 'already', true, 'msg', 'Thank you. We already have your report.'); end if;
  if (select count(*) from studyverse.reports where reporter = uid and created_at > now() - interval '1 day') >= 10 then
    return studyverse._pr_err('You sent many reports today. Please write to support@moneyviel.com if something is wrong.', 'limit'); end if;
  adult := (select adult_confirmed_at is not null from studyverse.profiles where user_id = uid) and not studyverse._pr_school_student(uid);
  insert into studyverse.reports (reporter, reported, reported_name, reporter_name, context, room_code, reason, detail)
  values (uid, p_user, left(nm, 40), left(me_nm, 40), p_context, nullif(rc, ''), p_reason, case when coalesce(adult, false) then studyverse._pr_clean(p_detail, 300) end);
  return jsonb_build_object('ok', true, 'msg', 'Thank you for telling us. We will look at it.');
end $$;

create or replace function studyverse.squad_block(p_user uuid) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  if p_user is null or p_user = uid then return studyverse._pr_err('Choose who you want to block.'); end if;
  if not exists (select 1 from studyverse.squad_friends where a = least(uid, p_user) and b = greatest(uid, p_user)) and not studyverse._pr_blocked(uid, p_user) then
    return studyverse._pr_err('You can block only your friends or friend requests.'); end if;
  if (select count(*) from studyverse.blocks where blocker = uid) >= 200 then return studyverse._pr_err('You have blocked many people already.'); end if;
  delete from studyverse.squad_friends where a = least(uid, p_user) and b = greatest(uid, p_user);
  delete from studyverse.squad_cheers where from_id = p_user and to_id = uid and seen_at is null;
  insert into studyverse.blocks (blocker, blocked) values (uid, p_user) on conflict do nothing;
  return jsonb_build_object('ok', true);
end $$;

-- ---------- 7. owner: reports ----------
create or replace function studyverse.owner_reports(p_status text default 'open', p_limit int default 100) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
begin
  if not studyverse._od_is_owner() then return null; end if;
  return jsonb_build_object('ok', true,
    'open', (select count(*) from studyverse.reports where status = 'open'),
    'rows', coalesce((select jsonb_agg(x order by (x ->> 'created_at') desc) from (
      select jsonb_build_object('id', r.id, 'created_at', r.created_at, 'reason', r.reason, 'context', r.context, 'room_code', r.room_code, 'detail', r.detail, 'status', r.status,
        'reported_id', r.reported, 'reported_name', r.reported_name, 'reported_email', ru.email,
        'reporter_id', r.reporter, 'reporter_name', r.reporter_name, 'reporter_email', pu.email,
        'n_on_user', (select count(*) from studyverse.reports r2 where r2.reported = r.reported and r2.created_at > now() - interval '30 days')) as x
      from studyverse.reports r left join auth.users ru on ru.id = r.reported left join auth.users pu on pu.id = r.reporter
      where p_status is null or p_status = 'all' or r.status = p_status
      order by r.created_at desc limit least(greatest(coalesce(p_limit, 100), 1), 500)) t), '[]'::jsonb));
end $$;

create or replace function studyverse.owner_report_set(p_id bigint, p_status text) returns jsonb
language plpgsql security definer set search_path = '' as $$
begin
  if not studyverse._od_is_owner() then return null; end if;
  if p_status not in ('open', 'done') then return studyverse._pr_err('Not a valid status.'); end if;
  update studyverse.reports set status = p_status, done_at = case when p_status = 'done' then now() end where id = p_id;
  if not found then return studyverse._pr_err('Report not found.'); end if;
  return jsonb_build_object('ok', true, 'status', p_status);
end $$;

-- ---------- 8. account deletion (service role only; the Edge Function delete-account deletes the auth user next) ----------
create or replace function studyverse._pr_delete_user_data(p_user uuid) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare em text; n_pay int; n_kids int; n_par int;
begin
  if p_user is null then return studyverse._pr_err('No user.'); end if;
  if exists (select 1 from studyverse.admins where user_id = p_user) then
    return studyverse._pr_err('Owner accounts cannot be deleted from the app. Please write to support@moneyviel.com.', 'owner'); end if;
  select lower(email) into em from auth.users where id = p_user;
  update studyverse.payments set user_id = null where user_id = p_user;                    -- kept for tax records, without the person
  get diagnostics n_pay = row_count;
  delete from studyverse.parent_links where parent_id = p_user;                            -- a parent: unlink every child
  get diagnostics n_kids = row_count;
  delete from studyverse.parent_links where child_id = p_user;                             -- a child: unlink from parents
  get diagnostics n_par = row_count;
  delete from studyverse.room_answers where user_id = p_user;                              -- no FK on these
  update studyverse.game_rooms set turn_user = null where turn_user = p_user;
  update studyverse.inst_bulk_log set caller = null where caller = p_user;
  if em is not null then delete from studyverse.parent_invites where lower(email) = em; end if;   -- invites addressed to this email
  delete from studyverse.squad_friends where requested_by = p_user;
  return jsonb_build_object('ok', true, 'payments_kept', n_pay, 'children_unlinked', n_kids, 'parents_unlinked', n_par);
end $$;

-- ---------- 9. server-side enforcement: wrap the existing RPCs (same names and signatures) ----------
-- Each original is renamed once to studyverse._pr_base_<name>; the wrapper below carries the marker [playready wrapper].
do $$
declare f record; cur regprocedure;
begin
  for f in select * from (values
      ('squad_home', '', 'squad_home()'),
      ('squad_add_friend', 'text', 'squad_add_friend(text)'),
      ('squad_answer', 'uuid, boolean', 'squad_answer(uuid, boolean)'),
      ('squad_cheer', 'uuid, text', 'squad_cheer(uuid, text)'),
      ('create_room', 'text, text, int, int, text, text, text, text', 'create_room(text, text, int, int, text, text, text, text)'),
      ('join_room', 'text, text, text, text', 'join_room(text, text, text, text)'),
      ('owner_dash_smart', 'jsonb', 'owner_dash_smart(jsonb)')) v(name, args, sig) loop
    cur := to_regprocedure('studyverse.' || f.sig);
    if cur is null then raise notice 'play_ready: % not found (earlier migration missing?) — wrapper will fail until it exists', f.sig; continue; end if;
    if (select prosrc from pg_proc where oid = cur) like '%[playready wrapper]%' then continue; end if;   -- already wrapped
    execute format('drop function if exists studyverse._pr_base_%s(%s)', f.name, f.args);
    execute format('alter function studyverse.%s rename to _pr_base_%s', f.sig, f.name);
  end loop;
end $$;

create or replace function studyverse.squad_home() returns jsonb
language plpgsql security definer set search_path = '' as $$
-- [playready wrapper] parent controls + blocks on top of _pr_base_squad_home()
declare uid uuid := auth.uid(); r jsonb := studyverse._pr_base_squad_home(); fr boolean; nw boolean;
begin
  if uid is null or r is null or coalesce(r ->> 'ok', '') <> 'true' then return r; end if;
  fr := studyverse._pr_on(uid, 'friends'); nw := studyverse._pr_on(uid, 'news');
  if not fr then
    r := r || jsonb_build_object('friends', '[]'::jsonb, 'incoming', '[]'::jsonb, 'outgoing', 0, 'cheers', '[]'::jsonb);
  else
    r := r || jsonb_build_object(
      'friends', coalesce((select jsonb_agg(x.v order by x.i) from jsonb_array_elements(coalesce(r -> 'friends', '[]'::jsonb)) with ordinality x(v, i)
                           where studyverse._pr_pair_ok(uid, (x.v ->> 'id')::uuid)), '[]'::jsonb),
      'incoming', coalesce((select jsonb_agg(x.v order by x.i) from jsonb_array_elements(coalesce(r -> 'incoming', '[]'::jsonb)) with ordinality x(v, i)
                           where studyverse._pr_pair_ok(uid, (x.v ->> 'id')::uuid)), '[]'::jsonb));
  end if;
  if not nw then      -- friend news is built from these two fields only: leave them out
    r := r || jsonb_build_object('friends', coalesce((select jsonb_agg((x.v - 'pz' - 'today') order by x.i) from jsonb_array_elements(r -> 'friends') with ordinality x(v, i)), '[]'::jsonb));
  end if;
  return r || jsonb_build_object('social', jsonb_build_object('friends', fr, 'rooms', studyverse._pr_on(uid, 'rooms'), 'news', nw));
end $$;

create or replace function studyverse.squad_add_friend(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
-- [playready wrapper]
declare uid uuid := auth.uid(); other uuid;
begin
  if uid is not null then
    if not studyverse._pr_on(uid, 'friends') then return studyverse._pr_err('Your parent has turned off friends for now.', 'parent_off'); end if;
    select user_id into other from studyverse.squad_profile where code = upper(regexp_replace(coalesce(p_code, ''), '\s', '', 'g'));
    if other is not null and other <> uid and not studyverse._pr_pair_ok(uid, other) then
      return studyverse._pr_err('You can''t add this friend right now.', 'not_allowed'); end if;
  end if;
  return studyverse._pr_base_squad_add_friend(p_code);
end $$;

create or replace function studyverse.squad_answer(p_user uuid, p_accept boolean) returns jsonb
language plpgsql security definer set search_path = '' as $$
-- [playready wrapper]
declare uid uuid := auth.uid();
begin
  if uid is not null and coalesce(p_accept, false) then
    if not studyverse._pr_on(uid, 'friends') then return studyverse._pr_err('Your parent has turned off friends for now.', 'parent_off'); end if;
    if p_user is not null and not studyverse._pr_pair_ok(uid, p_user) then return studyverse._pr_err('You can''t add this friend right now.', 'not_allowed'); end if;
  end if;
  return studyverse._pr_base_squad_answer(p_user, p_accept);
end $$;

create or replace function studyverse.squad_cheer(p_to uuid, p_kind text) returns jsonb
language plpgsql security definer set search_path = '' as $$
-- [playready wrapper]
declare uid uuid := auth.uid();
begin
  if uid is not null then
    if not studyverse._pr_on(uid, 'friends') then return studyverse._pr_err('Your parent has turned off friends and cheers for now.', 'parent_off'); end if;
    if p_to is not null and not studyverse._pr_pair_ok(uid, p_to) then return studyverse._pr_err('You can cheer only your friends.', 'not_allowed'); end if;
  end if;
  return studyverse._pr_base_squad_cheer(p_to, p_kind);
end $$;

create or replace function studyverse.create_room(p_game text, p_mode text, p_rounds int, p_turn_secs int, p_name text, p_avatar text, p_course text, p_level text)
returns jsonb language plpgsql security definer set search_path = '' as $$
-- [playready wrapper]
begin
  if auth.uid() is not null and not studyverse._pr_on(auth.uid(), 'rooms') then
    return studyverse._pr_err('Your parent has turned off live game rooms for now. You can still play the Arcade games on your own.', 'parent_off'); end if;
  return studyverse._pr_base_create_room(p_game, p_mode, p_rounds, p_turn_secs, p_name, p_avatar, p_course, p_level);
end $$;

create or replace function studyverse.join_room(p_code text, p_name text, p_avatar text, p_course text)
returns jsonb language plpgsql security definer set search_path = '' as $$
-- [playready wrapper]
begin
  if auth.uid() is not null and not studyverse._pr_on(auth.uid(), 'rooms') then
    return studyverse._pr_err('Your parent has turned off live game rooms for now. You can still play the Arcade games on your own.', 'parent_off'); end if;
  return studyverse._pr_base_join_room(p_code, p_name, p_avatar, p_course);
end $$;

-- Pulse Coach: open reports (last 30 days) become urgent items of kind 'report' (state via owner_followups as usual)
create or replace function studyverse.owner_dash_smart(p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
-- [playready wrapper]
declare r jsonb := studyverse._pr_base_owner_dash_smart(p); me uuid := auth.uid(); rep jsonb;
begin
  if r is null or coalesce(r ->> 'ok', '') <> 'true' then return r; end if;
  select coalesce(jsonb_agg(jsonb_build_object('key', 'report:' || x.id, 'kind', 'report', 'pri', 1, 'who', 'student', 'id', x.reported, 'email', ru.email, 'name', x.reported_name,
           'parents', null, 'phone', null, 'band', null, 'due', x.created_at,
           'meta', jsonb_build_object('reason', x.reason, 'context', x.context, 'room', x.room_code, 'by', x.reporter_name, 'detail', x.detail, 'rid', x.id,
                                      'n', (select count(*) from studyverse.reports r2 where r2.reported = x.reported and r2.created_at > now() - interval '30 days')),
           'state', case when fu.status = 'snoozed' and fu.snooze_until <= now() then 'open' else coalesce(fu.status, 'open') end,
           'snooze_until', fu.snooze_until, 'note', fu.note, 'marked_at', fu.updated_at) order by x.created_at desc), '[]'::jsonb)
    into rep
  from (select * from studyverse.reports where status = 'open' and created_at > now() - interval '30 days' order by created_at desc limit 50) x
  left join auth.users ru on ru.id = x.reported
  left join studyverse.owner_followups fu on fu.owner_id = me and fu.item_key = 'report:' || x.id;
  return jsonb_set(r, '{items}', rep || coalesce(r -> 'items', '[]'::jsonb));
end $$;

-- ---------- 10. privileges ----------
do $$
declare r record;
begin
  -- originals: callable only through the wrappers
  for r in select p.oid::regprocedure as sig from pg_proc p where p.pronamespace = 'studyverse'::regnamespace and p.proname like '\_pr\_base\_%' loop
    execute format('revoke all on function %s from public, anon, authenticated', r.sig);
    execute format('grant execute on function %s to service_role', r.sig);
  end loop;
end $$;
revoke all on function studyverse.legal_status(), studyverse.accept_terms(text, boolean, text, text), studyverse.confirm_adult(),
  studyverse.set_child_social(uuid, boolean, boolean, boolean), studyverse.child_social(uuid), studyverse.my_social(),
  studyverse.report_user(uuid, text, text, text, text), studyverse.squad_block(uuid), studyverse.owner_reports(text, int), studyverse.owner_report_set(bigint, text),
  studyverse.squad_home(), studyverse.squad_add_friend(text), studyverse.squad_answer(uuid, boolean), studyverse.squad_cheer(uuid, text),
  studyverse.create_room(text, text, int, int, text, text, text, text), studyverse.join_room(text, text, text, text), studyverse.owner_dash_smart(jsonb)
  from public, anon;
grant execute on function studyverse.legal_status(), studyverse.accept_terms(text, boolean, text, text), studyverse.confirm_adult(),
  studyverse.set_child_social(uuid, boolean, boolean, boolean), studyverse.child_social(uuid), studyverse.my_social(),
  studyverse.report_user(uuid, text, text, text, text), studyverse.squad_block(uuid), studyverse.owner_reports(text, int), studyverse.owner_report_set(bigint, text),
  studyverse.squad_home(), studyverse.squad_add_friend(text), studyverse.squad_answer(uuid, boolean), studyverse.squad_cheer(uuid, text),
  studyverse.create_room(text, text, int, int, text, text, text, text), studyverse.join_room(text, text, text, text), studyverse.owner_dash_smart(jsonb)
  to authenticated, service_role;
revoke all on function studyverse.read_allowed(uuid), studyverse._pr_delete_user_data(uuid) from public, anon, authenticated;
grant execute on function studyverse.read_allowed(uuid), studyverse._pr_delete_user_data(uuid) to service_role;
