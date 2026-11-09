-- ============================================================================================
-- StudyVerse — OWNER dashboard + 🧠 Smart Manager (pairs with js/owner.js).  Schema studyverse.
-- Purpose: help the owner see how the app is used, whether subscriptions grow or fall, and who needs a follow-up
-- (students, parents, schools, coaching centres) so nobody is lost. Data is used only to improve the service.
--
-- Everything here is READ-ONLY on the app's data. The only table written is studyverse.owner_followups (the owner's
-- own "done / snoozed / note" marks on Smart Manager items).
-- Every owner_dash_* function is SECURITY DEFINER, search_path = '', and returns NULL unless the caller is in
-- studyverse.admins. Helpers named _od_* are not callable by app users (revoked from public/anon/authenticated).
-- No passwords, tokens, payment ids or exact locations are returned; students' free text is not returned
-- (only the first/full name the student typed in their own profile, needed to recognise them).
--
-- Sources:  auth.users (email, created_at, last_sign_in_at) · profiles · progress.state.st (the app's synced ST:
--   profile, streak, xpLog, qstats, ins.day / ins.att / ins.tl, ou = usage recorded by js/owner.js) · course_access ·
--   payments · plans · codes / code_uses · parent_links / parent_invites / parent_prefs / parent_challenges ·
--   institutions / inst_classes / institution_members / seat_orders / pilot_requests · room_players · squad_friends.
-- Dates: the app's day keys are UTC ISO dates (js/app.js today()), so day maths here is in UTC as well;
--   the time-of-day heatmap is shown in India time (Asia/Kolkata).
-- Filters (jsonb p, all optional): band ('1-5' | '6-8' | '9-10' | '11-12' | 'ca' | 'ca-foundation' | 'ca-inter' | 'ca-final'),
--   grade (1–12), status ('paid' | 'school' | 'free' | 'trial' | 'lapsed' | 'trial_ended' | 'none'), plan (plans.id),
--   board, inst (institution uuid), state (institution state), source ('self' | 'school' | 'parent' | 'code'), q (search).
-- Idempotent: safe to run again. Run after 20261110_squad.sql.
-- ============================================================================================

-- ---------- the owner's own follow-up marks ----------
create table if not exists studyverse.owner_followups (
  owner_id     uuid not null references auth.users(id) on delete cascade,
  item_key     text not null check (length(item_key) between 3 and 200),
  status       text not null default 'open' check (status in ('open', 'done', 'snoozed')),
  snooze_until timestamptz,
  note         text check (note is null or length(note) <= 1000),
  updated_at   timestamptz not null default now(),
  primary key (owner_id, item_key)
);
alter table studyverse.owner_followups enable row level security;     -- no policies: only through the functions below
revoke all on studyverse.owner_followups from anon, authenticated;
grant all on studyverse.owner_followups to service_role;

-- ---------- pure helpers ----------
-- These tiny helpers use only built-in pg_catalog functions and run for every day key / answer of every student, so they
-- have NO "set search_path" (a SET clause stops PostgreSQL from inlining them, which made the dashboards ~10× slower).
-- pg_catalog is always searched first, and they are not callable by app users (revoked below).
create or replace function studyverse._od_is_owner() returns boolean language sql stable security definer set search_path = '' as $$
  select auth.uid() is not null and exists (select 1 from studyverse.admins a where a.user_id = auth.uid()) $$;
create or replace function studyverse._od_today() returns date language sql stable as $$
  select (now() at time zone 'utc')::date $$;
