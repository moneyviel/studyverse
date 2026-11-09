-- ============================================================================================
-- SQL tests for supabase/migrations/20261111_owner_dash.sql (Owner dashboard + Smart Manager).
-- Run AFTER the migration, as a superuser:   psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/owner_dash_test.sql
-- Everything is inside BEGIN … ROLLBACK. Each check prints PASS / FAIL as a NOTICE; the script ends with an ERROR if any failed.
-- Calls run as role "authenticated" with request.jwt.claims (like PostgREST). Expected numbers are worked out by hand
-- from the fixtures below (see the comments next to each check).
-- ============================================================================================
begin;
select set_config('odtest.fails', '0', true), set_config('odtest.n', '0', true);
create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('odtest.n', (current_setting('odtest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('odtest.fails', (current_setting('odtest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
-- raw reads that bypass RLS (test only): a fingerprint of the app's data, to prove the dashboard changes nothing
create function pg_temp.fp() returns text language sql security definer as $$
  select md5(concat_ws('|', (select string_agg(user_id || course || coalesce(valid_until::text, '') || coalesce(note, ''), ',' order by user_id, course) from studyverse.course_access),
    (select string_agg(id || status || coalesce(valid_until::text, ''), ',' order by id) from studyverse.payments),
    (select string_agg(user_id || md5(state::text), ',' order by user_id) from studyverse.progress),
    (select count(*)::text from studyverse.parent_links), (select count(*)::text from studyverse.institutions), (select count(*)::text from studyverse.codes))) $$;
create function pg_temp.nfollow() returns int language sql security definer as $$ select count(*)::int from studyverse.owner_followups $$;
grant execute on all functions in schema pg_temp to authenticated;

-- ---------- fixtures ----------
-- O owner · X student with nothing · S1 Riya (Class 7, paid, active, parent P1) · S2 Kabir (Class 10, trial ends in 20 h)
-- S3 Meera (CA Foundation, paid ended 5 days ago + a failed payment) · S4 Arjun (Class 3, school seat, idle 10 days)
-- S5 Zoya (Class 7, renewed, ends in 2 days) · P1 parent (last sign-in 20 days ago)
insert into auth.users (id, email, created_at, last_sign_in_at) values
  ('00000000-0000-0000-0000-0000000000a0', 'owner@od.test', now() - interval '200 days', now()),
  ('00000000-0000-0000-0000-0000000000a9', 'nobody@od.test', now() - interval '100 days', null),
  ('00000000-0000-0000-0000-0000000000b1', 'riya@od.test', now() - interval '60 days', now()),
  ('00000000-0000-0000-0000-0000000000b2', 'kabir@od.test', now() - interval '1 hour', now()),
  ('00000000-0000-0000-0000-0000000000b3', 'meera@od.test', now() - interval '70 days', now() - interval '2 hours'),
  ('00000000-0000-0000-0000-0000000000b4', 'arjun@od.test', now() - interval '40 days', now() - interval '10 days'),
  ('00000000-0000-0000-0000-0000000000b5', 'zoya@od.test', now() - interval '90 days', now() - interval '1 day'),
  ('00000000-0000-0000-0000-0000000000c1', 'mum@od.test', now() - interval '59 days', now() - interval '20 days');
insert into studyverse.admins (user_id) values ('00000000-0000-0000-0000-0000000000a0') on conflict do nothing;
insert into studyverse.profiles (user_id, role, trial_at) values
  ('00000000-0000-0000-0000-0000000000b1', 'student', now() - interval '60 days'), ('00000000-0000-0000-0000-0000000000b2', 'student', now() - interval '1 hour'),
  ('00000000-0000-0000-0000-0000000000b3', 'student', null), ('00000000-0000-0000-0000-0000000000b4', 'student', null),
  ('00000000-0000-0000-0000-0000000000b5', 'student', null), ('00000000-0000-0000-0000-0000000000c1', 'parent', null);
insert into studyverse.plans (id, course, label, months, price_inr, sort) values
  ('od-6-8-m', 'school', 'Class 6–8 · 1 month', 1, 249, 90), ('od-ca-f-m', 'ca-foundation', 'CA Foundation · 1 month', 1, 499, 91);
insert into studyverse.payments (user_id, plan_id, amount_paise, order_id, status, created_at, paid_at, valid_until) values
  ('00000000-0000-0000-0000-0000000000b1', 'od-6-8-m', 24900, 'od-o1', 'paid', now() - interval '20 days', now() - interval '20 days', now() + interval '10 days'),
  ('00000000-0000-0000-0000-0000000000b3', 'od-ca-f-m', 49900, 'od-o2', 'paid', now() - interval '35 days', now() - interval '35 days', now() - interval '5 days'),
  ('00000000-0000-0000-0000-0000000000b3', 'od-ca-f-m', 49900, 'od-o3', 'failed', now() - interval '2 hours', null, null),
  ('00000000-0000-0000-0000-0000000000b5', 'od-6-8-m', 24900, 'od-o4', 'paid', now() - interval '60 days', now() - interval '60 days', now() - interval '30 days'),
  ('00000000-0000-0000-0000-0000000000b5', 'od-6-8-m', 24900, 'od-o5', 'paid', now() - interval '28 days', now() - interval '28 days', now() + interval '2 days');
insert into studyverse.course_access (user_id, course, valid_until, note) values
  ('00000000-0000-0000-0000-0000000000b1', 'school-g7', now() + interval '10 days', 'paid od-6-8-m'),
  ('00000000-0000-0000-0000-0000000000b2', 'school-all', now() + interval '20 hours', 'trial'),
  ('00000000-0000-0000-0000-0000000000b3', 'ca-foundation', now() - interval '5 days', 'paid od-ca-f-m'),
  ('00000000-0000-0000-0000-0000000000b5', 'school-g7', now() + interval '2 days', 'paid od-6-8-m');
insert into studyverse.parent_links (parent_id, child_id, child_name, created_at) values
  ('00000000-0000-0000-0000-0000000000c1', '00000000-0000-0000-0000-0000000000b1', 'Riya', now() - interval '58 days');
-- a school in its pilot (ends in 3 days) with Arjun in Class 3-A; and a new pilot request from someone else
insert into studyverse.institutions (id, name, type, city, state, status, pilot_until, contact_name, contact_email, contact_phone) values
  ('00000000-0000-0000-0000-0000000000d1', 'Sunrise School', 'school', 'Pune', 'Maharashtra', 'pilot', now() + interval '3 days', 'Mrs Rao', 'rao@sunrise.test', '+919876543210');
insert into studyverse.inst_classes (id, institution_id, grade, section, course, name) values
  ('00000000-0000-0000-0000-0000000000e1', '00000000-0000-0000-0000-0000000000d1', 3, 'A', 'school-g3', 'Class 3-A');
insert into studyverse.institution_members (institution_id, user_id, role, class_id) values
  ('00000000-0000-0000-0000-0000000000d1', '00000000-0000-0000-0000-0000000000b4', 'student', '00000000-0000-0000-0000-0000000000e1');
insert into studyverse.course_access (user_id, course, valid_until, note) values
  ('00000000-0000-0000-0000-0000000000b4', 'school-g3', now() + interval '3 days', 'inst 00000000-0000-0000-0000-0000000000d1');
insert into studyverse.pilot_requests (name, school, city, phone, email, students, created_at) values ('Mr Khan', 'Green Valley', 'Nagpur', '+919811111111', 'khan@gv.test', 300, now() - interval '2 days');

-- progress (the app's synced ST). D(n) = the app's day key n days ago (UTC). M(n) = epoch minute n hours ago.
create function pg_temp.D(n int) returns text language sql as $$ select to_char((now() at time zone 'utc')::date - n, 'YYYY-MM-DD') $$;
create function pg_temp.M(h int) returns int language sql as $$ select floor(extract(epoch from now() - make_interval(hours => h)) / 60)::int $$;
insert into studyverse.progress (user_id, state) values
  ('00000000-0000-0000-0000-0000000000b1', jsonb_build_object('v', 1, 'st', jsonb_build_object(
     'profile', jsonb_build_object('name', 'Riya Sharma', 'grade', 7, 'board', 'cbse'),
     'streak', jsonb_build_object('n', 6, 'last', pg_temp.D(0)), 'xp', 400,
     'xpLog', jsonb_build_object(pg_temp.D(0), 40, pg_temp.D(3), 20),
     'qstats', jsonb_build_object('g7-maths-01-01#3', jsonb_build_object('s', 6, 'w', 1), 'g7-maths-01-01#4', jsonb_build_object('s', 4, 'w', 1)),
     'topics', jsonb_build_object('g7-maths-01-01', jsonb_build_object('stars', 2, 'last', pg_temp.D(0))),
     'ins', jsonb_build_object('v', 1,
        'day', jsonb_build_object(pg_temp.D(0), jsonb_build_object('a', 12, 'r', 9, 'x', 40, 's', 600, 'sj', jsonb_build_object('maths', jsonb_build_array(12, 9, 600))),
                                  pg_temp.D(20), jsonb_build_object('a', 5, 'r', 5, 'x', 0, 's', 120, 'sj', jsonb_build_object('science', jsonb_build_array(5, 5, 120))),
                                  'bad-key', jsonb_build_object('a', 99)),
        'att', (select jsonb_agg(jsonb_build_array(pg_temp.M(2), 'g7-maths-01-01#3', case when i <= 2 then 1 else 0 end, 0)) from generate_series(1, 10) i)),
     'ou', jsonb_build_object('d', jsonb_build_object(pg_temp.D(0), jsonb_build_object('map', 3, 'practice', 2)),
                             'x', jsonb_build_object(pg_temp.D(0), jsonb_build_object('quiz', 2)),
                             't', jsonb_build_object('g7-maths-01-01', jsonb_build_array(3, 1)),
                             'dev', jsonb_build_object('os', 'Android', 'pwa', true, 'w', 'phone', 'app', '55'))))),
  ('00000000-0000-0000-0000-0000000000b2', jsonb_build_object('v', 1, 'st', jsonb_build_object(
     'profile', jsonb_build_object('name', 'Kabir', 'grade', 10, 'board', 'cbse'), 'streak', jsonb_build_object('n', 1, 'last', pg_temp.D(0)),
     'xpLog', jsonb_build_object(pg_temp.D(0), 10),
     'ou', jsonb_build_object('d', jsonb_build_object(pg_temp.D(0), jsonb_build_object('practice', 1)))))),
  ('00000000-0000-0000-0000-0000000000b3', jsonb_build_object('v', 1, 'st', jsonb_build_object(
     'profile', jsonb_build_object('name', 'Meera', 'grade', 12, 'course', 'ca'), 'ca', jsonb_build_object('level', 'foundation'),
     'streak', jsonb_build_object('n', 2, 'last', pg_temp.D(40))))),
  ('00000000-0000-0000-0000-0000000000b4', jsonb_build_object('v', 1, 'st', jsonb_build_object(
     'profile', jsonb_build_object('name', 'Arjun', 'grade', 3, 'board', 'cbse'), 'xpLog', jsonb_build_object(pg_temp.D(10), 15)))),
  ('00000000-0000-0000-0000-0000000000b5', jsonb_build_object('v', 1, 'st', jsonb_build_object(
     'profile', jsonb_build_object('name', 'Zoya', 'grade', 7, 'board', 'icse'), 'streak', jsonb_build_object('n', 9, 'last', pg_temp.D(1)),
     'xpLog', jsonb_build_object(pg_temp.D(1), 30, 'junk', 'x'))));

select set_config('odtest.fp', pg_temp.fp(), true);
set local role authenticated;
do $$
declare O uuid := '00000000-0000-0000-0000-0000000000a0'; X uuid := '00000000-0000-0000-0000-0000000000b1';
  t date := (now() at time zone 'utc')::date; f date := (now() at time zone 'utc')::date - 29; r jsonb; c jsonb; items jsonb; k text;
begin
  -- ===== non-admins get nothing =====
  perform pg_temp.as_user(X);
  perform pg_temp.chk(studyverse.owner_dash_meta() is null, 'student: meta → null');
  perform pg_temp.chk(studyverse.owner_dash_overview(f, t, '{}') is null, 'student: overview → null');
  perform pg_temp.chk(studyverse.owner_dash_subs(f, t, null, '{}') is null, 'student: subscriptions → null');
  perform pg_temp.chk(studyverse.owner_dash_students('{}', 'name', false, 50, 0) is null, 'student: students list → null');
  perform pg_temp.chk(studyverse.owner_dash_student(X) is null, 'student: own profile drill-down → null');
  perform pg_temp.chk(studyverse.owner_dash_usage(f, t, '{}') is null, 'student: usage → null');
  perform pg_temp.chk(studyverse.owner_dash_parents(f, t, null, 50, 0) is null, 'student: parents → null');
  perform pg_temp.chk(studyverse.owner_dash_institutions('{}') is null, 'student: institutions → null');
  perform pg_temp.chk(studyverse.owner_dash_institution('00000000-0000-0000-0000-0000000000d1') is null, 'student: one institution → null');
  perform pg_temp.chk(studyverse.owner_dash_smart('{}') is null, 'student: smart manager → null');
  perform pg_temp.chk(studyverse.owner_followup_set('trial:x:y', 'done', null, 'hi') is null and pg_temp.nfollow() = 0, 'student: cannot write follow-ups');
  perform pg_temp.as_user('00000000-0000-0000-0000-0000000000c1');
  perform pg_temp.chk(studyverse.owner_dash_overview(f, t, '{}') is null, 'parent: overview → null');
  perform set_config('request.jwt.claims', '', true);
  perform pg_temp.chk(studyverse.owner_dash_students('{}', 'name', false, 50, 0) is null, 'signed out: students → null');
  begin perform studyverse._od_users('{}'); perform pg_temp.chk(false, 'helper _od_users must not be callable by app users');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'helper _od_users is not callable by app users'); end;

  -- ===== owner =====
  perform pg_temp.as_user(O);
  r := studyverse.owner_dash_meta();
  perform pg_temp.chk((r ->> 'ok')::boolean and jsonb_array_length(r -> 'institutions') = 1 and r -> 'boards' @> '["cbse","icse"]', 'meta: institutions and boards');

  -- Overview, last 30 days. Students = X(nobody), S1–S5 = 6 (owner and parent left out).
  r := studyverse.owner_dash_overview(f, t, '{}'); c := r -> 'cur';
  perform pg_temp.chk((c ->> 'students')::int = 6, 'overview: 6 students (owner and parent excluded) [' || (c ->> 'students') || ']');
  perform pg_temp.chk((c ->> 'signups')::int = 1, 'overview: 1 signup in 30 days (Kabir)');
  perform pg_temp.chk((c ->> 'dau')::int = 2 and (c ->> 'wau')::int = 3 and (c ->> 'mau')::int = 4, 'overview: DAU 2 · WAU 3 · MAU 4 [' || concat_ws('/', c ->> 'dau', c ->> 'wau', c ->> 'mau') || ']');
  perform pg_temp.chk((c ->> 'paying')::int = 2 and (c ->> 'mrr')::numeric = 498, 'overview: 2 paying, MRR ₹498 (249 + 249) [' || (c ->> 'mrr') || ']');
  perform pg_temp.chk((c ->> 'revenue')::numeric = 498 and (c ->> 'payments')::int = 2, 'overview: revenue ₹498 from 2 payments in the period');
  perform pg_temp.chk((c ->> 'new_paid')::int = 1 and (c ->> 'renewed')::int = 1 and (c ->> 'churned')::int = 1, 'overview: new 1 (Riya) · renewed 1 (Zoya) · churned 1 (Meera)');
  perform pg_temp.chk((c ->> 'trials')::int = 1 and (c ->> 'trial_paid')::int = 0, 'overview: 1 trial started, 0 converted yet');
  perform pg_temp.chk((r #>> '{prev,new_paid}')::int = 1 and (r #>> '{prev,revenue}')::numeric = 499, 'overview: previous 30 days = Meera''s first payment ₹499');
  perform pg_temp.chk((r #>> '{status,paid}')::int = 2 and (r #>> '{status,school}')::int = 1 and (r #>> '{status,trial}')::int = 1
                      and (r #>> '{status,lapsed}')::int = 1 and (r #>> '{status,none}')::int = 1, 'overview: status split paid 2 · school 1 · trial 1 · lapsed 1 · none 1');
  perform pg_temp.chk((r #>> '{bands,6-8}')::int = 2 and (r #>> '{bands,ca-foundation}')::int = 1, 'overview: band split (6–8: 2, CA Foundation: 1)');
  perform pg_temp.chk((r ->> 'parents')::int = 1 and (r ->> 'schools')::int = 1 and jsonb_array_length(r -> 'series') = 30, 'overview: parents, schools, 30 daily points');
  perform pg_temp.chk((select sum((e ->> 'active')::int) from jsonb_array_elements(r -> 'series') e) = 6, 'overview: active user-days = 6 (Riya ×3, Kabir, Zoya, Arjun)');
  -- filters
  r := studyverse.owner_dash_overview(f, t, '{"band":"6-8"}');
  perform pg_temp.chk((r #>> '{cur,students}')::int = 2 and (r #>> '{cur,paying}')::int = 2, 'overview filter band 6–8: 2 students, both paying');
  r := studyverse.owner_dash_overview(f, t, jsonb_build_object('inst', '00000000-0000-0000-0000-0000000000d1'));
  perform pg_temp.chk((r #>> '{cur,students}')::int = 1 and (r #>> '{status,school}')::int = 1, 'overview filter institution: Arjun only');

  -- Subscriptions
  r := studyverse.owner_dash_subs(f, t, 'week', '{}');
  perform pg_temp.chk(r ->> 'bucket' = 'week' and (select sum((e ->> 'new')::int) from jsonb_array_elements(r -> 'series') e) = 1
                      and (select sum((e ->> 'renewed')::int) from jsonb_array_elements(r -> 'series') e) = 1
                      and (select sum((e ->> 'expired')::int) from jsonb_array_elements(r -> 'series') e) = 1
                      and (select sum((e ->> 'failed')::int) from jsonb_array_elements(r -> 'series') e) = 1, 'subs: weekly series new 1 · renewed 1 · expired 1 · failed 1');
  perform pg_temp.chk((select sum((e ->> 'revenue')::numeric) from jsonb_array_elements(r -> 'series') e) = 498, 'subs: revenue series sums to ₹498');
  perform pg_temp.chk((r ->> 'due7')::int = 1 and (r ->> 'due30')::int = 2 and r #>> '{due,0,email}' = 'zoya@od.test', 'subs: renewals due 7d = 1 (Zoya first), 30d = 2');
  perform pg_temp.chk(jsonb_array_length(r -> 'by_plan') = 1 and (r #>> '{by_plan,0,payments}')::int = 2 and (r #>> '{by_plan,0,active_now}')::int = 2, 'subs: by plan (Class 6–8 monthly: 2 payments, 2 active)');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(r -> 'by_band') e where e ->> 'band' = '6-8' and (e ->> 'paid')::int = 2), 'subs: by band 6–8 has 2 paid');
  perform pg_temp.chk(jsonb_array_length(r -> 'cohorts') = 12, 'subs: 12 signup-month cohorts');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(r -> 'cohorts') e where (e ->> 'n')::int >= 1 and jsonb_array_length(e -> 'act') >= 1), 'subs: cohorts carry retention rows');

  -- Students table
  r := studyverse.owner_dash_students('{"q":"riya"}', 'name', false, 50, 0);
  perform pg_temp.chk((r ->> 'total')::int = 1 and r #>> '{rows,0,parents}' = 'mum@od.test' and (r #>> '{rows,0,answered}')::int = 10
                      and (r #>> '{rows,0,accuracy}')::int = 80 and (r #>> '{rows,0,streak}')::int = 6 and r #>> '{rows,0,band}' = '6-8', 'students: search Riya → parents, 10 answered, 80% accuracy, streak 6');
  perform pg_temp.chk(r #>> '{rows,0,status}' = 'paid' and r #>> '{rows,0,plan}' = 'Class 6–8 · 1 month' and r #>> '{rows,0,source}' = 'self', 'students: Riya paid, plan label, source self');
  perform pg_temp.chk(not ((r -> 'rows' -> 0) ? 'password') and not ((r -> 'rows' -> 0) ? 'payment_id'), 'students: no secrets in rows');
  r := studyverse.owner_dash_students('{}', 'answered', true, 2, 0);
  perform pg_temp.chk((r ->> 'total')::int = 6 and jsonb_array_length(r -> 'rows') = 2 and r #>> '{rows,0,email}' = 'riya@od.test', 'students: sort by answered desc, page of 2');
  r := studyverse.owner_dash_students('{}', 'answered', true, 2, 4);
  perform pg_temp.chk(jsonb_array_length(r -> 'rows') = 2, 'students: last page has 2 rows');
  r := studyverse.owner_dash_students('{"status":"lapsed"}', 'name', false, 50, 0);
  perform pg_temp.chk((r ->> 'total')::int = 1 and r #>> '{rows,0,email}' = 'meera@od.test' and r #>> '{rows,0,band}' = 'ca-foundation', 'students: filter lapsed → Meera (CA Foundation)');
  r := studyverse.owner_dash_students('{"source":"school"}', 'name', false, 50, 0);
  perform pg_temp.chk((r ->> 'total')::int = 1 and r #>> '{rows,0,inst_name}' = 'Sunrise School' and r #>> '{rows,0,class_name}' = 'Class 3-A', 'students: source school → Arjun with class');
  r := studyverse.owner_dash_students('{"board":"icse","grade":"7"}', 'bogus; drop table x', true, 50, 0);
  perform pg_temp.chk((r ->> 'total')::int = 1 and r ->> 'sort' = 'last_active', 'students: board + class filter; unknown sort key falls back safely');

  -- One student
  r := studyverse.owner_dash_student('00000000-0000-0000-0000-0000000000b1');
  perform pg_temp.chk((r ->> 'ok')::boolean and jsonb_array_length(r -> 'payments') = 1 and jsonb_array_length(r -> 'parents') = 1 and r #>> '{parents,0,email}' = 'mum@od.test', 'student: payments and parents');
  perform pg_temp.chk(jsonb_array_length(r -> 'days') = 3 and r #>> '{subjects,0,subj}' = 'g7-maths' and (r #>> '{topics_done,g7-maths}')::int = 1, 'student: 3 active days, subject progress, topics done');
  perform pg_temp.chk((r #>> '{usage,map}')::int = 3 and r #>> '{device,os}' = 'Android', 'student: feature usage and device');
  perform pg_temp.chk((studyverse.owner_dash_student('00000000-0000-0000-0000-0000000000a0') ->> 'ok')::boolean is false, 'student: the owner account is not a student');

  -- Usage & content
  r := studyverse.owner_dash_usage(f, t, '{}');
  perform pg_temp.chk((r ->> 'students')::int = 6 and (r ->> 'active')::int = 4 and (r ->> 'tracked_users')::int = 2, 'usage: 6 students, 4 active, 2 with usage tracking');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(r -> 'features') e where e ->> 'k' = 'practice' and (e ->> 'users')::int = 2 and (e ->> 'opens')::int = 3), 'usage: practice used by 2 students, 3 opens');
  perform pg_temp.chk((r #>> '{drop_steps,quiz}')::int = 2 and r #>> '{drop_topics,0,topic}' = 'g7-maths-01-01' and (r #>> '{drop_topics,0,left_n}')::int = 2, 'usage: drop-off at quiz (2), topic left twice');
  perform pg_temp.chk(r #>> '{hard,0,qid}' = 'g7-maths-01-01#3' and (r #>> '{hard,0,acc}')::int = 20 and (r #>> '{hard,0,tries}')::int = 10, 'usage: hardest question 20% of 10 tries');
  perform pg_temp.chk(r #>> '{subjects,0,sid}' = 'maths' and (r #>> '{subjects,0,answers}')::int = 12 and r #>> '{chapters,0,ch}' = 'g7-maths-01', 'usage: subjects and chapters popularity');
  perform pg_temp.chk((select sum((e ->> 2)::int) from jsonb_array_elements(r -> 'hours') e) = 10, 'usage: time-of-day heatmap counts 10 answers');
  r := studyverse.owner_dash_usage(f, t, '{"band":"ca"}');
  perform pg_temp.chk((r ->> 'students')::int = 1 and jsonb_array_length(r -> 'hard') = 0, 'usage filter CA: no school questions');

  -- Parents, institutions
  r := studyverse.owner_dash_parents(f, t, null, 50, 0);
  perform pg_temp.chk((r ->> 'total')::int = 1 and (r ->> 'linked')::int = 1 and (r ->> 'idle')::int = 1 and (r ->> 'kid_paid')::int = 1
                      and r #>> '{rows,0,kid_names}' = 'Riya', 'parents: 1 linked, idle 20 days, child paid');
  r := studyverse.owner_dash_institutions('{}');
  perform pg_temp.chk((r ->> 'total')::int = 1 and (r ->> 'pilots_now')::int = 1 and (r ->> 'students')::int = 1 and (r ->> 'requests')::int = 1
                      and (r #>> '{rows,0,had_pilot}')::boolean and not (r #>> '{rows,0,paid}')::boolean, 'institutions: 1 pilot school with 1 student, 1 request');
  r := studyverse.owner_dash_institution('00000000-0000-0000-0000-0000000000d1');
  perform pg_temp.chk((r ->> 'ok')::boolean and jsonb_array_length(r -> 'classes') = 1 and (r #>> '{classes,0,students}')::int = 1
                      and jsonb_array_length(r -> 'students') = 1 and not ((r -> 'inst') ? 'gstin'), 'institution drill-down: classes, students, no GSTIN/address');

  -- Smart Manager
  r := studyverse.owner_dash_smart('{}'); items := r -> 'items';
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'trial_end' and e ->> 'email' = 'kabir@od.test' and (e ->> 'pri')::int = 1), 'smart: Kabir''s trial ends today (urgent)');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'expiring' and e ->> 'email' = 'zoya@od.test' and (e ->> 'pri')::int = 1), 'smart: Zoya''s plan ends in 2 days (urgent)');
  perform pg_temp.chk(not exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'expiring' and e ->> 'email' = 'riya@od.test'), 'smart: Riya (10 days left) not yet flagged');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'lapsed' and e ->> 'email' = 'meera@od.test'), 'smart: Meera lapsed 5 days ago');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'pay_failed' and e ->> 'email' = 'meera@od.test'), 'smart: Meera''s failed payment');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'paid_idle' and e ->> 'email' = 'arjun@od.test' and (e #>> '{meta,days}')::int = 10), 'smart: Arjun has a seat but idle 10 days');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'parent_idle' and e ->> 'email' = 'mum@od.test'), 'smart: parent has not opened the app in 14+ days');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'pilot_ending' and e ->> 'phone' = '+919876543210'), 'smart: Sunrise pilot ends in 3 days (with coordinator phone)');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'pilot_request' and e ->> 'name' = 'Green Valley'), 'smart: new pilot request to call');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(items) e where e ->> 'kind' = 'hard_question' and e ->> 'id' = 'g7-maths-01-01#3'), 'smart: hard question to check');
  perform pg_temp.chk((select (e ->> 'pri')::int from jsonb_array_elements(items) e limit 1) = 1, 'smart: list starts with urgent items');
  perform pg_temp.chk(r #>> '{improve,hard,0,qid}' = 'g7-maths-01-01#3' and r #>> '{improve,drop,0,topic}' = 'g7-maths-01-01' and (r #>> '{improve,features,map}')::int = 1, 'smart: weekly improve summary');
  perform pg_temp.chk(jsonb_array_length((studyverse.owner_dash_smart('{"band":"ca"}')) -> 'items') >= 2
                      and not exists (select 1 from jsonb_array_elements((studyverse.owner_dash_smart('{"band":"ca"}')) -> 'items') e where e ->> 'email' = 'kabir@od.test'), 'smart: filters apply to student items');
  -- marks
  select e ->> 'key' into k from jsonb_array_elements(items) e where e ->> 'kind' = 'trial_end';
  perform pg_temp.chk((studyverse.owner_followup_set(k, 'done', null, 'Sent plans on WhatsApp') ->> 'ok')::boolean, 'followup: mark done with note');
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(studyverse.owner_dash_smart('{}') -> 'items') e where e ->> 'key' = k and e ->> 'state' = 'done' and e ->> 'note' = 'Sent plans on WhatsApp'), 'followup: item shows done + note');
  perform studyverse.owner_followup_set(k, 'snoozed', 2, null);
  perform pg_temp.chk(exists (select 1 from jsonb_array_elements(studyverse.owner_dash_smart('{}') -> 'items') e where e ->> 'key' = k and e ->> 'state' = 'snoozed' and e ->> 'note' = 'Sent plans on WhatsApp'), 'followup: snooze keeps the note');
  perform studyverse.owner_followup_set(k, 'open', null, null);
  perform pg_temp.chk(pg_temp.nfollow() = 0, 'followup: reopen without a note removes the mark');
  perform pg_temp.chk((studyverse.owner_followup_set('x', 'done') ->> 'ok')::boolean is false and (studyverse.owner_followup_set('abc:1', 'deleted') ->> 'ok')::boolean is false, 'followup: bad key / status refused');

  -- read-only: nothing in the app's data changed
  perform pg_temp.chk(pg_temp.fp() = current_setting('odtest.fp'), 'dashboards changed no app data');
end $$;
reset role;

do $$ begin
  raise notice '%/% checks passed', current_setting('odtest.n')::int - current_setting('odtest.fails')::int, current_setting('odtest.n');
  if current_setting('odtest.fails')::int > 0 then raise exception '% check(s) failed', current_setting('odtest.fails'); end if;
end $$;
rollback;
