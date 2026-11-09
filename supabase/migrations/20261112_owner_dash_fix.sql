-- ============================================================================================
-- StudyVerse — Pulse (owner dashboard) fixes, round 2 (pairs with js/owner.js).  Run AFTER 20261111_owner_dash.sql.
-- 1. Test / demo accounts are hidden everywhere unless the dashboard sends p.test = true ("Show test accounts"):
--    emails ending @example.com, @example.org, .test or .invalid; auth user_metadata demo = true; the old
--    "Demo Student" profile. School / coaching staff (admins, teachers) are no longer counted as students;
--    owners (studyverse.admins) were already left out.
-- 2. Comparison everywhere: overview / subscriptions / usage / parents also return the previous period of the same
--    length, a faded previous-period series for the trend charts, and — when p.cmp = N (the "All time" view) —
--    the last N days vs the N days before (c30 / p30).
-- 3. owner_dash_parents gets one new optional argument p jsonb (test toggle + comparison). Because the argument list
--    changes, the old 5-argument version is dropped first (old app versions keep working: the new argument has a default).
-- Everything else is CREATE OR REPLACE with the same signatures. Still read-only except owner_followups. Idempotent.
-- ============================================================================================

-- ---------- helpers ----------
create or replace function studyverse._od_test_email(e text) returns boolean language sql immutable as $$
  select coalesce(lower(e) ~ '(@example\.(com|org)|\.test|\.invalid)$', false) $$;
