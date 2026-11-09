-- ============================================================================================
-- SQL tests for supabase/migrations/20261110_fields.sql (strict PIN / phone / email / board on the server).
-- Run AFTER 20261109_institutions.sql and 20261110_fields.sql, as a superuser:
--   psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/fields_test.sql
-- Everything is inside BEGIN … ROLLBACK. Each check prints PASS / FAIL; the script ends with an ERROR if any failed.
-- ============================================================================================
begin;
select set_config('fdtest.fails', '0', true), set_config('fdtest.n', '0', true);
create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('fdtest.n', (current_setting('fdtest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('fdtest.fails', (current_setting('fdtest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
create function pg_temp.inst(i uuid) returns studyverse.institutions language sql security definer as $$ select * from studyverse.institutions where id = i $$;
create function pg_temp.svc_pilot(p jsonb, ip text) returns jsonb language sql security definer as $$ select studyverse._pilot_request(p, ip) $$;
create function pg_temp.last_pilot() returns studyverse.pilot_requests language sql security definer as $$ select * from studyverse.pilot_requests order by id desc limit 1 $$;
grant execute on all functions in schema pg_temp to authenticated;

insert into auth.users (id, email) values ('00000000-0000-0000-0000-0000000f000a', 'fowner@t.test'), ('00000000-0000-0000-0000-0000000f00a1', 'fprincipal@t.test');
insert into studyverse.admins (user_id) values ('00000000-0000-0000-0000-0000000f000a');

do $$
declare O uuid := '00000000-0000-0000-0000-0000000f000a'; P uuid := '00000000-0000-0000-0000-0000000f00a1'; j jsonb; I uuid; r studyverse.institutions; q studyverse.pilot_requests; ok boolean;
begin
  -- ===================== pure helpers =====================
  perform pg_temp.chk(studyverse._fld_pin_ok('411001') and not studyverse._fld_pin_ok('011001') and not studyverse._fld_pin_ok('41100') and not studyverse._fld_pin_ok('4110011') and not studyverse._fld_pin_ok('41a001'), 'PIN: 6 digits, first 1–9');
  perform pg_temp.chk(studyverse._fld_phone_ok('+919876543210') and studyverse._fld_phone_ok('+14155550123') and studyverse._fld_phone_ok('+971501234567'), 'phone: valid E.164 accepted');
  perform pg_temp.chk(not studyverse._fld_phone_ok('+915876543210') and not studyverse._fld_phone_ok('+9198765432101') and not studyverse._fld_phone_ok('+91987654321'), 'phone: +91 must be 10 digits starting 6–9');
  perform pg_temp.chk(not studyverse._fld_phone_ok('9876543210') and not studyverse._fld_phone_ok('+0123456789') and not studyverse._fld_phone_ok('+12345') and not studyverse._fld_phone_ok('+1234567890123456'), 'phone: not E.164 refused');
  perform pg_temp.chk(studyverse._fld_phone_norm('98765 43210') = '+919876543210' and studyverse._fld_phone_norm('098765-43210') = '+919876543210'
    and studyverse._fld_phone_norm('91 98765 43210') = '+919876543210' and studyverse._fld_phone_norm('0044 20 7946 0958') = '+442079460958'
    and studyverse._fld_phone_norm('+1 (415) 555-0123') = '+14155550123' and studyverse._fld_phone_norm('  ') is null, 'phone: friendly input normalised to E.164');
  perform pg_temp.chk(studyverse._fld_email_ok('name@school.com') and studyverse._fld_email_ok('a.b+c@mail.co.in') and studyverse._fld_email_ok('o''brien@x.ie'), 'email: good shapes accepted');
  perform pg_temp.chk(not studyverse._fld_email_ok('name@school') and not studyverse._fld_email_ok('name school@x.com') and not studyverse._fld_email_ok('a..b@x.com')
    and not studyverse._fld_email_ok('@x.com') and not studyverse._fld_email_ok('a@-x.com') and not studyverse._fld_email_ok('a@x.c') and not studyverse._fld_email_ok('Name@School.com'), 'email: bad shapes (and upper case, which callers lower first) refused');
  perform pg_temp.chk(studyverse._fld_board_ok('CBSE') and studyverse._fld_board_ok('State board: Jammu & Kashmir') and studyverse._fld_board_ok(null)
    and not studyverse._fld_board_ok('<script>') and not studyverse._fld_board_ok(repeat('x', 61)), 'board: list values ok, junk refused');

  -- ===================== owner creates an institution =====================
  perform pg_temp.as_user(O);
  j := studyverse.owner_create_institution('{"name":"Green Valley School","city":"Pune","state":"Maharashtra","board":"State board: Maharashtra","pincode":"411001","contact_phone":"98765 43210","contact_email":" Head@GreenValley.EDU.in "}');
  perform pg_temp.chk((j ->> 'ok')::boolean, 'create institution with PIN, board, phone, email'); I := (j ->> 'id')::uuid;
  r := pg_temp.inst(I);
  perform pg_temp.chk(r.pincode = '411001' and r.board = 'State board: Maharashtra' and r.contact_phone = '+919876543210' and r.contact_email = 'head@greenvalley.edu.in', 'stored normalised: E.164 phone, lower-case email');
  j := studyverse.owner_create_institution('{"name":"X School","pincode":"011001"}');  perform pg_temp.chk(not (j ->> 'ok')::boolean and j ->> 'msg' ilike '%PIN%', 'PIN starting 0 refused');
  j := studyverse.owner_create_institution('{"name":"X School","pincode":"41100"}');   perform pg_temp.chk(not (j ->> 'ok')::boolean, '5-digit PIN refused');
  j := studyverse.owner_create_institution('{"name":"X School","contact_phone":"5876543210"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean and j ->> 'msg' ilike '%6, 7, 8 or 9%', 'Indian number starting 5 refused');
  j := studyverse.owner_create_institution('{"name":"X School","contact_phone":"+9198765432101"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, '11-digit Indian number refused');
  j := studyverse.owner_create_institution('{"name":"X School","contact_phone":"12ab"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'garbage phone refused');
  j := studyverse.owner_create_institution('{"name":"X School","contact_email":"head@school"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean and j ->> 'msg' ilike '%email%', 'bad email refused');
  j := studyverse.owner_create_institution('{"name":"X School","board":"<b>bad</b>"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'junk board refused');
  j := studyverse.owner_create_institution('{"name":"Dubai Coaching","type":"coaching","contact_phone":"+971 50 123 4567"}');
  perform pg_temp.chk((j ->> 'ok')::boolean and (pg_temp.inst((j ->> 'id')::uuid)).contact_phone = '+971501234567', 'foreign number with country code stored as E.164');
  j := studyverse.owner_create_institution('{"name":"Old Style School"}'); perform pg_temp.chk((j ->> 'ok')::boolean, 'old payload without the new fields still works');

  -- ===================== admin edits details =====================
  insert into studyverse.institution_members (institution_id, user_id, role) values (I, P, 'admin');
  perform pg_temp.as_user(P);
  j := studyverse.inst_update_details(I, '{"name":"Green Valley School","pincode":"560 001","board":"CBSE","contact_phone":"+447911123456","contact_email":"office@gv.in"}');
  r := pg_temp.inst(I);
  perform pg_temp.chk((j ->> 'ok')::boolean and r.pincode = '560001' and r.board = 'CBSE' and r.contact_phone = '+447911123456', 'admin saves details (PIN spaces removed, UK phone kept)');
  j := studyverse.inst_update_details(I, '{"name":"Green Valley School","pincode":"56001"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean and (pg_temp.inst(I)).pincode = '560001', 'bad PIN on edit refused, old value kept');
  j := studyverse.inst_update_details(I, '{"name":"Green Valley School","contact_email":"office@@gv.in"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bad email on edit refused');
  j := studyverse.inst_update_details(I, '{"name":"Green Valley School","contact_phone":"+91 12345 67890"}'); perform pg_temp.chk(not (j ->> 'ok')::boolean, '+91 landline-style number refused');
  j := studyverse.inst_update_details(I, '{"name":"Green Valley School","pincode":"","contact_phone":"","contact_email":""}');
  r := pg_temp.inst(I); perform pg_temp.chk((j ->> 'ok')::boolean and r.pincode is null and r.contact_phone is null and r.contact_email is null, 'empty optional fields are cleared');

  -- the table itself refuses a bad PIN (even for the service role / direct SQL)
  begin update studyverse.institutions set pincode = '012345' where id = I; ok := false; exception when check_violation then ok := true; end;
  perform pg_temp.chk(ok, 'table check: PIN 012345 refused');

  -- ===================== pilot request =====================
  j := pg_temp.svc_pilot('{"name":"Asha","school":"Sunrise","city":"Jaipur","pincode":"302001","board":"State board: Rajasthan","phone":"+919812345678","email":"Asha@Sunrise.in","students":"240"}', 'fip1');
  q := pg_temp.last_pilot();
  perform pg_temp.chk((j ->> 'ok')::boolean and q.pincode = '302001' and q.board = 'State board: Rajasthan' and q.phone = '+919812345678' and q.email = 'asha@sunrise.in' and q.students = 240, 'pilot request stores PIN, board, E.164 phone, lower-case email');
  j := pg_temp.svc_pilot('{"name":"B","phone":"12345","email":"b@x.com"}', 'fip2');      perform pg_temp.chk(j ->> 'field' = 'phone', 'pilot: bad phone refused');
  j := pg_temp.svc_pilot('{"name":"B","phone":"+919812345678","email":"b@x"}', 'fip2');  perform pg_temp.chk(j ->> 'field' = 'email', 'pilot: bad email refused');
  j := pg_temp.svc_pilot('{"name":"B","pincode":"0123456"}', 'fip2');                      perform pg_temp.chk(j ->> 'field' = 'pincode', 'pilot: bad PIN refused');
  j := pg_temp.svc_pilot('{"name":"B","board":"<x>"}', 'fip2');                            perform pg_temp.chk(j ->> 'field' = 'board', 'pilot: junk board refused');
  j := pg_temp.svc_pilot('{"name":"B","students":"12a"}', 'fip2');                         perform pg_temp.chk(j ->> 'field' = 'students', 'pilot: students must be digits');
  begin insert into studyverse.pilot_requests (name, pincode) values ('x', '99999'); ok := false; exception when check_violation then ok := true; end;
  perform pg_temp.chk(ok, 'table check: pilot PIN 99999 refused');

  -- ===================== permissions =====================
  perform pg_temp.chk(not has_function_privilege('anon', 'studyverse._pilot_request(jsonb, text)', 'execute') and not has_function_privilege('authenticated', 'studyverse._pilot_request(jsonb, text)', 'execute'), '_pilot_request is service-only');
  perform pg_temp.chk(has_function_privilege('authenticated', 'studyverse.inst_update_details(uuid, jsonb)', 'execute') and has_function_privilege('authenticated', 'studyverse.owner_create_institution(jsonb)', 'execute'), 'signed-in RPCs still callable');
end $$;

do $$ begin
  raise notice '% checks, % failed', current_setting('fdtest.n'), current_setting('fdtest.fails');
  if current_setting('fdtest.fails')::int > 0 then raise exception 'fields tests FAILED'; end if;
end $$;
rollback;
