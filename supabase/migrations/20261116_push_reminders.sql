-- 📳 Phone reminders (web push) for Knowtopia students — schema "studyverse" only.
-- • studyverse.push_subs: one row per phone that switched reminders on (push address + keys from the browser).
--   No policies: only the RPCs below (security definer) and the service role touch it.
-- • Students switch it on/off themselves (Me → Settings); a linked parent can switch it off (child_social.push).
-- • The Edge Function "knowtopia-nudge" runs once a day from pg_cron at 17:31 India time (after school, before night),
--   sends at most ONE reminder per student per day, and skips anyone who already studied today.
-- • The VAPID keys live in studyverse.job_config (service role only). They are set once by hand, NOT in this file.

create table if not exists studyverse.push_subs (
  endpoint   text primary key,
  user_id    uuid not null references auth.users(id) on delete cascade,
  p256dh     text not null,
  auth       text not null,
  need       int,                         -- topics/units still needed for the next Mind Gym pack (sent by the app)
  last_sent  date,                        -- India date of the last reminder to this student
  fails      int not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists push_subs_user on studyverse.push_subs(user_id);
alter table studyverse.push_subs enable row level security;
revoke all on studyverse.push_subs from anon, authenticated;
grant all on studyverse.push_subs to service_role;

alter table studyverse.job_config add column if not exists vapid_public text, add column if not exists vapid_private text;
alter table studyverse.child_social add column if not exists push boolean not null default true;

-- parent switch: add "push" to the existing controls
create or replace function studyverse._pr_on(p_uid uuid, p_kind text) returns boolean language sql stable security definer set search_path = '' as $$
  select coalesce((select case p_kind when 'friends' then s.friends when 'rooms' then s.rooms when 'push' then s.push else s.news end
                   from studyverse.child_social s where s.child_id = p_uid
                     and exists (select 1 from studyverse.parent_links l where l.child_id = p_uid)), true) $$;

drop function if exists studyverse.set_child_social(uuid, boolean, boolean, boolean);
create or replace function studyverse.set_child_social(p_child uuid, p_friends boolean default null, p_rooms boolean default null, p_news boolean default null, p_push boolean default null)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); r studyverse.child_social;
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  if p_child is null or not studyverse._pr_linked(uid, p_child) then return studyverse._pr_err('Only a linked parent can change this.', 'not_parent'); end if;
  insert into studyverse.child_social (child_id, friends, rooms, news, push, updated_by, updated_at)
  values (p_child, coalesce(p_friends, true), coalesce(p_rooms, true), coalesce(p_news, true), coalesce(p_push, true), uid, now())
  on conflict (child_id) do update set friends = coalesce(p_friends, studyverse.child_social.friends), rooms = coalesce(p_rooms, studyverse.child_social.rooms),
    news = coalesce(p_news, studyverse.child_social.news), push = coalesce(p_push, studyverse.child_social.push), updated_by = uid, updated_at = now()
  returning * into r;
  return jsonb_build_object('ok', true, 'friends', r.friends, 'rooms', r.rooms, 'news', r.news, 'push', r.push, 'updated_at', r.updated_at);
end $$;
revoke all on function studyverse.set_child_social(uuid, boolean, boolean, boolean, boolean) from public, anon;
grant execute on function studyverse.set_child_social(uuid, boolean, boolean, boolean, boolean) to authenticated;

