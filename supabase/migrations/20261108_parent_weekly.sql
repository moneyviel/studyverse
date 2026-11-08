-- Weekly parent report emails (one short email per parent per week; full report stays in the app)
create table if not exists studyverse.parent_prefs (
  parent_id uuid primary key references auth.users(id) on delete cascade,
  weekly_email boolean not null default true,
  last_sent date,
  unsub uuid not null default gen_random_uuid(),
  updated_at timestamptz not null default now()
);
alter table studyverse.parent_prefs enable row level security;
create policy parent_prefs_own on studyverse.parent_prefs for select to authenticated using (parent_id = (select auth.uid()));
grant select on studyverse.parent_prefs to authenticated;
grant all on studyverse.parent_prefs to service_role;

create table if not exists studyverse.job_config (id int primary key default 1 check (id = 1), cron_key text not null default replace(gen_random_uuid()::text || gen_random_uuid()::text, '-', ''));
alter table studyverse.job_config enable row level security;   -- no policies: only the service role and cron read it
insert into studyverse.job_config(id) values (1) on conflict do nothing;
grant all on studyverse.job_config to service_role;

-- parent switches the weekly email on/off
create or replace function studyverse.set_weekly_email(p_on boolean) returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return jsonb_build_object('ok', false); end if;
  insert into studyverse.parent_prefs(parent_id, weekly_email) values (uid, p_on)
    on conflict (parent_id) do update set weekly_email = excluded.weekly_email, updated_at = now();
  return jsonb_build_object('ok', true, 'on', p_on);
end $$;
revoke all on function studyverse.set_weekly_email(boolean) from public, anon;
grant execute on function studyverse.set_weekly_email(boolean) to authenticated;

-- service only: parents due a weekly email (oldest first), with their children's synced progress
create or replace function studyverse.weekly_due(p_limit int) returns table(parent_id uuid, email text, unsub uuid, children jsonb)
language sql security definer set search_path = '' as $$
  with par as (
    select distinct l.parent_id from studyverse.parent_links l
  ), due as (
    select p.parent_id, u.email, coalesce(pp.unsub, gen_random_uuid()) unsub, pp.last_sent, pp.parent_id is null as fresh
    from par p join auth.users u on u.id = p.parent_id
    left join studyverse.parent_prefs pp on pp.parent_id = p.parent_id
    where coalesce(pp.weekly_email, true) and u.email is not null
      and (pp.last_sent is null or pp.last_sent <= (now() at time zone 'Asia/Kolkata')::date - 7)
    order by pp.last_sent nulls first limit greatest(1, least(p_limit, 280))
  )
  select d.parent_id, d.email, d.unsub,
    (select coalesce(jsonb_agg(jsonb_build_object('name', l.child_name, 'state', pr.state -> 'st', 'updated_at', pr.updated_at,
        'controls', cc.controls)), '[]'::jsonb)
       from studyverse.parent_links l
       left join studyverse.progress pr on pr.user_id = l.child_id
       left join studyverse.child_controls cc on cc.child_id = l.child_id
      where l.parent_id = d.parent_id) children
  from due d;
$$;
revoke all on function studyverse.weekly_due(int) from public, anon, authenticated;
grant execute on function studyverse.weekly_due(int) to service_role;

-- service only: mark sent (creates the prefs row with its unsubscribe id on first send)
create or replace function studyverse.weekly_mark(p_parent uuid, p_unsub uuid) returns void language sql security definer set search_path = '' as $$
  insert into studyverse.parent_prefs(parent_id, last_sent, unsub) values (p_parent, (now() at time zone 'Asia/Kolkata')::date, p_unsub)
  on conflict (parent_id) do update set last_sent = excluded.last_sent, updated_at = now();
$$;
revoke all on function studyverse.weekly_mark(uuid, uuid) from public, anon, authenticated;
grant execute on function studyverse.weekly_mark(uuid, uuid) to service_role;

-- anyone with the link from their email can unsubscribe (no sign-in needed)
create or replace function studyverse.weekly_unsub(p_unsub uuid) returns boolean language sql security definer set search_path = '' as $$
  update studyverse.parent_prefs set weekly_email = false, updated_at = now() where unsub = p_unsub returning true;
$$;
revoke all on function studyverse.weekly_unsub(uuid) from public, anon, authenticated;
grant execute on function studyverse.weekly_unsub(uuid) to service_role;
