-- ============================================================================================
-- SQL tests for supabase/migrations/20261109_institutions.sql (Schools & Coaching).
-- Run AFTER the migration, as a superuser:   psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/institutions_test.sql
-- Everything is inside BEGIN … ROLLBACK. Each check prints PASS / FAIL as a NOTICE; the script ends with an ERROR if any failed.
-- Calls run as role "authenticated" with request.jwt.claims (like PostgREST). Price expectations are worked out by hand
-- in the comments: amount = students × rate × 10 months; discount on the whole order; GST only with a seller GSTIN.
-- ============================================================================================
begin;
select set_config('ittest.fails', '0', true), set_config('ittest.n', '0', true);
create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('ittest.n', (current_setting('ittest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('ittest.fails', (current_setting('ittest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
-- raw reads that bypass RLS (test only)
create function pg_temp.ca(u uuid, c text) returns studyverse.course_access language sql security definer as $$ select * from studyverse.course_access where user_id = u and course = c $$;
create function pg_temp.nlinks(c uuid) returns int language sql security definer as $$ select count(*)::int from studyverse.parent_links where child_id = c $$;
create function pg_temp.inst(i uuid) returns studyverse.institutions language sql security definer as $$ select * from studyverse.institutions where id = i $$;
create function pg_temp.set_billing(g text, st text) returns void language sql security definer as $$ update studyverse.billing_config set gstin = g, state = st where id = 1 $$;
create function pg_temp.age_order(o uuid) returns void language sql security definer as $$ update studyverse.seat_orders set valid_until = now() - interval '1 minute' where id = o $$;
create function pg_temp.code_of(i uuid, roll text) returns text language sql security definer as $$ select code from studyverse.join_codes where institution_id = i and roll_no = roll $$;
create function pg_temp.pinv(e text) returns uuid language sql security definer as $$ select child_id from studyverse.inst_parent_invites where email = e order by created_at limit 1 $$;
create function pg_temp.svc_bulk(c uuid, i uuid, r jsonb) returns jsonb language sql security definer as $$ select studyverse._inst_bulk_prepare(c, i, r) $$;
create function pg_temp.svc_add(i uuid, u uuid, r text, c uuid, roll text, n text) returns jsonb language sql security definer as $$ select studyverse._inst_add_member(i, u, r, c, roll, n) $$;
create function pg_temp.svc_pilot(p jsonb, ip text) returns jsonb language sql security definer as $$ select studyverse._pilot_request(p, ip) $$;
create function pg_temp.svc_mail(o uuid, c uuid) returns jsonb language sql security definer as $$ select studyverse._inst_order_mail(o, c) $$;
create function pg_temp.svc_staff(c uuid, i uuid, r text) returns jsonb language sql security definer as $$ select studyverse._inst_staff_ok(c, i, r) $$;
grant execute on all functions in schema pg_temp to authenticated;

-- ---------- fixtures ----------
insert into auth.users (id, email) values
  ('00000000-0000-0000-0000-00000000000a', 'owner@t.test'),   ('00000000-0000-0000-0000-0000000000a1', 'principal@t.test'),
  ('00000000-0000-0000-0000-0000000000b1', 'teacher7b@t.test'), ('00000000-0000-0000-0000-0000000000b2', 'teacher8a@t.test'),
  ('00000000-0000-0000-0000-0000000000c1', 'riya@t.test'),    ('00000000-0000-0000-0000-0000000000c2', 'kabir@t.test'),
  ('00000000-0000-0000-0000-0000000000c3', 'meera@t.test'),   ('00000000-0000-0000-0000-0000000000c4', 'other@t.test'),
  ('00000000-0000-0000-0000-0000000000d1', 'mum@t.test'),     ('00000000-0000-0000-0000-0000000000d2', 'dad@t.test'),
  ('00000000-0000-0000-0000-0000000000e1', 'otherprincipal@t.test');
insert into studyverse.admins (user_id) values ('00000000-0000-0000-0000-00000000000a') on conflict do nothing;
insert into studyverse.profiles (user_id, role) values ('00000000-0000-0000-0000-0000000000d1', 'parent'), ('00000000-0000-0000-0000-0000000000c1', 'student');
-- Riya already has a PAID Class 7 plan till 2099 and a parent link (Mum): neither may be lost by joining a school
insert into studyverse.course_access (user_id, course, valid_until, note) values ('00000000-0000-0000-0000-0000000000c1', 'school-g7', '2099-01-01', 'paid s68-year');
insert into studyverse.parent_links (parent_id, child_id, child_name) values ('00000000-0000-0000-0000-0000000000d1', '00000000-0000-0000-0000-0000000000c1', 'Riya');
-- Kabir is in his 24-hour trial (replaced by the longer school seat)
insert into studyverse.course_access (user_id, course, valid_until, note) values ('00000000-0000-0000-0000-0000000000c2', 'school-g7', now() + interval '20 hours', 'trial');
insert into studyverse.progress (user_id, state, updated_at) values
  ('00000000-0000-0000-0000-0000000000c1', jsonb_build_object('st', jsonb_build_object('profile', jsonb_build_object('name', 'Riya Sharma', 'grade', 7),
     'ins', jsonb_build_object('day', jsonb_build_object(to_char((now() at time zone 'Asia/Kolkata')::date, 'YYYY-MM-DD'), jsonb_build_object('a', 12, 'r', 9),
                                                          to_char((now() at time zone 'Asia/Kolkata')::date - 3, 'YYYY-MM-DD'), jsonb_build_object('a', 5, 'r', 4),
                                                          to_char((now() at time zone 'Asia/Kolkata')::date - 20, 'YYYY-MM-DD'), jsonb_build_object('a', 50, 'r', 50))))), now()),
  ('00000000-0000-0000-0000-0000000000c2', jsonb_build_object('st', jsonb_build_object('profile', jsonb_build_object('name', 'Kabir', 'grade', 7),
     'ins', jsonb_build_object('day', jsonb_build_object(to_char((now() at time zone 'Asia/Kolkata')::date, 'YYYY-MM-DD'), jsonb_build_object('a', 20, 'r', 20))))), now());
select pg_temp.set_billing(null, 'Maharashtra');

set local role authenticated;
do $$
declare O uuid := '00000000-0000-0000-0000-00000000000a'; P uuid := '00000000-0000-0000-0000-0000000000a1';
  T7 uuid := '00000000-0000-0000-0000-0000000000b1'; T8 uuid := '00000000-0000-0000-0000-0000000000b2';
  RIYA uuid := '00000000-0000-0000-0000-0000000000c1'; KAB uuid := '00000000-0000-0000-0000-0000000000c2'; MEE uuid := '00000000-0000-0000-0000-0000000000c3';
  OTH uuid := '00000000-0000-0000-0000-0000000000c4'; MUM uuid := '00000000-0000-0000-0000-0000000000d1'; DAD uuid := '00000000-0000-0000-0000-0000000000d2';
  P2 uuid := '00000000-0000-0000-0000-0000000000e1';
  j jsonb; I uuid; I2 uuid; C7 uuid; C8 uuid; CA1 uuid; X uuid; k text; kt text; o1 uuid; o2 uuid; n int; r record; ca studyverse.course_access;
begin
  -- ===================== pricing (pure) =====================
  perform pg_temp.as_user(P);
  j := studyverse.quote_order('[{"band":"1-5","students":29}]');
  perform pg_temp.chk(not (j ->> 'ok')::boolean and j ->> 'code' = 'min' and (j ->> 'students')::int = 29, 'min: 29 students refused');
  j := studyverse.quote_order('[{"band":"1-5","students":20},{"band":"6-8","students":9}]');
  perform pg_temp.chk(j ->> 'code' = 'min', 'min: 20+9 = 29 across bands refused');
  -- 30 × ₹100 × 10 = ₹30,000; no discount; no GSTIN → GST 0
  j := studyverse.quote_order('[{"band":"1-5","students":30}]');
  perform pg_temp.chk((j ->> 'ok')::boolean and (j ->> 'subtotal')::numeric = 30000 and (j ->> 'discount_pct')::int = 0 and (j ->> 'total')::numeric = 30000, 'quote 30 × Class 1–5 = ₹30,000');
  perform pg_temp.chk(j -> 'gst' ->> 'mode' = 'none' and j -> 'gst' ->> 'note' = 'GST: not charged — supplier not registered under GST', 'no seller GSTIN → GST not charged note');
  perform pg_temp.chk((j -> 'lines' -> 0 ->> 'months')::int = 10 and (j -> 'lines' -> 0 ->> 'rate')::int = 100 and (j ->> 'per_student_month')::numeric = 100, 'line: rate 100, 10 months, ₹100/student/month');
  -- 99 students: 99 × 125 × 10 = 1,23,750, still no discount
  j := studyverse.quote_order('[{"band":"6-8","students":99}]');
  perform pg_temp.chk((j ->> 'total')::numeric = 123750 and (j ->> 'discount_pct')::int = 0, '99 × Class 6–8 = ₹1,23,750, no discount');
  -- 100: 60 × 125 × 10 = 75,000 + 40 × 175 × 10 = 70,000 → 1,45,000; 10% = 14,500 → 1,30,500
  j := studyverse.quote_order('[{"band":"6-8","students":60},{"band":"9-10","students":40}]');
  perform pg_temp.chk((j ->> 'subtotal')::numeric = 145000 and (j ->> 'discount_pct')::int = 10 and (j ->> 'discount_amt')::numeric = 14500 and (j ->> 'total')::numeric = 130500, '100 students mixed: ₹1,45,000 − 10% = ₹1,30,500');
  perform pg_temp.chk(jsonb_array_length(j -> 'lines') = 2 and j -> 'lines' -> 1 ->> 'label' = 'Class 9–10' and (j -> 'lines' -> 1 ->> 'amount')::numeric = 70000, 'line items returned per band');
  -- same band twice is added: 50 + 50 Class 11–12 = 100 × 225 × 10 = 2,25,000 − 10% = 2,02,500
  j := studyverse.quote_order('[{"band":"11-12","students":50},{"band":"11-12","students":50}]');
  perform pg_temp.chk(jsonb_array_length(j -> 'lines') = 1 and (j ->> 'total')::numeric = 202500, 'same band merged: 100 × Class 11–12 → ₹2,02,500');
  -- 499 vs 500 CA: 499 × 250 × 10 = 12,47,500 − 10% = 11,22,750 ; 500 → 12,50,000 − 20% = 10,00,000
  j := studyverse.quote_order('[{"band":"ca","students":499}]');
  perform pg_temp.chk((j ->> 'total')::numeric = 1122750 and (j ->> 'discount_pct')::int = 10, '499 CA = ₹11,22,750 (10%)');
  j := studyverse.quote_order('[{"band":"ca","students":500}]');
  perform pg_temp.chk((j ->> 'total')::numeric = 1000000 and (j ->> 'discount_pct')::int = 20, '500 CA = ₹10,00,000 (20%)');
  -- 1000 Class 11–12: 22,50,000 − 30% (6,75,000) = 15,75,000
  j := studyverse.quote_order('[{"band":"11-12","students":1000}]');
  perform pg_temp.chk((j ->> 'total')::numeric = 1575000 and (j ->> 'discount_amt')::numeric = 675000, '1000 × Class 11–12 = ₹15,75,000 (30%)');
  j := studyverse.quote_order('[{"band":"13-14","students":40}]'); perform pg_temp.chk(j ->> 'code' = 'bad', 'unknown band refused');
  j := studyverse.quote_order('[{"band":"1-5","students":-4}]'); perform pg_temp.chk(j ->> 'code' = 'bad', 'negative count refused');
  j := studyverse.quote_order('[]'); perform pg_temp.chk(j ->> 'code' = 'empty', 'empty order refused');
  perform pg_temp.as_user(null); perform set_config('request.jwt.claims', '', true);
  j := studyverse.quote_order('[{"band":"1-5","students":30}]'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'quote needs sign-in');
  perform pg_temp.chk(studyverse._inst_ay('2026-11-09T10:00:00+05:30') = '2026-27' and studyverse._inst_ay('2027-02-01T10:00:00+05:30') = '2026-27' and studyverse._inst_ay('2027-04-01T00:30:00+05:30') = '2027-28', 'academic year Apr–Mar');
  perform pg_temp.chk(studyverse._inst_ay_end('2026-27') = '2027-03-31T23:59:59+05:30'::timestamptz, 'academic year ends 31 Mar 23:59:59 IST');
  perform pg_temp.chk(studyverse._inst_band('school-g5') = '1-5' and studyverse._inst_band('school-g6') = '6-8' and studyverse._inst_band('school-g10') = '9-10' and studyverse._inst_band('school-g11') = '11-12' and studyverse._inst_band('ca-foundation') = 'ca', 'bands by class');

  -- ===================== owner creates the institution =====================
  perform pg_temp.as_user(P); j := studyverse.owner_create_institution('{"name":"Sunrise School"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'non-owner cannot create an institution');
  perform pg_temp.as_user(O);
  j := studyverse.owner_create_institution('{"name":"Sunrise School","type":"school","city":"Pune","state":"Maharashtra","board":"CBSE","gstin":"27abcde1234f1z5","contact_email":"Head@Sunrise.test"}');
  I := (j ->> 'id')::uuid; perform pg_temp.chk((j ->> 'ok')::boolean and I is not null, 'owner creates Sunrise School');
  perform pg_temp.chk((pg_temp.inst(I)).gstin = '27ABCDE1234F1Z5' and (pg_temp.inst(I)).contact_email = 'head@sunrise.test' and (pg_temp.inst(I)).status = 'pilot', 'GSTIN upper-cased, email lower-cased, status pilot');
  j := studyverse.owner_create_institution('{"name":"Bad","gstin":"12345"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bad buyer GSTIN refused');
  j := studyverse.owner_create_institution('{"name":"Other Academy","type":"coaching","state":"Karnataka"}'); I2 := (j ->> 'id')::uuid;
  -- first admins (edge function institution-bulk does this with the service role after making the account)
  j := pg_temp.svc_add(I, P, 'admin', null, null, 'Mrs Rao'); perform pg_temp.chk((j ->> 'ok')::boolean, 'principal added as admin');
  j := pg_temp.svc_add(I2, P2, 'admin', null, null, null);
  j := pg_temp.svc_staff(T7, I, 'teacher'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'staff invite: a non-admin is refused');
  j := pg_temp.svc_staff(P, I, 'teacher'); perform pg_temp.chk((j ->> 'ok')::boolean and j ->> 'institution' = 'Sunrise School', 'staff invite: admin allowed');

  -- ===================== admin: classes, teachers, codes =====================
  perform pg_temp.as_user(P);
  j := studyverse.inst_save_class(I, null, 'class', 7, 'b'); C7 := (j ->> 'id')::uuid; perform pg_temp.chk(j ->> 'name' = '7-B', 'class 7-B made (section upper-cased)');
  j := studyverse.inst_save_class(I, null, 'class', 7, 'B'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'duplicate 7-B refused');
  j := studyverse.inst_save_class(I, null, 'class', 13, 'A'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'class 13 refused');
  j := studyverse.inst_save_class(I, null, 'class', 8, 'A'); C8 := (j ->> 'id')::uuid;
  j := studyverse.inst_save_class(I, null, 'batch', null, 'Morning'); CA1 := (j ->> 'id')::uuid; perform pg_temp.chk(j ->> 'name' = 'CA Foundation · Morning', 'CA batch made');
  perform pg_temp.as_user(P2); j := studyverse.inst_save_class(I, null, 'class', 5, 'A'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'admin of another institution cannot add classes');
  perform pg_temp.as_user(P);
  j := studyverse.inst_create_code(I, null, 'teacher', 7, 5); kt := j ->> 'code'; perform pg_temp.chk(kt ~ '^[A-Z0-9]{8}$', 'teacher code made');
  j := studyverse.inst_create_code(I, C7, 'student', 30, 100); k := j ->> 'code'; perform pg_temp.chk(k ~ '^[A-Z0-9]{8}$', 'class code for 7-B made');
  j := studyverse.inst_create_code(I, null, 'student', 30, 100); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'student code needs a class');
  -- teachers join with the teacher code, admin assigns classes
  perform pg_temp.as_user(T7); j := studyverse.inst_join(kt, 'Mr Iyer'); perform pg_temp.chk((j ->> 'ok')::boolean and j ->> 'role' = 'teacher', 'teacher joins with the teacher code');
  perform pg_temp.as_user(T8); j := studyverse.inst_join(lower(kt)); perform pg_temp.chk((j ->> 'ok')::boolean, 'second teacher joins (code case-insensitive)');
  perform pg_temp.as_user(P);
  j := studyverse.inst_assign_teacher(C7, T7, true); perform pg_temp.chk((j ->> 'ok')::boolean, 'assign teacher to 7-B');
  j := studyverse.inst_assign_teacher(C8, T8, true); j := studyverse.inst_assign_teacher(C7, OTH, true); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'cannot assign a non-teacher');
  perform pg_temp.as_user(T7); j := studyverse.inst_create_code(I, C8, 'student', 30, 100); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'teacher cannot make a code for a class they do not teach');
  j := studyverse.inst_create_code(I, null, 'teacher', 30, 5); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'teacher cannot make teacher codes');

  -- ===================== students join =====================
  perform pg_temp.as_user(MUM); j := studyverse.inst_join(k, 'Mum'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'a parent account cannot join as a student');
  perform pg_temp.as_user(RIYA); j := studyverse.inst_join(k, 'Riya', '12'); perform pg_temp.chk((j ->> 'ok')::boolean and j ->> 'class' = '7-B' and j ->> 'institution' = 'Sunrise School', 'Riya joins 7-B');
  j := studyverse.inst_join(k, 'Riya', '12'); perform pg_temp.chk((j ->> 'already')::boolean, 'joining twice is harmless');
  perform pg_temp.as_user(KAB); j := studyverse.inst_join(k, 'Kabir', '7');
  perform pg_temp.as_user(OTH); j := studyverse.inst_join('ZZZZZZZZ', 'X'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'unknown code refused');
  -- no seats yet: pilot status but no pilot class → nobody gets access; Riya's paid row and Kabir's trial are untouched
  ca := pg_temp.ca(RIYA, 'school-g7'); perform pg_temp.chk(ca.note = 'paid s68-year' and ca.valid_until = '2099-01-01', 'no seat yet: Riya keeps her paid row');
  ca := pg_temp.ca(KAB, 'school-g7'); perform pg_temp.chk(ca.note = 'trial', 'no seat yet: Kabir keeps his trial');
  perform pg_temp.chk(pg_temp.nlinks(RIYA) = 1, 'enrolment keeps the parent link');
  j := studyverse.inst_me(); perform pg_temp.chk(jsonb_array_length(j -> 'memberships') = 0, 'inst_me for a non-member: empty');
  perform pg_temp.as_user(RIYA); j := studyverse.inst_me();
  perform pg_temp.chk(j -> 'memberships' -> 0 ->> 'class_name' = '7-B' and j -> 'memberships' -> 0 ->> 'name' = 'Sunrise School' and j -> 'memberships' -> 0 ->> 'role' = 'student', 'inst_me: student sees school + class (badge)');

  -- ===================== RLS =====================
  perform pg_temp.as_user(T7);
  select count(*) into n from studyverse.institution_members where role = 'student'; perform pg_temp.chk(n = 2, 'teacher 7-B sees the 2 students of 7-B: ' || n);
  select count(*) into n from studyverse.inst_classes; perform pg_temp.chk(n = 1, 'teacher 7-B sees only class 7-B: ' || n);
  j := studyverse.class_progress(C7); perform pg_temp.chk((j ->> 'ok')::boolean and jsonb_array_length(j -> 'students') = 2, 'class_progress: 2 students');
  perform pg_temp.chk((select e ->> 'name' from jsonb_array_elements(j -> 'students') e where (e ->> 'user_id')::uuid = RIYA) = 'Riya'
    and (select (e -> 'state' -> 'profile' ->> 'grade')::int from jsonb_array_elements(j -> 'students') e where (e ->> 'user_id')::uuid = RIYA) = 7
    and (select (e ->> 'parents')::int from jsonb_array_elements(j -> 'students') e where (e ->> 'user_id')::uuid = RIYA) = 1, 'class_progress: name, synced state, parent count');
  j := studyverse.class_progress(C8); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'teacher 7-B cannot read 8-A progress');
  perform pg_temp.as_user(T8);
  select count(*) into n from studyverse.institution_members where role = 'student'; perform pg_temp.chk(n = 0, 'teacher 8-A sees no 7-B students');
  perform pg_temp.as_user(P);
  select count(*) into n from studyverse.institution_members; perform pg_temp.chk(n = 5, 'admin sees all 5 members (1 admin, 2 teachers, 2 students): ' || n);
  select count(*) into n from studyverse.join_codes; perform pg_temp.chk(n = 2, 'admin sees the codes');
  perform pg_temp.as_user(P2);
  select count(*) into n from studyverse.institution_members where institution_id = I; perform pg_temp.chk(n = 0, 'other institution''s admin sees nothing of Sunrise');
  select count(*) into n from studyverse.institutions; perform pg_temp.chk(n = 1, 'other admin sees only their own institution');
  j := studyverse.class_progress(C7); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'other admin cannot read Sunrise progress');
  j := studyverse.inst_overview(I); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'other admin cannot see Sunrise overview');
  perform pg_temp.as_user(RIYA);
  select count(*) into n from studyverse.institution_members; perform pg_temp.chk(n = 1, 'student sees only own membership');
  select count(*) into n from studyverse.join_codes; perform pg_temp.chk(n = 0, 'student cannot read codes');
  select count(*) into n from studyverse.seat_orders; perform pg_temp.chk(n = 0, 'student cannot read orders');
  j := studyverse.class_progress(C7); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'student cannot read class progress');
  perform pg_temp.as_user(O);
  select count(*) into n from studyverse.institutions; perform pg_temp.chk(n = 2, 'owner sees all institutions');
  j := studyverse.class_progress(C7); perform pg_temp.chk((j ->> 'ok')::boolean, 'owner can read class progress');

  -- ===================== pilot =====================
  perform pg_temp.as_user(P); j := studyverse.owner_grant_pilot(I, C7, 30); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'admin cannot grant a pilot');
  perform pg_temp.as_user(O);
  j := studyverse.owner_grant_pilot(I, C7, 31); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'pilot longer than 30 days refused');
  j := studyverse.owner_grant_pilot(I, CA1, 30); perform pg_temp.chk((j ->> 'ok')::boolean, 'pilot can move to another class');
  j := studyverse.owner_grant_pilot(I, C7, 30); perform pg_temp.chk((j ->> 'ok')::boolean, 'owner grants a 30-day pilot for 7-B');
  ca := pg_temp.ca(KAB, 'school-g7'); perform pg_temp.chk(ca.note = 'inst ' || I and ca.valid_until = (pg_temp.inst(I)).pilot_until, 'pilot: Kabir''s trial replaced by the 30-day pilot');
  ca := pg_temp.ca(RIYA, 'school-g7'); perform pg_temp.chk(ca.note = 'paid s68-year' and ca.valid_until = '2099-01-01', 'pilot: Riya''s longer paid plan kept');
  perform pg_temp.as_user(P); j := studyverse.inst_overview(I);
  perform pg_temp.chk((j -> 'seats' -> 1 ->> 'pilot')::int = 2 and (j -> 'seats' -> 1 ->> 'used')::int = 0 and j ->> 'pilot_class' = '7-B', 'overview: 2 pilot students in Class 6–8, 0 paid seats used');

  -- ===================== orders & paid seats =====================
  perform pg_temp.as_user(T7); j := studyverse.create_order(I, '[{"band":"6-8","students":30}]'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'teacher cannot order');
  perform pg_temp.as_user(P);
  j := studyverse.create_order(I, '[{"band":"6-8","students":20}]'); perform pg_temp.chk(j ->> 'code' = 'min', 'order below 30 refused');
  j := studyverse.create_order(I, '[{"band":"6-8","students":30}]', '2030-31'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'far-future academic year refused');
  j := studyverse.create_order(I, '[{"band":"6-8","students":30}]', null, false); o1 := (j ->> 'order_id')::uuid;
  perform pg_temp.chk(j ->> 'status' = 'draft' and j ->> 'invoice_no' is null and (j ->> 'total')::numeric = 37500, 'draft order: 30 × ₹125 × 10 = ₹37,500, no number yet');
  j := studyverse.submit_order(o1); perform pg_temp.chk(j ->> 'status' = 'invoiced' and j ->> 'invoice_no' like 'SV-' || studyverse._inst_ay(now()) || '-%', 'submit → invoiced with number ' || coalesce(j ->> 'invoice_no', '?'));
  j := pg_temp.svc_mail(o1, T7); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'invoice email: teacher refused');
  j := pg_temp.svc_mail(o1, P); perform pg_temp.chk((j ->> 'ok')::boolean and j ->> 'by' = 'principal@t.test', 'invoice email: admin allowed');
  j := pg_temp.svc_mail(o1, P); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'invoice email: once per 10 minutes');
  ca := pg_temp.ca(KAB, 'school-g7'); perform pg_temp.chk(ca.valid_until = (pg_temp.inst(I)).pilot_until, 'invoiced (not paid): still on pilot');
  perform pg_temp.as_user(O); j := studyverse.owner_mark_paid(o1, 'NEFT 123'); perform pg_temp.chk((j ->> 'ok')::boolean, 'owner marks paid');
  perform pg_temp.chk((pg_temp.inst(I)).status = 'active', 'institution is active');
  ca := pg_temp.ca(KAB, 'school-g7'); perform pg_temp.chk(ca.note = 'inst ' || I and ca.valid_until = studyverse._inst_ay_end(studyverse._inst_ay(now())), 'paid: Kabir''s seat runs to 31 March');
  ca := pg_temp.ca(RIYA, 'school-g7'); perform pg_temp.chk(ca.note = 'paid s68-year', 'paid: Riya''s own longer plan still kept');
  j := studyverse.owner_mark_paid(o1, 'again'); perform pg_temp.chk((j ->> 'ok')::boolean, 'marking paid twice is harmless');
  perform pg_temp.as_user(P); j := studyverse.inst_overview(I);
  perform pg_temp.chk((j -> 'seats' -> 1 ->> 'total')::int = 30 and (j -> 'seats' -> 1 ->> 'used')::int = 2 and (j -> 'seats' -> 1 ->> 'pilot')::int = 0, 'overview: Class 6–8 seats 2 used of 30');
  j := studyverse.cancel_order(o1); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'a paid order cannot be cancelled by the admin');
  -- GST on invoices once the seller has a GSTIN (seller Maharashtra; Sunrise is in Maharashtra → CGST + SGST)
  perform pg_temp.set_billing('27AAAAA0000A1Z5', 'Maharashtra');
  j := studyverse.create_order(I, '[{"band":"1-5","students":30}]'); o2 := (j ->> 'order_id')::uuid;
  perform pg_temp.chk(j -> 'gst' ->> 'mode' = 'intra' and (j -> 'gst' ->> 'cgst')::numeric = 2700 and (j -> 'gst' ->> 'sgst')::numeric = 2700 and (j ->> 'total')::numeric = 35400, 'GST intra-state: ₹30,000 + 9% + 9% = ₹35,400');
  perform pg_temp.as_user(P2); j := studyverse.quote_order('[{"band":"ca","students":40}]', I2);
  -- 40 × 250 × 10 = 1,00,000; Karnataka ≠ Maharashtra → IGST 18% = 18,000
  perform pg_temp.chk(j -> 'gst' ->> 'mode' = 'inter' and (j -> 'gst' ->> 'igst')::numeric = 18000 and (j ->> 'total')::numeric = 118000, 'GST inter-state: ₹1,00,000 + IGST 18% = ₹1,18,000');
  perform pg_temp.set_billing(null, 'Maharashtra');
  perform pg_temp.as_user(P); j := studyverse.cancel_order(o2); perform pg_temp.chk((j ->> 'ok')::boolean, 'admin cancels an unpaid order');
  -- seats are limited: a band with 0 paid seats gives nothing (CA batch, no pilot)
  perform pg_temp.as_user(O); X := OTH;
  j := pg_temp.svc_add(I, OTH, 'student', CA1, '1', 'Oz');
  ca := pg_temp.ca(OTH, 'ca-foundation'); perform pg_temp.chk(ca.user_id is null, 'CA batch with no seats: no access row');

  -- ===================== moving and removing =====================
  perform pg_temp.as_user(P);
  j := studyverse.inst_move_student(I, KAB, C8); perform pg_temp.chk((j ->> 'ok')::boolean, 'move Kabir to 8-A');
  ca := pg_temp.ca(KAB, 'school-g7'); perform pg_temp.chk(ca.user_id is null, 'old class seat removed (an old trial is not put back)');
  ca := pg_temp.ca(KAB, 'school-g8'); perform pg_temp.chk(ca.note = 'inst ' || I, 'new seat for Class 8');
  j := studyverse.inst_remove_member(I, RIYA, 'student'); perform pg_temp.chk((j ->> 'ok')::boolean, 'remove Riya from the school');
  ca := pg_temp.ca(RIYA, 'school-g7'); perform pg_temp.chk(ca.note = 'paid s68-year' and ca.valid_until = '2099-01-01', 'after removal Riya still has her own paid plan');
  perform pg_temp.chk(pg_temp.nlinks(RIYA) = 1, 'after removal the parent link is still there');
  j := studyverse.inst_remove_member(I, P, 'admin'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'the only admin cannot remove themselves');
  j := studyverse.inst_delete_class(C8); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'class with students cannot be deleted');
  -- seats end when the academic year order expires
  perform pg_temp.age_order(o1); perform pg_temp.as_user(O); perform studyverse.owner_end_pilot(I);
  ca := pg_temp.ca(KAB, 'school-g8'); perform pg_temp.chk(ca.user_id is null, 'expired order + ended pilot: seat removed');
  perform pg_temp.chk((pg_temp.inst(I)).status = 'expired', 'institution status expired');

  -- ===================== homework =====================
  perform pg_temp.as_user(P); j := studyverse.inst_move_student(I, KAB, C7);
  perform pg_temp.as_user(T7);
  j := studyverse.inst_set_homework(C7, 'chapter', '7-maths-3', 'Fractions practice', 'Maths', (now() at time zone 'Asia/Kolkata')::date + 3);
  X := (j ->> 'id')::uuid; perform pg_temp.chk((j ->> 'ok')::boolean, 'teacher sets homework');
  j := studyverse.inst_set_homework(C7, 'chapter', '7-maths-3', 'Old', 'Maths', (now() at time zone 'Asia/Kolkata')::date - 1); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'due date in the past refused');
  j := studyverse.inst_set_homework(C7, 'chapter', 'drop table', 'x', null, (now() at time zone 'Asia/Kolkata')::date); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bad target refused');
  perform pg_temp.as_user(T8); j := studyverse.inst_set_homework(C7, 'chapter', '7-maths-3', 'x', null, (now() at time zone 'Asia/Kolkata')::date); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'other teacher cannot set 7-B homework');
  perform pg_temp.as_user(KAB); j := studyverse.my_homework();
  perform pg_temp.chk(jsonb_array_length(j) = 1 and j -> 0 ->> 'title' = 'Fractions practice' and j -> 0 ->> 'done_at' is null and (j -> 0 ->> 'need')::int = 3, 'student sees homework (need 3)');
  j := studyverse.homework_done(X); j := studyverse.my_homework(); perform pg_temp.chk(j -> 0 ->> 'done_at' is not null, 'student marks homework done');
  perform pg_temp.as_user(MEE); j := studyverse.homework_done(X); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'non-member cannot mark homework');
  j := studyverse.my_homework(); perform pg_temp.chk(jsonb_array_length(j) = 0, 'non-member sees no homework');
  perform pg_temp.as_user(T7); j := studyverse.class_progress(C7);
  perform pg_temp.chk(jsonb_array_length(j -> 'homework') = 1 and (j -> 'students' -> 0 -> 'hw') ? X::text, 'teacher sees homework + completion');

  -- ===================== leaderboard (opt-in) =====================
  perform pg_temp.as_user(KAB); j := studyverse.class_leaderboard(C7); perform pg_temp.chk(jsonb_array_length(j -> 'rows') = 0, 'leaderboard empty until someone opts in');
  j := studyverse.inst_set_leaderboard(true); j := studyverse.class_leaderboard(C7);
  -- Kabir: 20 right today
  perform pg_temp.chk(jsonb_array_length(j -> 'rows') = 1 and j -> 'rows' -> 0 ->> 'name' = 'Kabir' and (j -> 'rows' -> 0 ->> 'score')::int = 20 and (j -> 'rows' -> 0 ->> 'me')::boolean, 'opted-in: first name + 20 correct this week');
  perform pg_temp.as_user(MEE); j := studyverse.class_leaderboard(C7); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'outsider cannot see the leaderboard');

  -- ===================== bulk upload + parent emails =====================
  j := pg_temp.svc_bulk(T7, I, '[{"name":"A","class":"7","section":"B"}]'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bulk: teacher refused');
  j := pg_temp.svc_bulk(P, I, '[{"name":"Meera","class":"7","section":"B","roll":"21","email":"meera@t.test","parent_email":"dad@t.test"},
                                {"name":"Arun","class":"9","section":"c","roll":"4","parent_email":"arunmum@t.test"},
                                {"name":"","class":"7","section":"B"},
                                {"name":"Zed","class":"14","section":"B"},
                                {"name":"Kim","class":"CA","section":"Evening","roll":"1"},
                                {"name":"Bad","class":"7","email":"bad@"}]');
  perform pg_temp.chk((j ->> 'ok')::boolean and jsonb_array_length(j -> 'invites') = 1 and jsonb_array_length(j -> 'codes') = 2 and jsonb_array_length(j -> 'errors') = 3, 'bulk: 1 invite, 2 roll codes, 3 row errors');
  perform pg_temp.chk((j ->> 'classes_created')::int = 2 and j -> 'codes' -> 0 ->> 'class_name' = '9-C' and j -> 'codes' -> 1 ->> 'class_name' = 'CA Foundation · Evening', 'bulk: classes 9-C and CA Evening made');
  k := j -> 'codes' -> 0 ->> 'code';
  j := pg_temp.svc_bulk(P, I, '[{"name":"Arun","class":"9","section":"C","roll":"4"}]');
  perform pg_temp.chk(j -> 'codes' -> 0 ->> 'code' = k, 'bulk: re-upload reuses the same roll code');
  -- the edge function then makes Meera's account and adds her (service role)
  j := pg_temp.svc_add(I, MEE, 'student', C7, '21', 'Meera'); perform pg_temp.chk((j ->> 'ok')::boolean and pg_temp.pinv('dad@t.test') = MEE, 'bulk email student added; parent invite now knows the child');
  -- Arun signs up on his phone with the roll code
  perform pg_temp.as_user(OTH); j := studyverse.inst_join(k, 'whatever');
  perform pg_temp.chk((j ->> 'ok')::boolean and j ->> 'class' = '9-C' and pg_temp.pinv('arunmum@t.test') = OTH, 'roll code joins 9-C; parent invite gets the child');
  perform pg_temp.as_user(T7); j := studyverse.inst_join(k); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'a roll code works only once');
  perform pg_temp.as_user(P); select display_name into r from studyverse.institution_members where user_id = OTH and role = 'student' and institution_id = I;
  perform pg_temp.chk(r.display_name = 'Arun', 'roll code keeps the school''s name for the student');
  -- Dad signs in → linked to Meera in Parent Hub
  perform pg_temp.as_user(DAD); j := studyverse.inst_claim(); perform pg_temp.chk((j ->> 'linked')::int = 1 and pg_temp.nlinks(MEE) = 1, 'parent signs in → Parent Hub link to Meera');
  j := studyverse.inst_claim(); perform pg_temp.chk((j ->> 'linked')::int = 0, 'claim is once only');
  perform pg_temp.as_user(RIYA); j := studyverse.inst_claim(); perform pg_temp.chk((j ->> 'linked')::int = 0, 'a student account claims nothing');

  -- ===================== pilot request form (service) =====================
  j := pg_temp.svc_pilot('{"name":"A","school":"S","phone":"9","email":"a@b.co","students":"120"}', 'ip1');
  perform pg_temp.chk((j ->> 'ok')::boolean, 'pilot request saved');
  j := pg_temp.svc_pilot('{"name":"A"}', 'ip1'); j := pg_temp.svc_pilot('{"name":"A"}', 'ip1'); j := pg_temp.svc_pilot('{"name":"A"}', 'ip1');
  perform pg_temp.chk(j ->> 'code' = 'limit', 'pilot request: 4th from the same IP within an hour is limited');

  -- ===================== owner panel lists =====================
  perform pg_temp.as_user(O);
  j := studyverse.owner_list_institutions(); perform pg_temp.chk(jsonb_array_length(j) = 2 and (j -> 1 ->> 'name') = 'Sunrise School' or (j -> 0 ->> 'name') = 'Sunrise School', 'owner lists institutions');
  j := studyverse.owner_list_orders(); perform pg_temp.chk(jsonb_array_length(j) = 2, 'owner lists non-draft orders (paid + cancelled)');
  j := studyverse.owner_set_billing('{"gstin":"bad","state":"Maharashtra"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'owner: bad seller GSTIN refused');
  j := studyverse.owner_set_billing('{"gstin":"27aaaaa0000a1z5","state":"Maharashtra"}'); perform pg_temp.chk((j ->> 'ok')::boolean, 'owner sets seller GSTIN');
  perform pg_temp.as_user(P); j := studyverse.owner_set_billing('{"gstin":null,"state":"Goa"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'admin cannot change seller config');
  j := studyverse.owner_list_institutions(); perform pg_temp.chk(jsonb_array_length(j) = 0, 'admin gets nothing from owner list');
  -- direct writes are blocked (no insert/update grants)
  begin insert into studyverse.institution_members (institution_id, user_id, role) values (I, MEE, 'admin'); perform pg_temp.chk(false, 'direct insert blocked');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'direct insert into members is blocked'); end;
  begin update studyverse.seat_orders set status = 'paid'; perform pg_temp.chk(false, 'direct update blocked');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'direct update of orders is blocked'); end;
end $$;

reset role;
do $$ begin
  raise notice '% checks, % failed', current_setting('ittest.n'), current_setting('ittest.fails');
  if current_setting('ittest.fails')::int > 0 then raise exception 'institutions tests FAILED'; end if;
end $$;
rollback;