create or replace function studyverse.child_social(p_child uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare uid uuid := auth.uid(); r studyverse.child_social;
begin
  if uid is null or p_child is null or not studyverse._pr_linked(uid, p_child) then return studyverse._pr_err('Only a linked parent can see this.', 'not_parent'); end if;
  select * into r from studyverse.child_social where child_id = p_child;
  return jsonb_build_object('ok', true, 'friends', coalesce(r.friends, true), 'rooms', coalesce(r.rooms, true), 'news', coalesce(r.news, true), 'push', coalesce(r.push, true), 'updated_at', r.updated_at);
end $$;

create or replace function studyverse.my_social() returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return studyverse._pr_err('Please sign in first.'); end if;
  return jsonb_build_object('ok', true, 'friends', studyverse._pr_on(uid, 'friends'), 'rooms', studyverse._pr_on(uid, 'rooms'), 'news', studyverse._pr_on(uid, 'news'),
    'push', studyverse._pr_on(uid, 'push'), 'parents', (select count(*) from studyverse.parent_links where child_id = uid));
end $$;

-- the app's public key (safe to share; the app needs it to switch reminders on)
create or replace function studyverse.push_key() returns text language sql stable security definer set search_path = '' as $$
  select vapid_public from studyverse.job_config where id = 1 $$;

-- student: save this phone (also used to refresh the Mind Gym hint). A phone moves to whoever is signed in now.
create or replace function studyverse.push_save(p_endpoint text, p_p256dh text, p_auth text, p_need int default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return jsonb_build_object('ok', false, 'msg', 'Please sign in first.'); end if;
  if coalesce(length(p_endpoint), 0) not between 20 and 1000 or p_endpoint !~ '^https://' or coalesce(length(p_p256dh), 0) not between 40 and 200 or coalesce(length(p_auth), 0) not between 10 and 100 then
    return jsonb_build_object('ok', false, 'msg', 'This phone could not be set up for reminders.'); end if;
  if (select count(*) from studyverse.push_subs where user_id = uid and endpoint <> p_endpoint) >= 5 then
    delete from studyverse.push_subs where endpoint = (select endpoint from studyverse.push_subs where user_id = uid order by updated_at limit 1); end if;
  insert into studyverse.push_subs (endpoint, user_id, p256dh, auth, need) values (p_endpoint, uid, p_p256dh, p_auth, p_need)
  on conflict (endpoint) do update set user_id = uid, p256dh = excluded.p256dh, auth = excluded.auth, need = excluded.need, fails = 0, updated_at = now();
  return jsonb_build_object('ok', true, 'allowed', studyverse._pr_on(uid, 'push'));
end $$;

-- student: switch this phone off
create or replace function studyverse.push_off(p_endpoint text) returns jsonb language sql security definer set search_path = '' as $$
  with d as (delete from studyverse.push_subs where endpoint = p_endpoint and user_id = auth.uid() returning 1)
  select jsonb_build_object('ok', true, 'removed', (select count(*) from d)) $$;

revoke all on function studyverse.push_key(), studyverse.push_save(text, text, text, int), studyverse.push_off(text) from public, anon;
grant execute on function studyverse.push_key(), studyverse.push_save(text, text, text, int), studyverse.push_off(text) to authenticated;

-- service: today's reminders — one phone per student (most recently used), not yet reminded today, parent allows it,
-- has a profile, did not study today. Long-quiet students (7+ days) get at most one reminder a week.
create or replace function studyverse.push_due(p_limit int default 2000) returns table(endpoint text, p256dh text, auth text, user_id uuid, need int,
  name text, ca boolean, streak_n int, streak_last text) language sql stable security definer set search_path = '' as $$
  with t as (select (now() at time zone 'Asia/Kolkata')::date d, (now() at time zone 'utc')::date u),
  one as (
    select distinct on (s.user_id) s.* from studyverse.push_subs s order by s.user_id, s.updated_at desc
  )
  select o.endpoint, o.p256dh, o.auth, o.user_id, o.need,
         left(coalesce(pr.state -> 'st' -> 'profile' ->> 'name', ''), 40),
         coalesce(pr.state -> 'st' -> 'profile' ->> 'course', '') = 'ca',
         coalesce(nullif(pr.state -> 'st' -> 'streak' ->> 'n', '')::int, 0),
         coalesce(pr.state -> 'st' -> 'streak' ->> 'last', '')
  from one o cross join t
  join studyverse.progress pr on pr.user_id = o.user_id
  where pr.state -> 'st' -> 'profile' is not null
    and studyverse._pr_on(o.user_id, 'push')
    and not exists (select 1 from studyverse.push_subs x where x.user_id = o.user_id and x.last_sent >= t.d)
    and coalesce(pr.state -> 'st' -> 'streak' ->> 'last', '') <> t.u::text
    and (coalesce(pr.state -> 'st' -> 'streak' ->> 'last', '') >= (t.u - 7)::text
         or not exists (select 1 from studyverse.push_subs x where x.user_id = o.user_id and x.last_sent > t.d - 7))
  limit greatest(1, least(p_limit, 5000));
$$;

-- service: record the result of one send
create or replace function studyverse.push_result(p_endpoint text, p_user uuid, p_ok boolean, p_gone boolean) returns void language plpgsql security definer set search_path = '' as $$
begin
  if p_gone then delete from studyverse.push_subs where endpoint = p_endpoint; return; end if;
  if p_ok then
    update studyverse.push_subs set last_sent = (now() at time zone 'Asia/Kolkata')::date, fails = 0 where user_id = p_user;
  else
    update studyverse.push_subs set fails = fails + 1 where endpoint = p_endpoint;
    delete from studyverse.push_subs where endpoint = p_endpoint and fails >= 5;
  end if;
end $$;

create or replace function studyverse.push_cfg(p_key text) returns jsonb language sql stable security definer set search_path = '' as $$
  select case when p_key <> '' and p_key = cron_key then jsonb_build_object('public', vapid_public, 'private', vapid_private) end
  from studyverse.job_config where id = 1 $$;

revoke all on function studyverse.push_due(int), studyverse.push_result(text, uuid, boolean, boolean), studyverse.push_cfg(text) from public, anon, authenticated;
grant execute on function studyverse.push_due(int), studyverse.push_result(text, uuid, boolean, boolean), studyverse.push_cfg(text) to service_role;

-- once a day at 17:31 India time (12:01 UTC)
select cron.schedule('studyverse-nudge', '1 12 * * *', $cron$ select net.http_post(
  url := 'https://fyvplhtpsxpxvvsilzqq.supabase.co/functions/v1/knowtopia-nudge',
  headers := jsonb_build_object('Content-Type', 'application/json', 'x-cron-key', (select cron_key from studyverse.job_config where id = 1)),
  body := '{}'::jsonb, timeout_milliseconds := 120000) $cron$);