create or replace function studyverse._od_n(v jsonb) returns numeric language sql immutable as $$
  select case when jsonb_typeof(v) = 'number' then (v #>> '{}')::numeric else 0 end $$;
-- 'YYYY-MM-DD' → date, or null for anything else (no exception block: this runs for every day key of every student)
create or replace function studyverse._od_date(p text) returns date language sql immutable as $$
  select case when p ~ '^20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
              and substr(p, 9, 2)::int <= extract(day from (substr(p, 1, 7) || '-01')::date + interval '1 month' - interval '1 day')
         then p::date end $$;
create or replace function studyverse._od_obj(v jsonb) returns jsonb language sql immutable as $$
  select case when jsonb_typeof(v) = 'object' then v else '{}'::jsonb end $$;
create or replace function studyverse._od_arr(v jsonb) returns jsonb language sql immutable as $$
  select case when jsonb_typeof(v) = 'array' then v else '[]'::jsonb end $$;
create or replace function studyverse._od_int(p text) returns int language sql immutable as $$
  select case when p ~ '^-?[0-9]{1,9}$' then p::int end $$;
create or replace function studyverse._od_uuid(p text) returns uuid language sql immutable as $$
  select case when p ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' then p::uuid end $$;
create or replace function studyverse._od_ts(d date) returns timestamptz language sql immutable as $$
  select (d::timestamp at time zone 'utc') $$;
-- day / week / month buckets so a chart never has hundreds of bars
create or replace function studyverse._od_bucket(f date, t date, b text) returns text language sql immutable as $$
  select case when b in ('day', 'week', 'month') then b when t - f <= 62 then 'day' when t - f <= 400 then 'week' else 'month' end $$;
create or replace function studyverse._od_band(kind text, grade int, lvl text) returns text language sql immutable as $$
  select case when kind = 'ca' then 'ca-' || coalesce(nullif(lvl, ''), 'foundation')
              when kind = 'school' and grade between 1 and 5 then '1-5' when kind = 'school' and grade between 6 and 8 then '6-8'
              when kind = 'school' and grade between 9 and 10 then '9-10' when kind = 'school' and grade between 11 and 12 then '11-12' end $$;

-- ---------- one row per student (parents and owners left out), with every filter applied ----------
create or replace function studyverse._od_users(p jsonb default '{}'::jsonb) returns table(
  user_id uuid, email text, name text, signup timestamptz, last_sign_in timestamptz, synced_at timestamptz,
  kind text, grade int, ca_level text, band text, board text,
  status text, plan_id text, plan text, valid_until timestamptz, trial_at timestamptz,
  inst_id uuid, inst_name text, class_name text, inst_state text, source text, n_parents int,
  last_active date, streak int, stars_week int, answered int, wrong int, n_paid int, paid_inr numeric)
language plpgsql stable security definer set search_path = '' as $$
#variable_conflict use_column
begin
  return query
  with base as (
    select u.id as user_id, u.email::text as email, u.created_at as signup, u.last_sign_in_at as last_sign_in, pr.updated_at as synced_at,
           x.prof, x.strk, x.xl, x.qs, x.dd, x.cal, pf.trial_at
    from auth.users u
    left join studyverse.profiles pf on pf.user_id = u.id
    left join studyverse.progress pr on pr.user_id = u.id
    -- read each part of the (large) saved state once
    left join lateral (select studyverse._od_obj(y.s -> 'profile') as prof, studyverse._od_obj(y.s -> 'streak') as strk, studyverse._od_obj(y.s -> 'xpLog') as xl,
                              studyverse._od_obj(y.s -> 'qstats') as qs, studyverse._od_obj(y.s #> '{ins,day}') as dd, y.s #>> '{ca,level}' as cal
                       from (select pr.state -> 'st' as s offset 0) y) x on true
    where coalesce(pf.role, 'student') <> 'parent'
      and not exists (select 1 from studyverse.admins a where a.user_id = u.id)
      and (studyverse._od_uuid(p ->> 'id') is null or u.id = studyverse._od_uuid(p ->> 'id'))
  ), f as (
    select b.*,
      case when b.prof ->> 'course' = 'ca' then 'ca' when b.prof <> '{}'::jsonb then 'school' else 'none' end as kind,
      studyverse._od_int(b.prof ->> 'grade') as g0,
      nullif(b.cal, '') as ca_level
    from base b
  ), g as (
    select f.*, case when f.kind = 'school' and f.g0 between 1 and 12 then f.g0 end as grade from f
  ), r as (
    select g.user_id, g.email, left(nullif(trim(g.prof ->> 'name'), ''), 60) as name, g.signup, g.last_sign_in, g.synced_at,
      g.kind, g.grade, case when g.kind = 'ca' then coalesce(g.ca_level, 'foundation') end as ca_level,
      studyverse._od_band(g.kind, g.grade, g.ca_level) as band, nullif(g.prof ->> 'board', '') as board,
      case when a.has_paid then 'paid' when a.has_school then 'school' when a.has_free then 'free' when a.has_trial then 'trial'
           when coalesce(a.ever_paid, false) or pay.n_paid > 0 then 'lapsed' when coalesce(a.n_rows, 0) > 0 then 'trial_ended' else 'none' end as status,
      lp.plan_id, coalesce(lp.label, case when a.has_school then 'School seat' end) as plan,
      case when a.has_paid then a.paid_until when a.has_school then a.school_until when a.has_free then a.free_until
           when a.has_trial then a.trial_until else a.any_until end as valid_until,
      g.trial_at, ins.inst_id, ins.inst_name, ins.class_name, ins.inst_state,
      case when ins.inst_id is not null then 'school'
           when exists (select 1 from studyverse.code_uses cu join studyverse.codes k on k.code = cu.code and k.kind = 'free' where cu.user_id = g.user_id) then 'code'
           when exists (select 1 from studyverse.parent_links pl join auth.users pu on pu.id = pl.parent_id where pl.child_id = g.user_id and pu.created_at <= g.signup) then 'parent'
           else 'self' end as source,
      (select count(*)::int from studyverse.parent_links pl where pl.child_id = g.user_id) as n_parents,
      la.d as last_active,
      case when studyverse._od_date(g.strk ->> 'last') >= studyverse._od_today() - 1 then coalesce(studyverse._od_int(g.strk ->> 'n'), 0) else 0 end as streak,
      coalesce((select sum(studyverse._od_n(e.value))::int from jsonb_each(g.xl) e
                where studyverse._od_date(e.key) >= date_trunc('week', studyverse._od_today())::date), 0) as stars_week,
      coalesce(qs.s, 0) as answered, coalesce(qs.w, 0) as wrong, coalesce(pay.n_paid, 0) as n_paid, coalesce(pay.inr, 0) as paid_inr
    from g
    left join lateral (
      select bool_or(c.act and c.note like 'paid%') as has_paid, bool_or(c.act and c.note like 'inst %') as has_school,
             bool_or(c.act and c.note not like 'paid%' and c.note not like 'inst %' and c.note <> 'trial') as has_free,
             bool_or(c.act and c.note = 'trial') as has_trial, bool_or(c.note like 'paid%') as ever_paid, count(*)::int as n_rows,
             max(c.until) filter (where c.act and c.note like 'paid%') as paid_until, max(c.until) filter (where c.act and c.note like 'inst %') as school_until,
             max(c.until) filter (where c.act and c.note not like 'paid%' and c.note not like 'inst %' and c.note <> 'trial') as free_until,
             max(c.until) filter (where c.act and c.note = 'trial') as trial_until, max(c.until) as any_until
      from (select coalesce(x.note, '') as note, x.valid_until as until, (x.valid_until is null or x.valid_until > now()) as act
            from studyverse.course_access x where x.user_id = g.user_id) c
    ) a on true
    left join lateral (
      select py.plan_id, pl.label from studyverse.payments py left join studyverse.plans pl on pl.id = py.plan_id
      where py.user_id = g.user_id and py.status = 'paid' order by py.paid_at desc nulls last limit 1
    ) lp on true
    left join lateral (
      select count(*)::int as n_paid, coalesce(sum(py.amount_paise), 0) / 100.0 as inr from studyverse.payments py
      where py.user_id = g.user_id and py.status = 'paid' and py.amount_paise > 0
    ) pay on true
    left join lateral (
      select im.institution_id as inst_id, i.name as inst_name, c.name as class_name, i.state as inst_state
      from studyverse.institution_members im join studyverse.institutions i on i.id = im.institution_id
      left join studyverse.inst_classes c on c.id = im.class_id
      where im.user_id = g.user_id and im.role = 'student' order by im.joined_at desc limit 1
    ) ins on true
    left join lateral (
      select max(z.d) as d from (
        select studyverse._od_date(k) as d from jsonb_object_keys(g.dd) k
        union all select studyverse._od_date(k) from jsonb_object_keys(g.xl) k
        union all select studyverse._od_date(g.strk ->> 'last')) z where z.d <= studyverse._od_today()
    ) la on true
    left join lateral (
      select sum(studyverse._od_n(e.value -> 's'))::int as s, sum(studyverse._od_n(e.value -> 'w'))::int as w
      from jsonb_each(g.qs) e
    ) qs on true
  )
  select r.* from r
  where (nullif(p ->> 'band', '') is null or r.band = p ->> 'band' or (p ->> 'band' = 'ca' and r.kind = 'ca'))
    and (studyverse._od_int(p ->> 'grade') is null or r.grade = studyverse._od_int(p ->> 'grade'))
    and (nullif(p ->> 'status', '') is null or r.status = p ->> 'status')
    and (nullif(p ->> 'plan', '') is null or r.plan_id = p ->> 'plan')
    and (nullif(p ->> 'board', '') is null or r.board = p ->> 'board')
    and (studyverse._od_uuid(p ->> 'inst') is null or r.inst_id = studyverse._od_uuid(p ->> 'inst'))
    and (nullif(p ->> 'state', '') is null or r.inst_state = p ->> 'state')
    and (nullif(p ->> 'source', '') is null or r.source = p ->> 'source')
    and (nullif(trim(p ->> 'q'), '') is null or r.email ilike '%' || trim(p ->> 'q') || '%' or r.name ilike '%' || trim(p ->> 'q') || '%')
;
end $$;

-- active days per student (union of insights days and the stars log): a = answers, r = right, secs = study time, xp = stars
create or replace function studyverse._od_days(ids uuid[]) returns table(user_id uuid, day date, a int, r int, secs int, xp int)
language sql stable security definer set search_path = '' as $$
  select pr.user_id, d.day, max(d.a)::int, max(d.r)::int, max(d.s)::int, max(d.x)::int
  from (select x.user_id, x.state from studyverse.progress x where x.user_id in (select unnest(ids)) offset 0) pr
  cross join lateral (select studyverse._od_obj(y.s #> '{ins,day}') as dd, studyverse._od_obj(y.s -> 'xpLog') as xl from (select pr.state -> 'st' as s offset 0) y) z
  cross join lateral (
    select studyverse._od_date(e.key) as day, studyverse._od_n(e.value -> 'a') as a, studyverse._od_n(e.value -> 'r') as r,
           studyverse._od_n(e.value -> 's') as s, studyverse._od_n(e.value -> 'x') as x
    from jsonb_each(z.dd) e
    union all
    select studyverse._od_date(e.key), 0, 0, 0, studyverse._od_n(e.value) from jsonb_each(z.xl) e
  ) d
  where d.day is not null and (d.a > 0 or d.s > 0 or d.x > 0)
  group by pr.user_id, d.day
$$;

-- recent answers [[epochMinute, qid, ok, conf], …] from ST.ins.att, between two timestamps
create or replace function studyverse._od_att(ids uuid[], f timestamptz, t timestamptz) returns table(user_id uuid, at timestamptz, qid text, ok int)
language sql stable security definer set search_path = '' as $$
  -- hot path (thousands of answers per student): plain expressions instead of the small helpers
  select y.user_id, to_timestamp(y.m * 60), y.q, y.o
  from (select pr.user_id, case when jsonb_typeof(x.v -> 0) = 'number' then (x.v ->> 0)::numeric end as m, x.v ->> 1 as q,
               case when x.v ->> 2 = '1' then 1 else 0 end as o, jsonb_typeof(x.v -> 1) as qt
        from (select x.user_id, x.state from studyverse.progress x where x.user_id in (select unnest(ids)) offset 0) pr
        cross join lateral (select pr.state #> '{st,ins,att}' as a offset 0) z
        cross join lateral jsonb_array_elements(case when jsonb_typeof(z.a) = 'array' then z.a else '[]'::jsonb end) as x(v)
        where jsonb_typeof(x.v) = 'array') y
  where y.qt = 'string' and y.m between extract(epoch from f) / 60 and extract(epoch from t) / 60
$$;

-- headline numbers for one period (used twice: this period and the one before)
create or replace function studyverse._od_kpis(ids uuid[], f date, t date) returns jsonb language sql stable security definer set search_path = '' as $$
  with act as (select d.user_id, d.day from studyverse._od_days(ids) d where d.day between least(f, t - 29) and t),
  pts as (select least(now(), studyverse._od_ts(t + 1)) as tp, studyverse._od_ts(f) as fs, least(now(), studyverse._od_ts(t + 1)) as te),
  pay as (select py.*, pl.months, row_number() over (partition by py.user_id order by py.paid_at) > 1 as is_renewal
          from studyverse.payments py left join studyverse.plans pl on pl.id = py.plan_id
          where py.user_id in (select unnest(ids)) and py.status = 'paid' and py.amount_paise > 0),
  cur as (select distinct on (pay.user_id) pay.* from pay, pts where pay.paid_at < pts.tp and pay.valid_until > pts.tp order by pay.user_id, pay.paid_at desc),
  firsts as (select pay.user_id, min(pay.paid_at) as first_at, max(pay.valid_until) as last_until from pay group by pay.user_id),
  tri as (select pf.user_id, exists (select 1 from pay where pay.user_id = pf.user_id) as paid from studyverse.profiles pf, pts
          where pf.user_id in (select unnest(ids)) and pf.trial_at >= pts.fs and pf.trial_at < pts.te)
  select jsonb_build_object(
    'from', f, 'to', t,
    'students', (select count(*) from auth.users u, pts where u.id in (select unnest(ids)) and u.created_at < pts.te),
    'signups', (select count(*) from auth.users u, pts where u.id in (select unnest(ids)) and u.created_at >= pts.fs and u.created_at < pts.te),
    'active', (select count(distinct a.user_id) from act a where a.day between f and t),
    'dau', (select count(distinct a.user_id) from act a where a.day = t),
    'wau', (select count(distinct a.user_id) from act a where a.day between t - 6 and t),
    'mau', (select count(distinct a.user_id) from act a where a.day between t - 29 and t),
    'avg_dau', round((select count(*) from act a where a.day between t - 29 and t) / 30.0, 1),
    'paying', (select count(*) from cur),
    'mrr', round(coalesce((select sum(cur.amount_paise / 100.0 / greatest(coalesce(cur.months, 1), 1)) from cur), 0)),
    'revenue', round(coalesce((select sum(pay.amount_paise) / 100.0 from pay, pts where pay.paid_at >= pts.fs and pay.paid_at < pts.te), 0)),
    'payments', (select count(*) from pay, pts where pay.paid_at >= pts.fs and pay.paid_at < pts.te),
    'new_paid', (select count(*) from firsts, pts where firsts.first_at >= pts.fs and firsts.first_at < pts.te),
    'renewed', (select count(*) from pay, pts where pay.paid_at >= pts.fs and pay.paid_at < pts.te and pay.is_renewal),
    'churned', (select count(*) from firsts, pts where firsts.last_until >= pts.fs and firsts.last_until < pts.te),
    'trials', (select count(*) from tri), 'trial_paid', (select count(*) from tri where tri.paid)
  ) $$;

-- ============================================================================================
-- RPCs (owner only)
-- ============================================================================================

-- filter choices for the dashboard's filter bar
create or replace function studyverse.owner_dash_meta() returns jsonb language plpgsql stable security definer set search_path = '' as $$
begin
  if not studyverse._od_is_owner() then return null; end if;
  return jsonb_build_object('ok', true, 'today', studyverse._od_today(), 'now', now(),
    'plans', coalesce((select jsonb_agg(jsonb_build_object('id', p.id, 'label', p.label, 'course', p.course, 'months', p.months, 'price', p.price_inr, 'active', p.active) order by p.sort, p.id) from studyverse.plans p), '[]'::jsonb),
    'boards', coalesce((select jsonb_agg(distinct x.b) from (select pr.state #>> '{st,profile,board}' as b from studyverse.progress pr) x where x.b is not null and x.b <> ''), '[]'::jsonb),
    'institutions', coalesce((select jsonb_agg(jsonb_build_object('id', i.id, 'name', i.name, 'type', i.type, 'state', i.state) order by i.name) from studyverse.institutions i), '[]'::jsonb),
    'states', coalesce((select jsonb_agg(distinct i.state) from studyverse.institutions i where i.state is not null and i.state <> ''), '[]'::jsonb));
end $$;

-- Overview: headline numbers now vs the previous period of the same length, status split, trend series
create or replace function studyverse.owner_dash_overview(p_from date, p_to date, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare ids uuid[]; f date := least(p_from, p_to); t date := greatest(p_from, p_to); n int; b text; res jsonb;
begin
  if not studyverse._od_is_owner() then return null; end if;
  if f is null or t is null or t - f > 3660 then return jsonb_build_object('ok', false, 'msg', 'Choose a date range of up to 10 years.'); end if;
  n := t - f + 1; b := studyverse._od_bucket(f, t, null);
  if to_regclass('pg_temp._od_u') is null then create temp table _od_u on commit drop as select * from studyverse._od_users('{}'::jsonb) limit 0; end if;
  truncate _od_u; insert into _od_u select * from studyverse._od_users(coalesce(p, '{}'::jsonb));
  select coalesce(array_agg(u.user_id), '{}') into ids from _od_u u;
  with days as (select * from studyverse._od_days(ids) d where d.day between f and t),
       bk as (select greatest(f, gs::date) as s, least(t, (gs + ('1 ' || b)::interval - interval '1 day')::date) as e
              from generate_series(date_trunc(b, f::timestamp), t::timestamp, ('1 ' || b)::interval) gs)
  select jsonb_build_object('ok', true, 'from', f, 'to', t, 'bucket', b,
    'cur', studyverse._od_kpis(ids, f, t), 'prev', studyverse._od_kpis(ids, f - n, f - 1),
    'status', coalesce((select jsonb_object_agg(x.status, x.c) from (select u.status, count(*) as c from _od_u u group by 1) x), '{}'::jsonb),
    'bands', coalesce((select jsonb_object_agg(coalesce(x.band, 'unknown'), x.c) from (select u.band, count(*) as c from _od_u u group by 1) x), '{}'::jsonb),
    'sources', coalesce((select jsonb_object_agg(x.source, x.c) from (select u.source, count(*) as c from _od_u u group by 1) x), '{}'::jsonb),
    'parents', (select count(*) from studyverse.profiles pf where pf.role = 'parent'),
    'parents_linked', (select count(distinct pl.parent_id) from studyverse.parent_links pl),
    'schools', (select count(*) from studyverse.institutions i where i.status in ('active', 'pilot')),
    'school_revenue', round(coalesce((select sum(o.taxable) from studyverse.seat_orders o where o.status = 'paid'
                       and o.paid_at >= studyverse._od_ts(f) and o.paid_at < studyverse._od_ts(t + 1)
                       and (studyverse._od_uuid(p ->> 'inst') is null or o.institution_id = studyverse._od_uuid(p ->> 'inst'))), 0)),
    'series', coalesce((select jsonb_agg(jsonb_build_object('d', bk.s,
        'active', (select count(distinct d.user_id) from days d where d.day between bk.s and bk.e),
        'signups', (select count(*) from _od_u u where (u.signup at time zone 'utc')::date between bk.s and bk.e),
        'answers', (select coalesce(sum(d.a), 0) from days d where d.day between bk.s and bk.e)) order by bk.s) from bk), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- Subscriptions: trend per bucket, by plan, by class band, retention cohorts, renewals due
create or replace function studyverse.owner_dash_subs(p_from date, p_to date, p_bucket text default null, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare ids uuid[]; f date := least(p_from, p_to); t date := greatest(p_from, p_to); b text; res jsonb; c0 date;
begin
  if not studyverse._od_is_owner() then return null; end if;
  if f is null or t is null or t - f > 3660 then return jsonb_build_object('ok', false, 'msg', 'Choose a date range of up to 10 years.'); end if;
  b := studyverse._od_bucket(f, t, p_bucket);
  if to_regclass('pg_temp._od_u') is null then create temp table _od_u on commit drop as select * from studyverse._od_users('{}'::jsonb) limit 0; end if;
  truncate _od_u; insert into _od_u select * from studyverse._od_users(coalesce(p, '{}'::jsonb));
  select coalesce(array_agg(u.user_id), '{}') into ids from _od_u u;
  c0 := (date_trunc('month', t::timestamp) - interval '11 months')::date;
  with pay as (select py.*, pl.label, pl.months from studyverse.payments py left join studyverse.plans pl on pl.id = py.plan_id where py.user_id in (select unnest(ids))),
       ok as (select pay.*, row_number() over (partition by pay.user_id order by pay.paid_at) > 1 as is_renewal from pay where pay.status = 'paid' and pay.amount_paise > 0),
       lastu as (select ok.user_id, max(ok.valid_until) as until from ok group by 1),
       firsts as (select ok.user_id, min(ok.paid_at) as first_at from ok group by 1),
       bk as (select greatest(f, gs::date) as s, least(t, (gs + ('1 ' || b)::interval - interval '1 day')::date) as e
              from generate_series(date_trunc(b, f::timestamp), t::timestamp, ('1 ' || b)::interval) gs),
       act as (select d.user_id, date_trunc('month', d.day)::date as m from studyverse._od_days(ids) d where d.day >= c0 group by 1, 2),
       coh as (select u.user_id, date_trunc('month', u.signup at time zone 'utc')::date as m from _od_u u where u.signup >= studyverse._od_ts(c0)),
       -- retention cells (signup month m, months after k): still active / still paying at the end of that month
       cact as (select coh.m, (extract(year from age(act.m, coh.m)) * 12 + extract(month from age(act.m, coh.m)))::int as k, count(distinct coh.user_id) as n
                from coh join act on act.user_id = coh.user_id and act.m >= coh.m group by 1, 2),
       cpay as (select coh.m, k, count(distinct coh.user_id) as n
                from coh join ok on ok.user_id = coh.user_id cross join lateral generate_series(0, 11) k
                where (coh.m + make_interval(months => k))::date <= t
                  and ok.paid_at < least(now(), studyverse._od_ts((coh.m + make_interval(months => k + 1))::date))
                  and ok.valid_until > least(now(), studyverse._od_ts((coh.m + make_interval(months => k + 1))::date)) group by 1, 2)
  select jsonb_build_object('ok', true, 'from', f, 'to', t, 'bucket', b,
    'series', coalesce((select jsonb_agg(jsonb_build_object('d', bk.s,
        'new', (select count(*) from firsts x where x.first_at >= studyverse._od_ts(bk.s) and x.first_at < studyverse._od_ts(bk.e + 1)),
        'renewed', (select count(*) from ok where ok.paid_at >= studyverse._od_ts(bk.s) and ok.paid_at < studyverse._od_ts(bk.e + 1) and ok.is_renewal),
        'expired', (select count(*) from lastu x where x.until >= studyverse._od_ts(bk.s) and x.until < least(now(), studyverse._od_ts(bk.e + 1))),
        'trials', (select count(*) from _od_u u where u.trial_at >= studyverse._od_ts(bk.s) and u.trial_at < studyverse._od_ts(bk.e + 1)),
        'failed', (select count(*) from pay where pay.status in ('failed', 'created') and pay.created_at < now() - interval '30 minutes'
                      and pay.created_at >= studyverse._od_ts(bk.s) and pay.created_at < studyverse._od_ts(bk.e + 1)),
        'revenue', round(coalesce((select sum(ok.amount_paise) / 100.0 from ok where ok.paid_at >= studyverse._od_ts(bk.s) and ok.paid_at < studyverse._od_ts(bk.e + 1)), 0))
      ) order by bk.s) from bk), '[]'::jsonb),
    'by_plan', coalesce((select jsonb_agg(x order by x.revenue desc, x.plan) from (
        select ok.plan_id as plan, max(ok.label) as label, count(*) as payments, round(sum(ok.amount_paise) / 100.0) as revenue,
               count(*) filter (where ok.valid_until > now()) as active_now
        from ok where ok.paid_at >= studyverse._od_ts(f) and ok.paid_at < studyverse._od_ts(t + 1) group by ok.plan_id) x), '[]'::jsonb),
    'by_band', coalesce((select jsonb_agg(x order by x.band) from (
        select coalesce(u.band, 'unknown') as band, count(*) as users, count(*) filter (where u.status = 'paid') as paid,
               count(*) filter (where u.status = 'school') as school, count(*) filter (where u.status = 'trial') as trial,
               count(*) filter (where u.status = 'free') as free, count(*) filter (where u.status in ('lapsed', 'trial_ended', 'none')) as not_paying
        from _od_u u group by 1) x), '[]'::jsonb),
    'cohorts', coalesce((select jsonb_agg(jsonb_build_object('m', cm.m, 'n', (select count(*) from coh where coh.m = cm.m),
        'act', (select jsonb_agg(coalesce((select cact.n from cact where cact.m = cm.m and cact.k = kk), 0) order by kk)
                from generate_series(0, (extract(year from age(date_trunc('month', t::timestamp), cm.m)) * 12 + extract(month from age(date_trunc('month', t::timestamp), cm.m)))::int) kk),
        'pay', (select jsonb_agg(coalesce((select cpay.n from cpay where cpay.m = cm.m and cpay.k = kk), 0) order by kk)
                from generate_series(0, (extract(year from age(date_trunc('month', t::timestamp), cm.m)) * 12 + extract(month from age(date_trunc('month', t::timestamp), cm.m)))::int) kk)
      ) order by cm.m) from (select gs::date as m from generate_series(c0::timestamp, date_trunc('month', t::timestamp), interval '1 month') gs) cm), '[]'::jsonb),
    'due7', (select count(*) from _od_u u where u.status = 'paid' and u.valid_until <= now() + interval '7 days'),
    'due30', (select count(*) from _od_u u where u.status = 'paid' and u.valid_until <= now() + interval '30 days'),
    'due', coalesce((select jsonb_agg(x order by x.valid_until) from (
        select u.user_id, u.email, u.name, u.band, u.plan, u.valid_until, u.last_active from _od_u u
        where u.status = 'paid' and u.valid_until <= now() + interval '30 days' order by u.valid_until limit 200) x), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- Students: one page of the table (search, filters, sort); p_limit up to 5000 for CSV export
create or replace function studyverse.owner_dash_students(p jsonb default '{}'::jsonb, p_sort text default 'last_active', p_desc boolean default true,
  p_limit int default 50, p_offset int default 0) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; lim int := least(greatest(coalesce(p_limit, 50), 1), 5000); off int := greatest(coalesce(p_offset, 0), 0);
  s text := case when p_sort in ('name', 'email', 'grade', 'band', 'board', 'status', 'plan', 'valid_until', 'signup', 'last_active', 'streak', 'stars_week', 'answered', 'accuracy', 'n_parents', 'inst_name', 'source', 'paid_inr') then p_sort else 'last_active' end;
begin
  if not studyverse._od_is_owner() then return null; end if;
  with u as (select x.*, case when x.answered > 0 then round(100.0 * (x.answered - x.wrong) / x.answered) end as accuracy
             from studyverse._od_users(coalesce(p, '{}'::jsonb)) x),
       o as (select u.*, row_number() over (order by
               case when not p_desc then case s when 'name' then lower(coalesce(u.name, u.email)) when 'email' then u.email when 'band' then u.band when 'board' then u.board
                 when 'status' then u.status when 'plan' then u.plan when 'inst_name' then u.inst_name when 'source' then u.source end end asc nulls last,
               case when p_desc then case s when 'name' then lower(coalesce(u.name, u.email)) when 'email' then u.email when 'band' then u.band when 'board' then u.board
                 when 'status' then u.status when 'plan' then u.plan when 'inst_name' then u.inst_name when 'source' then u.source end end desc nulls last,
               case when not p_desc then case s when 'grade' then u.grade::numeric when 'streak' then u.streak when 'stars_week' then u.stars_week when 'answered' then u.answered
                 when 'accuracy' then u.accuracy when 'n_parents' then u.n_parents when 'paid_inr' then u.paid_inr
                 when 'valid_until' then extract(epoch from u.valid_until) when 'signup' then extract(epoch from u.signup)
                 when 'last_active' then u.last_active - date '2000-01-01' end end asc nulls last,
               case when p_desc then case s when 'grade' then u.grade::numeric when 'streak' then u.streak when 'stars_week' then u.stars_week when 'answered' then u.answered
                 when 'accuracy' then u.accuracy when 'n_parents' then u.n_parents when 'paid_inr' then u.paid_inr
                 when 'valid_until' then extract(epoch from u.valid_until) when 'signup' then extract(epoch from u.signup)
                 when 'last_active' then u.last_active - date '2000-01-01' end end desc nulls last,
               u.email) as rn from u)
  select jsonb_build_object('ok', true, 'total', (select count(*) from o), 'sort', s, 'desc', p_desc, 'limit', lim, 'offset', off,
    'rows', coalesce((select jsonb_agg(jsonb_build_object('id', o.user_id, 'email', o.email, 'name', o.name, 'kind', o.kind, 'grade', o.grade, 'ca_level', o.ca_level,
        'band', o.band, 'board', o.board, 'status', o.status, 'plan', o.plan, 'plan_id', o.plan_id, 'valid_until', o.valid_until, 'signup', o.signup,
        'last_active', o.last_active, 'streak', o.streak, 'stars_week', o.stars_week, 'answered', o.answered, 'accuracy', o.accuracy,
        'n_paid', o.n_paid, 'paid_inr', o.paid_inr, 'source', o.source, 'inst_name', o.inst_name, 'class_name', o.class_name, 'n_parents', o.n_parents,
        'parents', (select string_agg(pu.email, ', ' order by pu.email) from studyverse.parent_links pl join auth.users pu on pu.id = pl.parent_id where pl.child_id = o.user_id))
      order by o.rn) from o where o.rn > off and o.rn <= off + lim), '[]'::jsonb)) into res;
  return res;
end $$;

-- One student, everything the owner may need to help them
create or replace function studyverse.owner_dash_student(p_user uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; st jsonb; t date := studyverse._od_today();
begin
  if not studyverse._od_is_owner() then return null; end if;
  select studyverse._od_obj(pr.state -> 'st') into st from studyverse.progress pr where pr.user_id = p_user;
  st := coalesce(st, '{}'::jsonb);
  select jsonb_build_object('ok', true,
    'user', (select to_jsonb(u) from studyverse._od_users(jsonb_build_object('id', p_user)) u),
    'role', (select pf.role from studyverse.profiles pf where pf.user_id = p_user),
    'access', coalesce((select jsonb_agg(jsonb_build_object('course', c.course, 'valid_until', c.valid_until, 'note', c.note, 'granted_at', c.granted_at) order by c.granted_at desc nulls last)
               from studyverse.course_access c where c.user_id = p_user), '[]'::jsonb),
    'payments', coalesce((select jsonb_agg(jsonb_build_object('plan', py.plan_id, 'label', pl.label, 'inr', py.amount_paise / 100.0, 'code', py.discount_code, 'percent', py.percent,
               'status', py.status, 'created_at', py.created_at, 'paid_at', py.paid_at, 'valid_until', py.valid_until) order by py.created_at desc)
               from studyverse.payments py left join studyverse.plans pl on pl.id = py.plan_id where py.user_id = p_user), '[]'::jsonb),
    'parents', coalesce((select jsonb_agg(jsonb_build_object('email', pu.email, 'linked_at', pl.created_at, 'last_sign_in', pu.last_sign_in_at,
               'weekly_email', coalesce(pp.weekly_email, true),
               'challenges', (select count(*) from studyverse.parent_challenges c where c.parent_id = pl.parent_id and c.child_id = p_user)) order by pl.created_at)
               from studyverse.parent_links pl join auth.users pu on pu.id = pl.parent_id left join studyverse.parent_prefs pp on pp.parent_id = pl.parent_id
               where pl.child_id = p_user), '[]'::jsonb),
    'codes', coalesce((select jsonb_agg(jsonb_build_object('code', cu.code, 'kind', k.kind, 'course', cu.course, 'used_at', cu.used_at)) from studyverse.code_uses cu
               left join studyverse.codes k on k.code = cu.code where cu.user_id = p_user), '[]'::jsonb),
    'school', (select jsonb_build_object('id', i.id, 'name', i.name, 'type', i.type, 'class', c.name, 'joined_at', im.joined_at)
               from studyverse.institution_members im join studyverse.institutions i on i.id = im.institution_id left join studyverse.inst_classes c on c.id = im.class_id
               where im.user_id = p_user and im.role = 'student' order by im.joined_at desc limit 1),
    'days', coalesce((select jsonb_agg(jsonb_build_object('d', d.day, 'a', d.a, 'r', d.r, 's', d.secs, 'x', d.xp) order by d.day)
               from studyverse._od_days(array[p_user]) d where d.day > t - 90), '[]'::jsonb),
    'subjects', coalesce((select jsonb_agg(x order by x.answered desc) from (
               select z.subj, sum(z.s)::int as answered, sum(z.w)::int as wrong, count(distinct z.topic)::int as topics
               from (select substring(e.key from '^(g[0-9]+-[a-z]+)-') as subj, split_part(e.key, '#', 1) as topic,
                            studyverse._od_n(e.value -> 's') as s, studyverse._od_n(e.value -> 'w') as w from jsonb_each(studyverse._od_obj(st -> 'qstats')) e) z
               where z.subj is not null group by z.subj) x), '[]'::jsonb),
    'topics_done', coalesce((select jsonb_object_agg(x.subj, x.n) from (select substring(e.key from '^(g[0-9]+-[a-z]+)-') as subj, count(*) as n
               from jsonb_each(studyverse._od_obj(st -> 'topics')) e where studyverse._od_n(e.value -> 'stars') > 0 group by 1) x where x.subj is not null), '{}'::jsonb),
    'weak', coalesce((select jsonb_agg(x order by x.acc, x.answered desc) from (
               select split_part(e.key, '#', 1) as topic, sum(studyverse._od_n(e.value -> 's'))::int as answered,
                      round(100 - 100.0 * sum(studyverse._od_n(e.value -> 'w')) / nullif(sum(studyverse._od_n(e.value -> 's')), 0)) as acc
               from jsonb_each(studyverse._od_obj(st -> 'qstats')) e group by 1 having sum(studyverse._od_n(e.value -> 's')) >= 4
               order by 3, 2 desc limit 8) x where x.acc < 70), '[]'::jsonb),
    'tests', coalesce((select jsonb_agg(x.v order by x.i desc) from (select v, i from jsonb_array_elements(studyverse._od_arr(st #> '{ins,tl}')) with ordinality as e(v, i)
               order by i desc limit 15) x), '[]'::jsonb),
    'usage', coalesce((select jsonb_object_agg(x.k, x.n) from (select fe.key as k, sum(studyverse._od_n(fe.value))::int as n
               from jsonb_each(studyverse._od_obj(st #> '{ou,d}')) dd cross join lateral jsonb_each(studyverse._od_obj(dd.value)) fe
               where studyverse._od_date(dd.key) > t - 30 group by 1) x), '{}'::jsonb),
    'device', studyverse._od_obj(st #> '{ou,dev}'),
    'live_games', (select count(*) from studyverse.room_players rp where rp.user_id = p_user),
    'friends', (select count(*) from studyverse.squad_friends sf where (sf.a = p_user or sf.b = p_user) and sf.status = 'accepted'),
    'xp', studyverse._od_n(st -> 'xp'), 'best_streak', studyverse._od_n(st #> '{streak,n}'), 'streak_last', st #>> '{streak,last}'
  ) into res;
  if res -> 'user' is null or res -> 'user' = 'null'::jsonb then return jsonb_build_object('ok', false, 'msg', 'Student not found.'); end if;
  return res;
end $$;

-- Usage & content: features, drop-off, hardest questions, subjects and chapters, time of day
create or replace function studyverse.owner_dash_usage(p_from date, p_to date, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare ids uuid[]; f date := least(p_from, p_to); t date := greatest(p_from, p_to); res jsonb; fs timestamptz; te timestamptz;
begin
  if not studyverse._od_is_owner() then return null; end if;
  if f is null or t is null or t - f > 3660 then return jsonb_build_object('ok', false, 'msg', 'Choose a date range of up to 10 years.'); end if;
  fs := studyverse._od_ts(f); te := studyverse._od_ts(t + 1);
  select coalesce(array_agg(u.user_id), '{}') into ids from studyverse._od_users(coalesce(p, '{}'::jsonb)) u;
  if to_regclass('pg_temp._od_a') is null then create temp table _od_a on commit drop as select * from studyverse._od_att('{}'::uuid[], now(), now()) limit 0; end if;
  truncate _od_a; insert into _od_a select * from studyverse._od_att(ids, fs, te);
  with pr as materialized (select x.user_id, y.ou_d, y.ou_x, y.ou_t, y.dd, y.story, y.exam, y.calc, y.gk
              from studyverse.progress x cross join lateral (select studyverse._od_obj(z.s #> '{ou,d}') as ou_d, studyverse._od_obj(z.s #> '{ou,x}') as ou_x,
                studyverse._od_obj(z.s #> '{ou,t}') as ou_t, studyverse._od_obj(z.s #> '{ins,day}') as dd, studyverse._od_obj(z.s -> 'story') <> '{}'::jsonb as story,
                studyverse._od_obj(z.s -> 'examPlan') <> '{}'::jsonb as exam, studyverse._od_obj(z.s #> '{calcAcad,m}') <> '{}'::jsonb as calc,
                studyverse._od_obj(z.s #> '{gk,seen}') <> '{}'::jsonb as gk from (select x.state -> 'st' as s offset 0) z) y
              where x.user_id in (select unnest(ids))),
       fu as (select pr.user_id, fe.key as k, studyverse._od_n(fe.value) as n from pr
              cross join lateral jsonb_each(pr.ou_d) dd cross join lateral jsonb_each(studyverse._od_obj(dd.value)) fe
              where studyverse._od_date(dd.key) between f and t),
       dx as (select fe.key as k, studyverse._od_n(fe.value) as n from pr
              cross join lateral jsonb_each(pr.ou_x) dd cross join lateral jsonb_each(studyverse._od_obj(dd.value)) fe
              where studyverse._od_date(dd.key) between f and t),
       tp as (select fe.key as topic, studyverse._od_n(fe.value -> 0) as starts, studyverse._od_n(fe.value -> 1) as done, pr.user_id from pr
              cross join lateral jsonb_each(pr.ou_t) fe where jsonb_typeof(fe.value) = 'array'),
       sj as (select pr.user_id, se.key as sid, studyverse._od_n(se.value -> 0) as a, studyverse._od_n(se.value -> 1) as r, studyverse._od_n(se.value -> 2) as s from pr
              cross join lateral jsonb_each(pr.dd) dd cross join lateral jsonb_each(studyverse._od_obj(dd.value -> 'sj')) se
              where studyverse._od_date(dd.key) between f and t and jsonb_typeof(se.value) = 'array')
  select jsonb_build_object('ok', true, 'from', f, 'to', t,
    'students', coalesce(array_length(ids, 1), 0),
    'active', (select count(distinct d.user_id) from studyverse._od_days(ids) d where d.day between f and t),
    'tracked_users', (select count(*) from (select fu.user_id from fu group by 1) z),
    'features', coalesce((select jsonb_agg(jsonb_build_object('k', x.k, 'users', x.users, 'opens', x.opens) order by x.users desc, x.opens desc)
                 from (select z.k, count(*) as users, sum(z.n)::int as opens from (select fu.k, fu.user_id, sum(fu.n) as n from fu group by 1, 2) z group by z.k) x), '[]'::jsonb),
    'derived', jsonb_build_object(
       'live', (select count(distinct rp.user_id) from studyverse.room_players rp where rp.user_id in (select unnest(ids)) and rp.joined_at >= fs and rp.joined_at < te),
       'story', (select count(*) from pr where pr.story),
       'exam', (select count(*) from pr where pr.exam),
       'calc', (select count(*) from pr where pr.calc),
       'gk', (select count(*) from pr where pr.gk),
       'friends', (select count(distinct x.u) from (select sf.a as u from studyverse.squad_friends sf where sf.status = 'accepted' union all
                    select sf.b from studyverse.squad_friends sf where sf.status = 'accepted') x where x.u in (select unnest(ids))),
       'challenges', (select count(distinct c.child_id) from studyverse.parent_challenges c where c.child_id in (select unnest(ids)) and c.created_at >= fs and c.created_at < te)),
    'drop_steps', coalesce((select jsonb_object_agg(x.k, x.n) from (select dx.k, sum(dx.n)::int as n from dx group by 1) x), '{}'::jsonb),
    'drop_topics', coalesce((select jsonb_agg(x order by x.left_n desc, x.starts desc) from (
                   select tp.topic, sum(tp.starts)::int as starts, sum(tp.done)::int as done, sum(greatest(tp.starts - tp.done, 0))::int as left_n, count(distinct tp.user_id) as users
                   from tp group by tp.topic having sum(tp.starts) >= 2 order by 4 desc, 2 desc limit 15) x), '[]'::jsonb),
    'hard', coalesce((select jsonb_agg(x order by x.acc, x.tries desc) from (
                   select a.qid, count(*) as tries, count(distinct a.user_id) as users, round(100.0 * sum(a.ok) / count(*)) as acc
                   from _od_a a group by a.qid having count(*) >= 5 order by 4, 2 desc limit 20) x), '[]'::jsonb),
    'answers', (select count(*) from _od_a), 'right', (select coalesce(sum(a.ok), 0) from _od_a a),
    'subjects', coalesce((select jsonb_agg(x order by x.answers desc) from (
                   select sj.sid, sum(sj.a)::int as answers, sum(sj.r)::int as right_n, sum(sj.s)::int as secs, count(distinct sj.user_id) as users
                   from sj group by sj.sid) x), '[]'::jsonb),
    'chapters', coalesce((select jsonb_agg(x order by x.answers desc) from (
                   select coalesce(substring(a.qid from '^(g[0-9]+-[a-z]+-[0-9]+)-'), split_part(a.qid, '#', 1)) as ch, count(*) as answers,
                          count(distinct a.user_id) as users, round(100.0 * sum(a.ok) / count(*)) as acc
                   from _od_a a group by 1 order by 2 desc limit 40) x), '[]'::jsonb),
    'hours', coalesce((select jsonb_agg(jsonb_build_array(x.dow, x.h, x.n)) from (
                   select extract(isodow from a.at at time zone 'Asia/Kolkata')::int as dow, extract(hour from a.at at time zone 'Asia/Kolkata')::int as h, count(*) as n
                   from _od_a a group by 1, 2) x), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- Parents: totals and a page of the list
create or replace function studyverse.owner_dash_parents(p_from date, p_to date, p_q text default null, p_limit int default 50, p_offset int default 0) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; f date := least(p_from, p_to); t date := greatest(p_from, p_to); lim int := least(greatest(coalesce(p_limit, 50), 1), 5000);
begin
  if not studyverse._od_is_owner() then return null; end if;
  with par as (
    select u.id, u.email::text as email, u.created_at, u.last_sign_in_at,
      (select count(*) from studyverse.parent_links pl where pl.parent_id = u.id) as kids,
      (select string_agg(left(coalesce(pl.child_name, 'Child'), 30), ', ' order by pl.created_at) from studyverse.parent_links pl where pl.parent_id = u.id) as kid_names,
      (select jsonb_agg(jsonb_build_object('id', pl.child_id, 'name', left(coalesce(pl.child_name, 'Child'), 30)) order by pl.created_at) from studyverse.parent_links pl where pl.parent_id = u.id) as kid_list,
      (select min(pl.created_at) from studyverse.parent_links pl where pl.parent_id = u.id) as linked_at,
      (select count(*) from studyverse.parent_invites pi where pi.parent_id = u.id and pi.accepted_at is null and pi.expires_at > now()) as pending,
      (select count(*) from studyverse.parent_challenges c where c.parent_id = u.id and c.created_at >= studyverse._od_ts(f) and c.created_at < studyverse._od_ts(t + 1)) as challenges,
      coalesce((select pp.weekly_email from studyverse.parent_prefs pp where pp.parent_id = u.id), true) as weekly,
      exists (select 1 from studyverse.parent_links pl join studyverse.course_access c on c.user_id = pl.child_id and c.note like 'paid%' and c.valid_until > now() where pl.parent_id = u.id) as kid_paid
    from auth.users u join studyverse.profiles pf on pf.user_id = u.id and pf.role = 'parent'
  )
  select jsonb_build_object('ok', true,
    'total', (select count(*) from par), 'linked', (select count(*) from par where par.kids > 0),
    'kids', (select count(distinct pl.child_id) from studyverse.parent_links pl),
    'seen7', (select count(*) from par where par.last_sign_in_at > now() - interval '7 days'),
    'seen30', (select count(*) from par where par.last_sign_in_at > now() - interval '30 days'),
    'idle', (select count(*) from par where par.kids > 0 and (par.last_sign_in_at is null or par.last_sign_in_at < now() - interval '14 days')),
    'weekly_on', (select count(*) from par where par.weekly), 'pending_invites', (select coalesce(sum(par.pending), 0) from par),
    'challenges', (select coalesce(sum(par.challenges), 0) from par), 'kid_paid', (select count(*) from par where par.kid_paid),
    'new', (select count(*) from par where par.created_at >= studyverse._od_ts(f) and par.created_at < studyverse._od_ts(t + 1)),
    'rows', coalesce((select jsonb_agg(to_jsonb(x) order by x.last_sign_in_at desc nulls last) from (
        select par.* from par where nullif(trim(p_q), '') is null or par.email ilike '%' || trim(p_q) || '%' or par.kid_names ilike '%' || trim(p_q) || '%'
        order by par.last_sign_in_at desc nulls last, par.email limit lim offset greatest(coalesce(p_offset, 0), 0)) x), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- Schools & coaching: one row per institution (seats bought / used, active %, orders, pilot), plus pilot→paid
create or replace function studyverse.owner_dash_institutions(p jsonb default '{}'::jsonb) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; t date := studyverse._od_today();
begin
  if not studyverse._od_is_owner() then return null; end if;
  with i as (select x.* from studyverse.institutions x
             where (nullif(p ->> 'state', '') is null or x.state = p ->> 'state') and (studyverse._od_uuid(p ->> 'inst') is null or x.id = studyverse._od_uuid(p ->> 'inst'))),
       m as (select im.institution_id, array_agg(im.user_id) as ids, count(*) as n from studyverse.institution_members im where im.role = 'student' group by 1),
       rows as (
         select i.id, i.name, i.type, i.city, i.state, i.board, i.status, i.pilot_until, i.created_at, i.contact_name, i.contact_email, i.contact_phone,
           coalesce(m.n, 0) as students,
           (select count(distinct d.user_id) from studyverse._od_days(coalesce(m.ids, '{}')) d where d.day > t - 7) as active7,
           (select coalesce(sum(o.students), 0) from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid' and o.valid_until > now()) as seats,
           (select count(*) from studyverse.seat_orders o where o.institution_id = i.id and o.status <> 'cancelled') as orders,
           (select count(*) from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'invoiced') as unpaid,
           (select round(coalesce(sum(o.taxable), 0)) from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid') as revenue,
           (select max(o.valid_until) from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid') as paid_until,
           (select count(*) from studyverse.institution_members im where im.institution_id = i.id and im.role = 'teacher') as teachers,
           (select count(*) from studyverse.inst_classes c where c.institution_id = i.id) as classes,
           (i.pilot_until is not null or exists (select 1 from studyverse.inst_grants g where g.institution_id = i.id and g.pilot)) as had_pilot,
           exists (select 1 from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid') as paid
         from i left join m on m.institution_id = i.id)
  select jsonb_build_object('ok', true,
    'total', (select count(*) from rows), 'schools', (select count(*) from rows where rows.type = 'school'), 'coaching', (select count(*) from rows where rows.type = 'coaching'),
    'pilots_now', (select count(*) from rows where rows.status = 'pilot' and rows.pilot_until > now()),
    'had_pilot', (select count(*) from rows where rows.had_pilot), 'pilot_paid', (select count(*) from rows where rows.had_pilot and rows.paid),
    'seats', (select coalesce(sum(rows.seats), 0) from rows), 'students', (select coalesce(sum(rows.students), 0) from rows),
    'active7', (select coalesce(sum(rows.active7), 0) from rows), 'revenue', (select coalesce(sum(rows.revenue), 0) from rows),
    'requests', (select count(*) from studyverse.pilot_requests pr where pr.created_at > now() - interval '30 days'),
    'request_rows', coalesce((select jsonb_agg(jsonb_build_object('id', pr.id, 'name', pr.name, 'school', pr.school, 'city', pr.city, 'phone', pr.phone, 'email', pr.email,
                       'students', pr.students, 'created_at', pr.created_at) order by pr.created_at desc)
                     from studyverse.pilot_requests pr where pr.created_at > now() - interval '90 days'), '[]'::jsonb),
    'rows', coalesce((select jsonb_agg(to_jsonb(rows) order by rows.name) from rows), '[]'::jsonb)) into res;
  return res;
end $$;

-- One institution: classes with activity, orders, students
create or replace function studyverse.owner_dash_institution(p_inst uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; t date := studyverse._od_today();
begin
  if not studyverse._od_is_owner() then return null; end if;
  if not exists (select 1 from studyverse.institutions i where i.id = p_inst) then return jsonb_build_object('ok', false, 'msg', 'Institution not found.'); end if;
  with s as (select u.* from studyverse._od_users(jsonb_build_object('inst', p_inst)) u),
       d as (select * from studyverse._od_days(coalesce((select array_agg(s.user_id) from s), '{}')) d where d.day > t - 30)
  select jsonb_build_object('ok', true,
    'inst', (select to_jsonb(i) - 'gstin' - 'address' - 'pincode' - 'created_by' from studyverse.institutions i where i.id = p_inst),
    'classes', coalesce((select jsonb_agg(jsonb_build_object('id', c.id, 'name', c.name, 'course', c.course,
        'students', (select count(*) from studyverse.institution_members im where im.class_id = c.id and im.role = 'student'),
        'active7', (select count(distinct d.user_id) from d join studyverse.institution_members im on im.user_id = d.user_id and im.class_id = c.id and im.role = 'student' where d.day > t - 7),
        'answers30', (select coalesce(sum(d.a), 0) from d join studyverse.institution_members im on im.user_id = d.user_id and im.class_id = c.id and im.role = 'student'),
        'right30', (select coalesce(sum(d.r), 0) from d join studyverse.institution_members im on im.user_id = d.user_id and im.class_id = c.id and im.role = 'student'),
        'homework', (select count(*) from studyverse.homework h where h.class_id = c.id)) order by c.course, c.section)
      from studyverse.inst_classes c where c.institution_id = p_inst), '[]'::jsonb),
    'orders', coalesce((select jsonb_agg(jsonb_build_object('id', o.id, 'students', o.students, 'taxable', o.taxable, 'total', o.total, 'status', o.status, 'year', o.academic_year,
        'valid_until', o.valid_until, 'invoice_no', o.invoice_no, 'created_at', o.created_at, 'paid_at', o.paid_at) order by o.created_at desc)
      from studyverse.seat_orders o where o.institution_id = p_inst), '[]'::jsonb),
    'teachers', (select count(*) from studyverse.institution_members im where im.institution_id = p_inst and im.role = 'teacher'),
    'admins', coalesce((select jsonb_agg(u.email) from studyverse.institution_members im join auth.users u on u.id = im.user_id where im.institution_id = p_inst and im.role = 'admin'), '[]'::jsonb),
    'days', coalesce((select jsonb_agg(jsonb_build_object('d', x.day, 'users', x.n, 'a', x.a) order by x.day) from (select d.day, count(distinct d.user_id) as n, sum(d.a) as a from d group by 1) x), '[]'::jsonb),
    'students', coalesce((select jsonb_agg(jsonb_build_object('id', s.user_id, 'name', s.name, 'email', s.email, 'class_name', s.class_name, 'last_active', s.last_active,
        'answered', s.answered, 'accuracy', case when s.answered > 0 then round(100.0 * (s.answered - s.wrong) / s.answered) end, 'streak', s.streak, 'status', s.status)
        order by s.last_active desc nulls last) from s), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- 🧠 Smart Manager: today's prioritised follow-ups, computed from fixed rules (no outside AI), with the owner's marks
create or replace function studyverse.owner_dash_smart(p jsonb default '{}'::jsonb) returns jsonb language plpgsql volatile security definer set search_path = '' as $$
declare res jsonb; ids uuid[]; t date := studyverse._od_today(); me uuid := auth.uid();
begin
  if not studyverse._od_is_owner() then return null; end if;
  if to_regclass('pg_temp._od_u') is null then create temp table _od_u on commit drop as select * from studyverse._od_users('{}'::jsonb) limit 0; end if;
  truncate _od_u; insert into _od_u select * from studyverse._od_users(coalesce(p, '{}'::jsonb));
  select coalesce(array_agg(u.user_id), '{}') into ids from _od_u u;
  if to_regclass('pg_temp._od_a') is null then create temp table _od_a on commit drop as select * from studyverse._od_att('{}'::uuid[], now(), now()) limit 0; end if;
  truncate _od_a; insert into _od_a select * from studyverse._od_att(ids, now() - interval '30 days', now());
  with d14 as (select d.* from studyverse._od_days(ids) d where d.day > t - 14),
    pp as materialized (select x.user_id, studyverse._od_obj(y.s #> '{ou,d}') as ou_d, studyverse._od_obj(y.s #> '{ou,x}') as ou_x, studyverse._od_obj(y.s #> '{ou,t}') as ou_t,
           studyverse._od_obj(y.s -> 'streak') as strk
           from (select x0.user_id, x0.state from studyverse.progress x0 where x0.user_id in (select uu.user_id from _od_u uu) offset 0) x
           cross join lateral (select x.state -> 'st' as s offset 0) y),
    wk as (select d14.user_id, count(*) filter (where d14.day > t - 7) as now7, count(*) filter (where d14.day <= t - 7) as prev7,
                  sum(d14.a) filter (where d14.day > t - 7) as a7, sum(d14.r) filter (where d14.day > t - 7) as r7 from d14 group by 1),
    par as (select pl.child_id, string_agg(pu.email, ',' order by pl.created_at) as emails from studyverse.parent_links pl join auth.users pu on pu.id = pl.parent_id group by 1),
    ia as materialized (select im.institution_id, count(distinct d.user_id) as n
           from studyverse._od_days(coalesce((select array_agg(im2.user_id) from studyverse.institution_members im2 where im2.role = 'student'), '{}')) d
           join studyverse.institution_members im on im.user_id = d.user_id and im.role = 'student' where d.day > t - 7 group by 1),
    iu as materialized (select i.*, (select count(*) from studyverse.institution_members im where im.institution_id = i.id and im.role = 'student') as students,
           (select coalesce(sum(o.students), 0) from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid' and o.valid_until > now()) as seats,
           coalesce((select ia.n from ia where ia.institution_id = i.id), 0) as active7
           from studyverse.institutions i where i.status in ('active', 'pilot')),
    stu as (select u.*, par.emails as parent_emails, wk.now7, wk.prev7, wk.a7, wk.r7 from _od_u u left join par on par.child_id = u.user_id left join wk on wk.user_id = u.user_id),
    items as (
      -- students
      select 'trial:' || s.user_id || ':' || to_char(s.valid_until, 'YYYYMMDD') as key, 'trial_end' as kind, 1 as pri, 'student' as who_kind, s.user_id::text as who_id,
             s.email, s.name, s.parent_emails, null::text as phone, s.band, s.valid_until as due, null::jsonb as meta
        from stu s where s.status = 'trial' and s.valid_until <= now() + interval '24 hours'
      union all
      select 'renew:' || s.user_id || ':' || to_char(s.valid_until, 'YYYYMMDD'), 'expiring', case when s.valid_until <= now() + interval '3 days' then 1 else 2 end, 'student', s.user_id::text,
             s.email, s.name, s.parent_emails, null, s.band, s.valid_until, jsonb_build_object('plan', s.plan)
        from stu s where s.status = 'paid' and s.valid_until <= now() + interval '7 days'
      union all
      select 'lapsed:' || s.user_id || ':' || to_char(s.valid_until, 'YYYYMMDD'), 'lapsed', 2, 'student', s.user_id::text, s.email, s.name, s.parent_emails, null, s.band, s.valid_until,
             jsonb_build_object('plan', s.plan)
        from stu s where s.status = 'lapsed' and s.valid_until > now() - interval '14 days'
      union all
      select 'idle:' || s.user_id || ':' || coalesce(s.last_active::text, 'never'), 'paid_idle', 2, 'student', s.user_id::text, s.email, s.name, s.parent_emails, null, s.band, null,
             jsonb_build_object('last_active', s.last_active, 'days', t - s.last_active, 'plan', s.plan)
        from stu s where s.status in ('paid', 'school') and (s.last_active is null or s.last_active <= t - 5)
      union all
      select 'falling:' || s.user_id || ':' || to_char(t, 'IYYYIW'), 'falling', 2, 'student', s.user_id::text, s.email, s.name, s.parent_emails, null, s.band, null,
             jsonb_build_object('now7', s.now7, 'prev7', s.prev7)
        from stu s where coalesce(s.prev7, 0) >= 4 and coalesce(s.now7, 0) * 2 < s.prev7 and s.status in ('paid', 'school', 'trial', 'free')
          and not (s.status in ('paid', 'school') and (s.last_active is null or s.last_active <= t - 5))
      union all
      select 'streak:' || s.user_id || ':' || (s.st_last)::text, 'streak_broken', 3, 'student', s.user_id::text, s.email, s.name, s.parent_emails, null, s.band, null,
             jsonb_build_object('streak', s.st_n)
        from (select stu.*, studyverse._od_date(pp.strk ->> 'last') as st_last, studyverse._od_int(pp.strk ->> 'n') as st_n
              from stu join pp on pp.user_id = stu.user_id) s
        where s.st_n >= 5 and s.st_last = t - 2
      union all
      select 'frustrated:' || s.user_id || ':' || to_char(t, 'IYYYIW'), 'frustrated', 2, 'student', s.user_id::text, s.email, s.name, s.parent_emails, null, s.band, null,
             jsonb_build_object('answers', s.a7, 'acc', round(100.0 * s.r7 / nullif(s.a7, 0)))
        from stu s where coalesce(s.a7, 0) >= 20 and s.r7 * 100 < s.a7 * 45
      union all
      select 'pay:' || py.id, 'pay_failed', 1, 'student', py.user_id::text, s.email, s.name, s.parent_emails, null, s.band, py.created_at,
             jsonb_build_object('plan', pl.label, 'inr', py.amount_paise / 100.0, 'status', py.status)
        from studyverse.payments py join stu s on s.user_id = py.user_id left join studyverse.plans pl on pl.id = py.plan_id
        where py.status in ('failed', 'created') and py.created_at > now() - interval '7 days' and py.created_at < now() - interval '30 minutes'
          and not exists (select 1 from studyverse.payments p2 where p2.user_id = py.user_id and p2.status = 'paid' and p2.created_at >= py.created_at)
          and py.id = (select max(p3.id) from studyverse.payments p3 where p3.user_id = py.user_id and p3.status in ('failed', 'created'))
      union all
      -- parents
      select 'parent:' || pu.id || ':' || to_char(t, 'IYYYIW'), 'parent_idle', 3, 'parent', pu.id::text, pu.email::text, null,
             null, null, null, pu.last_sign_in_at, jsonb_build_object('kids', (select string_agg(left(coalesce(pl.child_name, 'Child'), 30), ', ') from studyverse.parent_links pl where pl.parent_id = pu.id))
        from auth.users pu join studyverse.profiles pf on pf.user_id = pu.id and pf.role = 'parent'
        where exists (select 1 from studyverse.parent_links pl join _od_u uu on uu.user_id = pl.child_id where pl.parent_id = pu.id)
          and (pu.last_sign_in_at is null or pu.last_sign_in_at < now() - interval '14 days')
      union all
      select 'pinvite:' || pi.id, 'parent_invite', 3, 'parent', pi.parent_id::text, pu.email::text, null, null, null, null, pi.created_at,
             jsonb_build_object('child', left(coalesce(pi.child_name, ''), 30))
        from studyverse.parent_invites pi join auth.users pu on pu.id = pi.parent_id
        where pi.accepted_at is null and pi.expires_at > now() and pi.created_at < now() - interval '3 days'
      union all
      -- schools & coaching
      select 'pilotend:' || i.id || ':' || to_char(i.pilot_until, 'YYYYMMDD'), 'pilot_ending', 1, 'school', i.id::text, i.contact_email, i.name, null, i.contact_phone, null, i.pilot_until,
             jsonb_build_object('contact', i.contact_name, 'type', i.type)
        from studyverse.institutions i where i.pilot_until > now() and i.pilot_until <= now() + interval '5 days'
          and not exists (select 1 from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid')
      union all
      select 'pilotover:' || i.id || ':' || to_char(i.pilot_until, 'YYYYMMDD'), 'pilot_over', 2, 'school', i.id::text, i.contact_email, i.name, null, i.contact_phone, null, i.pilot_until,
             jsonb_build_object('contact', i.contact_name, 'type', i.type)
        from studyverse.institutions i where i.pilot_until <= now() and i.pilot_until > now() - interval '14 days'
          and not exists (select 1 from studyverse.seat_orders o where o.institution_id = i.id and o.status in ('paid', 'invoiced'))
      union all
      select 'schoolrenew:' || i.id || ':' || to_char(o.until, 'YYYYMMDD'), 'school_renewal', case when o.until <= now() + interval '14 days' then 1 else 2 end, 'school', i.id::text,
             i.contact_email, i.name, null, i.contact_phone, null, o.until, jsonb_build_object('contact', i.contact_name, 'type', i.type, 'seats', o.seats)
        from studyverse.institutions i join (select o.institution_id, max(o.valid_until) as until, sum(o.students) filter (where o.valid_until > now()) as seats
                                            from studyverse.seat_orders o where o.status = 'paid' group by 1) o on o.institution_id = i.id
        where o.until > now() and o.until <= now() + interval '30 days'
      union all
      select 'schoolusage:' || x.id || ':' || to_char(t, 'IYYYIW'), 'school_low_use', 2, 'school', x.id::text, x.contact_email, x.name, null, x.contact_phone, null, null,
             jsonb_build_object('contact', x.contact_name, 'type', x.type, 'seats', x.seats, 'students', x.students, 'active7', x.active7)
        from iu x
        where (x.seats >= 10 and x.students * 2 < x.seats) or (x.students >= 5 and x.active7 * 10 < x.students * 3)
      union all
      select 'invoice:' || o.id, 'order_unpaid', 2, 'school', i.id::text, i.contact_email, i.name, null, i.contact_phone, null, o.invoiced_at,
             jsonb_build_object('contact', i.contact_name, 'total', o.total, 'invoice_no', o.invoice_no)
        from studyverse.seat_orders o join studyverse.institutions i on i.id = o.institution_id
        where o.status = 'invoiced' and o.invoiced_at < now() - interval '7 days'
      union all
      select 'request:' || r.id, 'pilot_request', 1, 'lead', r.id::text, r.email, r.school, null, r.phone, null, r.created_at,
             jsonb_build_object('contact', r.name, 'city', r.city, 'students', r.students)
        from studyverse.pilot_requests r where r.created_at > now() - interval '14 days'
          and not exists (select 1 from studyverse.institutions i where (r.email is not null and lower(i.contact_email) = lower(r.email)) or (r.phone is not null and i.contact_phone = r.phone))
      union all
      -- content
      select 'hardq:' || h.qid, 'hard_question', 3, 'content', h.qid, null, null, null, null, null, null, jsonb_build_object('tries', h.tries, 'acc', h.acc, 'users', h.users)
        from (select a.qid, count(*) as tries, count(distinct a.user_id) as users, round(100.0 * sum(a.ok) / count(*)) as acc
              from _od_a a group by a.qid having count(*) >= 10 and sum(a.ok) * 100 < count(*) * 35 order by 4, 2 desc limit 5) h
    ),
    marked as (select it.*, fu.status as mark, fu.snooze_until, fu.note, fu.updated_at as marked_at
               from items it left join studyverse.owner_followups fu on fu.owner_id = me and fu.item_key = it.key)
  select jsonb_build_object('ok', true, 'today', t,
    'items', coalesce((select jsonb_agg(jsonb_build_object('key', m.key, 'kind', m.kind, 'pri', m.pri, 'who', m.who_kind, 'id', m.who_id, 'email', m.email, 'name', m.name,
        'parents', m.parent_emails, 'phone', m.phone, 'band', m.band, 'due', m.due, 'meta', m.meta,
        'state', case when m.mark = 'snoozed' and m.snooze_until <= now() then 'open' else coalesce(m.mark, 'open') end,
        'snooze_until', m.snooze_until, 'note', m.note, 'marked_at', m.marked_at) order by m.pri, case m.kind when 'pilot_ending' then 1 when 'pilot_request' then 2 when 'school_renewal' then 3 when 'trial_end' then 4
        when 'expiring' then 5 when 'pay_failed' then 6 when 'pilot_over' then 7 when 'order_unpaid' then 8 when 'school_low_use' then 9 else 10 end, m.due nulls last, m.key)
      from (select * from marked limit 600) m), '[]'::jsonb),
    'improve', jsonb_build_object(
      'hard', coalesce((select jsonb_agg(x) from (select a.qid, count(*) as tries, round(100.0 * sum(a.ok) / count(*)) as acc from _od_a a
                group by a.qid having count(*) >= 5 order by 3, 2 desc limit 3) x), '[]'::jsonb),
      'drop', coalesce((select jsonb_agg(x) from (select fe.key as topic, sum(greatest(studyverse._od_n(fe.value -> 0) - studyverse._od_n(fe.value -> 1), 0))::int as left_n,
                sum(studyverse._od_n(fe.value -> 0))::int as starts
                from pp cross join lateral jsonb_each(pp.ou_t) fe
                where jsonb_typeof(fe.value) = 'array' group by 1 having sum(studyverse._od_n(fe.value -> 0)) >= 2 order by 2 desc, 3 desc limit 3) x), '[]'::jsonb),
      'steps', coalesce((select jsonb_object_agg(x.k, x.n) from (select fe.key as k, sum(studyverse._od_n(fe.value))::int as n
                from pp cross join lateral jsonb_each(pp.ou_x) dd cross join lateral jsonb_each(studyverse._od_obj(dd.value)) fe
                where studyverse._od_date(dd.key) > t - 7 group by 1) x), '{}'::jsonb),
      'features', coalesce((select jsonb_object_agg(x.k, x.users) from (select z.k, count(*) as users from (select fe.key as k, pp.user_id
                from pp cross join lateral jsonb_each(pp.ou_d) dd cross join lateral jsonb_each(studyverse._od_obj(dd.value)) fe
                where studyverse._od_date(dd.key) > t - 30 group by 1, 2) z group by 1) x), '{}'::jsonb),
      'tracked', (select count(*) from pp where pp.ou_d <> '{}'::jsonb))
  ) into res;
  return res;
end $$;

-- the owner's mark on one Smart Manager item (the only write in this file)
create or replace function studyverse.owner_followup_set(p_key text, p_status text, p_snooze_days int default null, p_note text default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare k text := left(trim(coalesce(p_key, '')), 200); n text := nullif(left(trim(coalesce(p_note, '')), 1000), '');
begin
  if not studyverse._od_is_owner() then return null; end if;
  if length(k) < 3 or p_status not in ('open', 'done', 'snoozed') then return jsonb_build_object('ok', false, 'msg', 'Not a valid item.'); end if;
  if p_status = 'open' and n is null then
    delete from studyverse.owner_followups where owner_id = auth.uid() and item_key = k;
    return jsonb_build_object('ok', true, 'status', 'open');
  end if;
  insert into studyverse.owner_followups (owner_id, item_key, status, snooze_until, note, updated_at)
  values (auth.uid(), k, p_status, case when p_status = 'snoozed' then now() + make_interval(days => least(greatest(coalesce(p_snooze_days, 3), 1), 90)) end, n, now())
  on conflict (owner_id, item_key) do update set status = excluded.status, snooze_until = excluded.snooze_until,
    note = case when p_note is null then studyverse.owner_followups.note else excluded.note end, updated_at = now();
  return jsonb_build_object('ok', true, 'status', p_status);
end $$;

-- ---------- privileges ----------
do $$
declare r record;
begin
  for r in select p.oid::regprocedure as sig, p.proname from pg_proc p where p.pronamespace = 'studyverse'::regnamespace
             and (p.proname like '\_od\_%' or p.proname like 'owner\_dash\_%' or p.proname = 'owner_followup_set') loop
    execute format('revoke all on function %s from public, anon', r.sig);
    if r.proname like '\_od\_%' then execute format('revoke all on function %s from authenticated', r.sig);
    else execute format('grant execute on function %s to authenticated', r.sig); end if;
    execute format('grant execute on function %s to service_role', r.sig);
  end loop;
end $$;