create or replace function studyverse._od_test_user(u uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from auth.users x where x.id = u and (studyverse._od_test_email(x.email) or coalesce(x.raw_user_meta_data ->> 'demo', '') in ('true', '1')))
      or exists (select 1 from studyverse.progress pr where pr.user_id = u and pr.state #>> '{st,profile,name}' = 'Demo Student') $$;

-- subscription numbers for one period
create or replace function studyverse._od_subsums(ids uuid[], f date, t date) returns jsonb language sql stable security definer set search_path = '' as $$
  with pay as (select py.* from studyverse.payments py where py.user_id in (select unnest(ids))),
       ok as (select pay.*, row_number() over (partition by pay.user_id order by pay.paid_at) > 1 as is_renewal from pay where pay.status = 'paid' and pay.amount_paise > 0),
       lastu as (select ok.user_id, max(ok.valid_until) as until from ok group by 1),
       firsts as (select ok.user_id, min(ok.paid_at) as first_at from ok group by 1),
       r as (select studyverse._od_ts(f) as fs, least(now(), studyverse._od_ts(t + 1)) as te, studyverse._od_ts(t + 1) as te2)
  select jsonb_build_object(
    'new', (select count(*) from firsts, r where firsts.first_at >= r.fs and firsts.first_at < r.te2),
    'renewed', (select count(*) from ok, r where ok.paid_at >= r.fs and ok.paid_at < r.te2 and ok.is_renewal),
    'expired', (select count(*) from lastu, r where lastu.until >= r.fs and lastu.until < r.te),
    'trials', (select count(*) from studyverse.profiles pf, r where pf.user_id in (select unnest(ids)) and pf.trial_at >= r.fs and pf.trial_at < r.te2),
    'failed', (select count(*) from pay, r where pay.status in ('failed', 'created') and pay.created_at < now() - interval '30 minutes' and pay.created_at >= r.fs and pay.created_at < r.te2),
    'revenue', round(coalesce((select sum(ok.amount_paise) / 100.0 from ok, r where ok.paid_at >= r.fs and ok.paid_at < r.te2), 0))) $$;

-- activity numbers for one period (from the per-day records, so they are complete)
create or replace function studyverse._od_actsums(ids uuid[], f date, t date) returns jsonb language sql stable security definer set search_path = '' as $$
  select jsonb_build_object('active', count(distinct d.user_id), 'answers', coalesce(sum(d.a), 0), 'right', coalesce(sum(d.r), 0), 'secs', coalesce(sum(d.secs), 0))
  from studyverse._od_days(ids) d where d.day between f and t $$;

-- ---------- students: hide test / demo accounts and school staff ----------
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
      -- test / demo accounts are hidden unless p.test is true
      and (coalesce(p ->> 'test', '') in ('true', '1') or not (studyverse._od_test_email(u.email) or coalesce(u.raw_user_meta_data ->> 'demo', '') in ('true', '1')
           or coalesce(x.prof ->> 'name', '') = 'Demo Student'))
      -- school / coaching staff (admins, teachers) are not students unless they also joined a class as a student
      and not (exists (select 1 from studyverse.institution_members im where im.user_id = u.id and im.role in ('admin', 'teacher'))
               and not exists (select 1 from studyverse.institution_members im where im.user_id = u.id and im.role = 'student'))
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

-- ---------- overview ----------
create or replace function studyverse.owner_dash_overview(p_from date, p_to date, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare ids uuid[]; f date := least(p_from, p_to); t date := greatest(p_from, p_to); n int; b text; res jsonb; tp boolean := coalesce(p ->> 'test', '') in ('true', '1');
begin
  if not studyverse._od_is_owner() then return null; end if;
  if f is null or t is null or t - f > 3660 then return jsonb_build_object('ok', false, 'msg', 'Choose a date range of up to 10 years.'); end if;
  n := t - f + 1; b := studyverse._od_bucket(f, t, null);
  if to_regclass('pg_temp._od_u') is null then create temp table _od_u on commit drop as select * from studyverse._od_users('{}'::jsonb) limit 0; end if;
  truncate _od_u; insert into _od_u select * from studyverse._od_users(coalesce(p, '{}'::jsonb));
  select coalesce(array_agg(u.user_id), '{}') into ids from _od_u u;
  with days as (select * from studyverse._od_days(ids) d where d.day between f - n and t),
       bk as (select greatest(f, gs::date) as s, least(t, (gs + ('1 ' || b)::interval - interval '1 day')::date) as e
              from generate_series(date_trunc(b, f::timestamp), t::timestamp, ('1 ' || b)::interval) gs),
       -- the same buckets shifted back by the period length (faded "previous period" line)
       bkp as (select row_number() over (order by bk.s) as i, bk.s - n as s, bk.e - n as e from bk)
  select jsonb_build_object('ok', true, 'from', f, 'to', t, 'bucket', b,
    'cur', studyverse._od_kpis(ids, f, t), 'prev', studyverse._od_kpis(ids, f - n, f - 1),
    'c30', case when studyverse._od_int(p ->> 'cmp') > 0 then studyverse._od_kpis(ids, t - (studyverse._od_int(p ->> 'cmp') - 1), t) end,
    'p30', case when studyverse._od_int(p ->> 'cmp') > 0 then studyverse._od_kpis(ids, t - (2 * studyverse._od_int(p ->> 'cmp') - 1), t - studyverse._od_int(p ->> 'cmp')) end,
    'status', coalesce((select jsonb_object_agg(x.status, x.c) from (select u.status, count(*) as c from _od_u u group by 1) x), '{}'::jsonb),
    'bands', coalesce((select jsonb_object_agg(coalesce(x.band, 'unknown'), x.c) from (select u.band, count(*) as c from _od_u u group by 1) x), '{}'::jsonb),
    'sources', coalesce((select jsonb_object_agg(x.source, x.c) from (select u.source, count(*) as c from _od_u u group by 1) x), '{}'::jsonb),
    'parents', (select count(*) from studyverse.profiles pf join auth.users pu on pu.id = pf.user_id where pf.role = 'parent' and (tp or not studyverse._od_test_user(pu.id))),
    'parents_linked', (select count(distinct pl.parent_id) from studyverse.parent_links pl where tp or not studyverse._od_test_user(pl.parent_id)),
    'schools', (select count(*) from studyverse.institutions i where i.status in ('active', 'pilot') and (tp or not studyverse._od_test_email(i.contact_email))),
    'school_revenue', round(coalesce((select sum(o.taxable) from studyverse.seat_orders o where o.status = 'paid'
                       and o.paid_at >= studyverse._od_ts(f) and o.paid_at < studyverse._od_ts(t + 1)
                       and (studyverse._od_uuid(p ->> 'inst') is null or o.institution_id = studyverse._od_uuid(p ->> 'inst'))), 0)),
    'series', coalesce((select jsonb_agg(jsonb_build_object('d', bk.s,
        'active', (select count(distinct d.user_id) from days d where d.day between bk.s and bk.e),
        'signups', (select count(*) from _od_u u where (u.signup at time zone 'utc')::date between bk.s and bk.e),
        'answers', (select coalesce(sum(d.a), 0) from days d where d.day between bk.s and bk.e)) order by bk.s) from bk), '[]'::jsonb),
    'pseries', coalesce((select jsonb_agg(jsonb_build_object('d', bkp.s,
        'active', (select count(distinct d.user_id) from days d where d.day between bkp.s and bkp.e),
        'signups', (select count(*) from _od_u u where (u.signup at time zone 'utc')::date between bkp.s and bkp.e)) order by bkp.i) from bkp), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- ---------- subscriptions ----------
create or replace function studyverse.owner_dash_subs(p_from date, p_to date, p_bucket text default null, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare ids uuid[]; f date := least(p_from, p_to); t date := greatest(p_from, p_to); b text; res jsonb; c0 date; n int; kc int;
begin
  if not studyverse._od_is_owner() then return null; end if;
  if f is null or t is null or t - f > 3660 then return jsonb_build_object('ok', false, 'msg', 'Choose a date range of up to 10 years.'); end if;
  b := studyverse._od_bucket(f, t, p_bucket); n := t - f + 1; kc := studyverse._od_int(p ->> 'cmp');
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
    'sums', studyverse._od_subsums(ids, f, t), 'psums', studyverse._od_subsums(ids, f - n, f - 1),
    'c30', case when kc > 0 then studyverse._od_subsums(ids, t - (kc - 1), t) end, 'p30', case when kc > 0 then studyverse._od_subsums(ids, t - (2 * kc - 1), t - kc) end,
    'pseries', coalesce((select jsonb_agg(jsonb_build_object('d', bk.s - n,
        'new', (select count(*) from firsts x where x.first_at >= studyverse._od_ts(bk.s - n) and x.first_at < studyverse._od_ts(bk.e - n + 1)),
        'revenue', round(coalesce((select sum(ok.amount_paise) / 100.0 from ok where ok.paid_at >= studyverse._od_ts(bk.s - n) and ok.paid_at < studyverse._od_ts(bk.e - n + 1)), 0))
      ) order by bk.s) from bk), '[]'::jsonb),
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

-- ---------- usage & content ----------
create or replace function studyverse.owner_dash_usage(p_from date, p_to date, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare ids uuid[]; f date := least(p_from, p_to); t date := greatest(p_from, p_to); res jsonb; fs timestamptz; te timestamptz; n int; k int;
begin
  if not studyverse._od_is_owner() then return null; end if;
  if f is null or t is null or t - f > 3660 then return jsonb_build_object('ok', false, 'msg', 'Choose a date range of up to 10 years.'); end if;
  fs := studyverse._od_ts(f); te := studyverse._od_ts(t + 1); n := t - f + 1; k := studyverse._od_int(p ->> 'cmp');
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
    'act', studyverse._od_actsums(ids, f, t), 'pact', studyverse._od_actsums(ids, f - n, f - 1),
    'c30', case when k > 0 then studyverse._od_actsums(ids, t - (k - 1), t) end, 'p30', case when k > 0 then studyverse._od_actsums(ids, t - (2 * k - 1), t - k) end,
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

-- ---------- parents (new optional argument p) ----------
drop function if exists studyverse.owner_dash_parents(date, date, text, int, int);
create or replace function studyverse.owner_dash_parents(p_from date, p_to date, p_q text default null, p_limit int default 50, p_offset int default 0, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; f date := least(p_from, p_to); t date := greatest(p_from, p_to); lim int := least(greatest(coalesce(p_limit, 50), 1), 5000);
  tp boolean := coalesce(p ->> 'test', '') in ('true', '1'); n int := greatest(p_from, p_to) - least(p_from, p_to) + 1; k int := studyverse._od_int(p ->> 'cmp');
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
      (select count(*) from studyverse.parent_challenges c where c.parent_id = u.id and c.created_at >= studyverse._od_ts(f - n) and c.created_at < studyverse._od_ts(f)) as challenges_prev,
      coalesce((select pp.weekly_email from studyverse.parent_prefs pp where pp.parent_id = u.id), true) as weekly,
      exists (select 1 from studyverse.parent_links pl join studyverse.course_access c on c.user_id = pl.child_id and c.note like 'paid%' and c.valid_until > now() where pl.parent_id = u.id) as kid_paid
    from auth.users u join studyverse.profiles pf on pf.user_id = u.id and pf.role = 'parent'
    where tp or not studyverse._od_test_user(u.id)
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
    'new_prev', (select count(*) from par where par.created_at >= studyverse._od_ts(f - n) and par.created_at < studyverse._od_ts(f)),
    'challenges_prev', (select coalesce(sum(par.challenges_prev), 0) from par),
    'new_c30', case when k > 0 then (select count(*) from par where par.created_at >= studyverse._od_ts(t - k + 1)) end,
    'new_p30', case when k > 0 then (select count(*) from par where par.created_at >= studyverse._od_ts(t - 2 * k + 1) and par.created_at < studyverse._od_ts(t - k + 1)) end,
    'seen7_prev', (select count(*) from par where par.last_sign_in_at > now() - interval '14 days' and par.last_sign_in_at <= now() - interval '7 days'),
    'rows', coalesce((select jsonb_agg(to_jsonb(x) - 'challenges_prev' order by x.last_sign_in_at desc nulls last) from (
        select par.* from par where nullif(trim(p_q), '') is null or par.email ilike '%' || trim(p_q) || '%' or par.kid_names ilike '%' || trim(p_q) || '%'
        order by par.last_sign_in_at desc nulls last, par.email limit lim offset greatest(coalesce(p_offset, 0), 0)) x), '[]'::jsonb)
  ) into res;
  return res;
end $$;

-- ---------- schools & coaching ----------
create or replace function studyverse.owner_dash_institutions(p jsonb default '{}'::jsonb) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare res jsonb; t date := studyverse._od_today();
begin
  if not studyverse._od_is_owner() then return null; end if;
  with i as (select x.* from studyverse.institutions x
             where (coalesce(p ->> 'test', '') in ('true', '1') or not studyverse._od_test_email(x.contact_email))
               and (nullif(p ->> 'state', '') is null or x.state = p ->> 'state') and (studyverse._od_uuid(p ->> 'inst') is null or x.id = studyverse._od_uuid(p ->> 'inst'))),
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
    'requests', (select count(*) from studyverse.pilot_requests pr where pr.created_at > now() - interval '30 days' and (coalesce(p ->> 'test', '') in ('true', '1') or not studyverse._od_test_email(pr.email))),
    'requests_prev', (select count(*) from studyverse.pilot_requests pr where pr.created_at > now() - interval '60 days' and pr.created_at <= now() - interval '30 days' and (coalesce(p ->> 'test', '') in ('true', '1') or not studyverse._od_test_email(pr.email))),
    'request_rows', coalesce((select jsonb_agg(jsonb_build_object('id', pr.id, 'name', pr.name, 'school', pr.school, 'city', pr.city, 'phone', pr.phone, 'email', pr.email,
                       'students', pr.students, 'created_at', pr.created_at) order by pr.created_at desc)
                     from studyverse.pilot_requests pr where pr.created_at > now() - interval '90 days' and (coalesce(p ->> 'test', '') in ('true', '1') or not studyverse._od_test_email(pr.email))), '[]'::jsonb),
    'rows', coalesce((select jsonb_agg(to_jsonb(rows) order by rows.name) from rows), '[]'::jsonb)) into res;
  return res;
end $$;

-- ---------- Pulse Coach ----------
create or replace function studyverse.owner_dash_smart(p jsonb default '{}'::jsonb) returns jsonb language plpgsql volatile security definer set search_path = '' as $$
declare res jsonb; ids uuid[]; t date := studyverse._od_today(); me uuid := auth.uid(); tp boolean := coalesce(p ->> 'test', '') in ('true', '1');
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
           from studyverse.institutions i where i.status in ('active', 'pilot') and (tp or not studyverse._od_test_email(i.contact_email))),
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
          and (pu.last_sign_in_at is null or pu.last_sign_in_at < now() - interval '14 days') and (tp or not studyverse._od_test_user(pu.id))
      union all
      select 'pinvite:' || pi.id, 'parent_invite', 3, 'parent', pi.parent_id::text, pu.email::text, null, null, null, null, pi.created_at,
             jsonb_build_object('child', left(coalesce(pi.child_name, ''), 30))
        from studyverse.parent_invites pi join auth.users pu on pu.id = pi.parent_id
        where pi.accepted_at is null and pi.expires_at > now() and pi.created_at < now() - interval '3 days' and (tp or not studyverse._od_test_user(pi.parent_id))
      union all
      -- schools & coaching
      select 'pilotend:' || i.id || ':' || to_char(i.pilot_until, 'YYYYMMDD'), 'pilot_ending', 1, 'school', i.id::text, i.contact_email, i.name, null, i.contact_phone, null, i.pilot_until,
             jsonb_build_object('contact', i.contact_name, 'type', i.type)
        from studyverse.institutions i where i.pilot_until > now() and i.pilot_until <= now() + interval '5 days' and (tp or not studyverse._od_test_email(i.contact_email))
          and not exists (select 1 from studyverse.seat_orders o where o.institution_id = i.id and o.status = 'paid')
      union all
      select 'pilotover:' || i.id || ':' || to_char(i.pilot_until, 'YYYYMMDD'), 'pilot_over', 2, 'school', i.id::text, i.contact_email, i.name, null, i.contact_phone, null, i.pilot_until,
             jsonb_build_object('contact', i.contact_name, 'type', i.type)
        from studyverse.institutions i where i.pilot_until <= now() and i.pilot_until > now() - interval '14 days' and (tp or not studyverse._od_test_email(i.contact_email))
          and not exists (select 1 from studyverse.seat_orders o where o.institution_id = i.id and o.status in ('paid', 'invoiced'))
      union all
      select 'schoolrenew:' || i.id || ':' || to_char(o.until, 'YYYYMMDD'), 'school_renewal', case when o.until <= now() + interval '14 days' then 1 else 2 end, 'school', i.id::text,
             i.contact_email, i.name, null, i.contact_phone, null, o.until, jsonb_build_object('contact', i.contact_name, 'type', i.type, 'seats', o.seats)
        from studyverse.institutions i join (select o.institution_id, max(o.valid_until) as until, sum(o.students) filter (where o.valid_until > now()) as seats
                                            from studyverse.seat_orders o where o.status = 'paid' group by 1) o on o.institution_id = i.id
        where o.until > now() and o.until <= now() + interval '30 days' and (tp or not studyverse._od_test_email(i.contact_email))
      union all
      select 'schoolusage:' || x.id || ':' || to_char(t, 'IYYYIW'), 'school_low_use', 2, 'school', x.id::text, x.contact_email, x.name, null, x.contact_phone, null, null,
             jsonb_build_object('contact', x.contact_name, 'type', x.type, 'seats', x.seats, 'students', x.students, 'active7', x.active7)
        from iu x
        where (x.seats >= 10 and x.students * 2 < x.seats) or (x.students >= 5 and x.active7 * 10 < x.students * 3)
      union all
      select 'invoice:' || o.id, 'order_unpaid', 2, 'school', i.id::text, i.contact_email, i.name, null, i.contact_phone, null, o.invoiced_at,
             jsonb_build_object('contact', i.contact_name, 'total', o.total, 'invoice_no', o.invoice_no)
        from studyverse.seat_orders o join studyverse.institutions i on i.id = o.institution_id
        where o.status = 'invoiced' and o.invoiced_at < now() - interval '7 days' and (tp or not studyverse._od_test_email(i.contact_email))
      union all
      select 'request:' || r.id, 'pilot_request', 1, 'lead', r.id::text, r.email, r.school, null, r.phone, null, r.created_at,
             jsonb_build_object('contact', r.name, 'city', r.city, 'students', r.students)
        from studyverse.pilot_requests r where r.created_at > now() - interval '14 days' and (tp or not studyverse._od_test_email(r.email))
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
