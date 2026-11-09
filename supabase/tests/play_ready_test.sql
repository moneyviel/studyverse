-- ============================================================================================
-- SQL tests for supabase/migrations/20261113_play_ready.sql (consent records, adults-only reading, parent controls
-- enforced on the server, report & block, owner reports + Pulse items, account-deletion clean-up).
-- Run AFTER every earlier migration and 20261113_play_ready.sql, as a superuser:
--     psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/play_ready_test.sql
-- Everything is inside BEGIN … ROLLBACK. Each check prints PASS / FAIL as a NOTICE; the script ends with an ERROR if any
-- failed. Calls run as role "authenticated" with request.jwt.claims (like PostgREST).
-- ============================================================================================
begin;
select set_config('prtest.fails', '0', true), set_config('prtest.n', '0', true);
create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('prtest.n', (current_setting('prtest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('prtest.fails', (current_setting('prtest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
-- raw helpers that bypass RLS (test only)
create function pg_temp.n_consents(u uuid, k text) returns int language sql security definer as $$ select count(*)::int from studyverse.consents where subject_id = u and kind = k $$;
create function pg_temp.adult_at(u uuid) returns timestamptz language sql security definer as $$ select adult_confirmed_at from studyverse.profiles where user_id = u $$;
create function pg_temp.code(u uuid) returns text language sql security definer as $$ select code from studyverse.squad_profile where user_id = u $$;
create function pg_temp.befriend(x uuid, y uuid) returns void language sql security definer as $$
  insert into studyverse.squad_friends (a, b, requested_by, status, accepted_at) values (least(x, y), greatest(x, y), x, 'accepted', now()) on conflict do nothing $$;
create function pg_temp.pair(x uuid, y uuid) returns text language sql security definer as $$ select status from studyverse.squad_friends where a = least(x, y) and b = greatest(x, y) $$;
create function pg_temp.n_reports(u uuid) returns int language sql security definer as $$ select count(*)::int from studyverse.reports where reporter = u $$;
create function pg_temp.last_detail(u uuid) returns text language sql security definer as $$ select detail from studyverse.reports where reporter = u order by id desc limit 1 $$;
create function pg_temp.set_version(v text, re boolean) returns void language sql security definer as $$ update studyverse.legal_settings set version = v, needs_reaccept = re where id = 1 $$;
create function pg_temp.del(u uuid) returns jsonb language sql security definer as $$ select studyverse._pr_delete_user_data(u) $$;
create function pg_temp.del_auth(u uuid) returns void language sql security definer as $$ delete from auth.users where id = u $$;
create function pg_temp.pay_users(o text) returns uuid language sql security definer as $$ select user_id from studyverse.payments where order_id = o $$;
create function pg_temp.pay_exists(o text) returns boolean language sql security definer as $$ select exists (select 1 from studyverse.payments where order_id = o) $$;
create function pg_temp.links(p uuid) returns int language sql security definer as $$ select count(*)::int from studyverse.parent_links where parent_id = p or child_id = p $$;
create function pg_temp.room_of(u uuid) returns text language sql security definer as $$ select code from studyverse.room_players where user_id = u order by joined_at desc limit 1 $$;
create function pg_temp.call_base_home() returns jsonb language sql as $$ select studyverse._pr_base_squad_home() $$;
grant execute on all functions in schema pg_temp to authenticated, anon;

-- ---------- fixtures ----------
-- O owner · K1 Riya (retail, Class 7, parent P1) · K2 Kabir (retail) · K3 Meera (retail) · K4 Aarav (school class 7-A)
-- A1 Ananya (CA adult) · P1 parent of K1 · P2 parent linked to nobody
insert into auth.users (id, email, raw_user_meta_data) values
  ('00000000-0000-0000-0000-0000000000f0', 'owner@pr.test', '{}'),
  ('00000000-0000-0000-0000-0000000000f1', 'riya@pr.test', '{"sv_role":"student","sv_consent":{"v":"2.0","g":true}}'),
  ('00000000-0000-0000-0000-0000000000f2', 'kabir@pr.test', '{}'),
  ('00000000-0000-0000-0000-0000000000f3', 'meera@pr.test', '{}'),
  ('00000000-0000-0000-0000-0000000000f4', 'aarav@pr.test', '{}'),
  ('00000000-0000-0000-0000-0000000000f5', 'ananya@pr.test', '{"sv_consent":{"v":"1.0"}}'),
  ('00000000-0000-0000-0000-0000000000e1', 'mum@pr.test', '{}'),
  ('00000000-0000-0000-0000-0000000000e2', 'dad@pr.test', '{}');
insert into studyverse.admins (user_id) values ('00000000-0000-0000-0000-0000000000f0') on conflict do nothing;
insert into studyverse.profiles (user_id, role) values ('00000000-0000-0000-0000-0000000000e1', 'parent'), ('00000000-0000-0000-0000-0000000000e2', 'parent');
insert into studyverse.parent_links (parent_id, child_id, child_name) values ('00000000-0000-0000-0000-0000000000e1', '00000000-0000-0000-0000-0000000000f1', 'Riya');
insert into studyverse.parent_invites (parent_id, email, child_name) values ('00000000-0000-0000-0000-0000000000e2', 'kabir@pr.test', 'Kabir');
insert into studyverse.course_access (user_id, course, valid_until, note) values
  ('00000000-0000-0000-0000-0000000000f1', 'school-g7', now() + interval '30 days', 'paid'),
  ('00000000-0000-0000-0000-0000000000f2', 'school-g7', now() + interval '30 days', 'paid'),
  ('00000000-0000-0000-0000-0000000000f3', 'school-g7', now() + interval '30 days', 'paid');
insert into studyverse.institutions (id, name) values ('10000000-0000-0000-0000-0000000000a1', 'Green Valley School');
insert into studyverse.inst_classes (id, institution_id, grade, section, course, name) values
  ('20000000-0000-0000-0000-0000000000a7', '10000000-0000-0000-0000-0000000000a1', 7, 'A', 'school-g7', 'Class 7-A');
insert into studyverse.institution_members (institution_id, user_id, role, class_id, display_name) values
  ('10000000-0000-0000-0000-0000000000a1', '00000000-0000-0000-0000-0000000000f4', 'student', '20000000-0000-0000-0000-0000000000a7', 'Aarav');
insert into studyverse.plans (id, course, label, months, price_inr, sort) values ('pr-test', 'school', 'Test plan', 1, 199, 99) on conflict (id) do nothing;
insert into studyverse.payments (user_id, plan_id, amount_paise, order_id, status, paid_at) values
  ('00000000-0000-0000-0000-0000000000e2', 'pr-test', 19900, 'order_PRTEST_1', 'paid', now());

set local role authenticated;
do $$
declare O uuid := '00000000-0000-0000-0000-0000000000f0'; K1 uuid := '00000000-0000-0000-0000-0000000000f1'; K2 uuid := '00000000-0000-0000-0000-0000000000f2';
  K3 uuid := '00000000-0000-0000-0000-0000000000f3'; K4 uuid := '00000000-0000-0000-0000-0000000000f4'; A1 uuid := '00000000-0000-0000-0000-0000000000f5';
  P1 uuid := '00000000-0000-0000-0000-0000000000e1'; P2 uuid := '00000000-0000-0000-0000-0000000000e2';
  r jsonb; h jsonb; c text; i int; denied boolean;
begin
  -- ================= 1. consent records =================
  perform pg_temp.as_user(K1);
  r := studyverse.legal_status();
  perform pg_temp.chk((r ->> 'ok')::boolean and (r ->> 'accepted')::boolean and r ->> 'version' = '2.0', 'sign-up tick boxes in user metadata are recorded: accepted v2.0');
  perform pg_temp.chk(pg_temp.n_consents(K1, 'terms') = 1 and pg_temp.n_consents(K1, 'parental') = 1, 'sign-up wrote one terms row and one parental (guardian) row');
  perform studyverse.legal_status();
  perform pg_temp.chk(pg_temp.n_consents(K1, 'terms') = 1, 'calling legal_status again records nothing twice');
  perform pg_temp.as_user(A1);
  r := studyverse.legal_status();
  perform pg_temp.chk(not (r ->> 'accepted')::boolean and pg_temp.n_consents(A1, 'terms') = 0, 'metadata for an OLD version is not counted: the gate shows');
  r := studyverse.accept_terms('1.9', false, 'gate', 'Test agent');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'version' and r ->> 'version' = '2.0', 'accepting a wrong version is refused (returns the current one)');
  r := studyverse.accept_terms('2.0', false, 'gate', repeat('x', 500));
  perform pg_temp.chk((r ->> 'ok')::boolean and (studyverse.legal_status() ->> 'accepted')::boolean, 'accepting v2.0 from the gate: accepted');
  perform studyverse.accept_terms('2.0', false, 'gate', null);
  perform pg_temp.chk(pg_temp.n_consents(A1, 'terms') = 1 and pg_temp.n_consents(A1, 'parental') = 0, 'accepting twice keeps one row; no guardian row without the tick');
  perform pg_temp.as_user(K4);
  r := studyverse.legal_status();
  perform pg_temp.chk(not (r ->> 'parental')::boolean and (r ->> 'school')::boolean, 'school-class student without a parent: parental = false, school = true');
  perform studyverse.accept_terms('2.0', true, 'gate', null);
  r := studyverse.legal_status();
  perform pg_temp.chk((r ->> 'accepted')::boolean and (r ->> 'parental')::boolean, 'school student ticks "my parent/guardian agrees": both recorded');
  -- a new IMPORTANT version: everyone sees the gate again once; a SMALL change: nobody does
  reset role; perform pg_temp.set_version('2.1', true); set local role authenticated;
  perform pg_temp.as_user(A1);
  perform pg_temp.chk(not (studyverse.legal_status() ->> 'accepted')::boolean, 'important new version 2.1: gate shows again');
  reset role; perform pg_temp.set_version('2.1', false); set local role authenticated;
  perform pg_temp.chk((studyverse.legal_status() ->> 'accepted')::boolean, 'small change (needs_reaccept = false): no gate for someone who accepted before');
  reset role; perform pg_temp.set_version('2.0', true); set local role authenticated;
  perform pg_temp.as_user(K2);
  perform pg_temp.chk(not (studyverse.legal_status() ->> 'accepted')::boolean, 'existing user with no record: gate shows once');

  -- ================= 2. adults-only handwriting reading =================
  perform pg_temp.as_user(A1);
  begin perform studyverse.read_allowed(A1); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'read_allowed cannot be called by a signed-in user');
end $$;

do $$
declare A1 uuid := '00000000-0000-0000-0000-0000000000f5'; K4 uuid := '00000000-0000-0000-0000-0000000000f4'; r jsonb;
begin
  reset role;
  perform pg_temp.chk(studyverse.read_allowed(A1) ->> 'why' = 'adult', 'service: not confirmed yet → refused (why = adult)');
  set local role authenticated;
  perform pg_temp.as_user(A1);
  r := studyverse.confirm_adult();
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.adult_at(A1) is not null and pg_temp.n_consents(A1, 'ai_reading') = 1, 'CA student says "I''m 18 or older": stored with time + ai_reading consent');
  perform studyverse.confirm_adult();
  perform pg_temp.chk(pg_temp.n_consents(A1, 'ai_reading') = 1, 'confirming again adds nothing');
  reset role;
  perform pg_temp.chk((studyverse.read_allowed(A1) ->> 'ok')::boolean, 'service: confirmed adult → allowed');
  set local role authenticated;
  perform pg_temp.as_user(K4);
  r := studyverse.confirm_adult();
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'school' and pg_temp.adult_at(K4) is null, 'a school-class student cannot confirm 18+');
  reset role;
  update studyverse.profiles set adult_confirmed_at = now() where user_id = K4;
  insert into studyverse.profiles (user_id, adult_confirmed_at) values (K4, now()) on conflict (user_id) do update set adult_confirmed_at = now();
  perform pg_temp.chk(studyverse.read_allowed(K4) ->> 'why' = 'school', 'service: a school-class student is refused even if marked adult');
  perform pg_temp.chk(studyverse.read_allowed(null) ->> 'why' = 'signin', 'service: no user → refused');
  set local role authenticated;
end $$;

do $$
declare O uuid := '00000000-0000-0000-0000-0000000000f0'; K1 uuid := '00000000-0000-0000-0000-0000000000f1'; K2 uuid := '00000000-0000-0000-0000-0000000000f2';
  K3 uuid := '00000000-0000-0000-0000-0000000000f3'; K4 uuid := '00000000-0000-0000-0000-0000000000f4'; A1 uuid := '00000000-0000-0000-0000-0000000000f5';
  P1 uuid := '00000000-0000-0000-0000-0000000000e1'; P2 uuid := '00000000-0000-0000-0000-0000000000e2';
  r jsonb; h jsonb; c text; c2 text; denied boolean;
begin
  -- ================= 3. parent controls =================
  perform pg_temp.as_user(K1); perform studyverse.squad_sync('{}'::jsonb, 3, null, 'Riya', '🦊', '{"sdk4-easy": 90}', 'school');
  perform pg_temp.as_user(K2); perform studyverse.squad_sync('{}'::jsonb, 4, null, 'Kabir', '🐼', '{"sdk4-easy": 80}', 'school');
  perform pg_temp.as_user(K3); perform studyverse.squad_sync('{}'::jsonb, 0, null, 'Meera', '🐨', null, 'school');
  perform pg_temp.as_user(K1);
  r := studyverse.my_social();
  perform pg_temp.chk((r ->> 'friends')::boolean and (r ->> 'rooms')::boolean and (r ->> 'news')::boolean and (r ->> 'parents')::int = 1, 'child: everything on by default; 1 linked parent');
  r := studyverse.set_child_social(K1, false, false, false);
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'not_parent', 'a child cannot change their own controls');
  perform pg_temp.as_user(P2);
  r := studyverse.set_child_social(K1, false, null, null);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'a parent who is not linked cannot change controls');
  r := studyverse.child_social(K1);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'a parent who is not linked cannot read controls');
  -- friends on: K1 adds K2, K2 accepts
  perform pg_temp.as_user(K1); r := studyverse.squad_add_friend(pg_temp.code(K2));
  perform pg_temp.chk((r ->> 'ok')::boolean and r ->> 'status' = 'pending', 'friends on: request sent');
  perform pg_temp.as_user(K2); r := studyverse.squad_answer(K1, true);
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.pair(K1, K2) = 'accepted', 'friends on: accepted');
  perform pg_temp.as_user(K1); h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 1 and h -> 'social' = '{"friends": true, "rooms": true, "news": true}'::jsonb and h -> 'friends' -> 0 ? 'pz', 'squad_home: friend listed, social flags returned, puzzle times included');
  -- the parent turns friends OFF
  perform pg_temp.as_user(P1);
  r := studyverse.set_child_social(K1, false, null, null);
  perform pg_temp.chk((r ->> 'ok')::boolean and not (r ->> 'friends')::boolean and (r ->> 'rooms')::boolean and (r ->> 'news')::boolean, 'linked parent turns friends off (others unchanged)');
  perform pg_temp.chk(not (studyverse.child_social(K1) ->> 'friends')::boolean, 'parent reads the setting back');
  perform pg_temp.as_user(K1);
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 0 and jsonb_array_length(h -> 'incoming') = 0 and not (h -> 'social' ->> 'friends')::boolean, 'friends off: friends league / list are empty on the server');
  r := studyverse.squad_add_friend(pg_temp.code(K3));
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'parent_off', 'friends off: add friend refused');
  r := studyverse.squad_cheer(K2, 'star');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'parent_off', 'friends off: cheering refused');
  perform pg_temp.as_user(K2);
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 0, 'friends off: Riya is hidden from her friend''s squad too');
  r := studyverse.squad_cheer(K1, 'star');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'friends off: nobody can cheer Riya');
  r := studyverse.squad_add_friend(pg_temp.code(K1));
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'not_allowed', 'friends off: nobody can send Riya a request');
  -- a request waiting for Riya can't be accepted while off (K3 asked before)
  perform pg_temp.as_user(P1); perform studyverse.set_child_social(K1, true, null, null);
  perform pg_temp.as_user(K3); perform studyverse.squad_add_friend(pg_temp.code(K1));
  perform pg_temp.as_user(P1); perform studyverse.set_child_social(K1, false, null, null);
  perform pg_temp.as_user(K1);
  r := studyverse.squad_answer(K3, true);
  perform pg_temp.chk(not (r ->> 'ok')::boolean and pg_temp.pair(K1, K3) = 'pending', 'friends off: accepting a waiting request refused');
  r := studyverse.squad_answer(K3, false);
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.pair(K1, K3) is null, 'friends off: saying no to a request still works');
  -- friends back on: the old friendship returns; news off strips the news fields
  perform pg_temp.as_user(P1); perform studyverse.set_child_social(K1, true, null, false);
  perform pg_temp.as_user(K1); h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 1 and not (h -> 'friends' -> 0 ? 'pz') and not (h -> 'friends' -> 0 ? 'today') and (h -> 'friends' -> 0 ? 'week'), 'news off: friend kept, puzzle times / today''s stars (news) left out');
  perform pg_temp.chk(not (h -> 'social' ->> 'news')::boolean, 'news off: flag returned');
  r := studyverse.squad_cheer(K2, 'star');
  perform pg_temp.chk((r ->> 'ok')::boolean, 'friends on again: cheering works');
  -- rooms
  r := studyverse.create_room('quiz', 'ffa', 5, 10, 'Riya', '🦊', 'school-g7', 'mixed');
  perform pg_temp.chk((r ->> 'ok')::boolean, 'rooms on: create_room works'); c := r ->> 'code';
  perform pg_temp.as_user(P1); perform studyverse.set_child_social(K1, null, false, null);
  perform pg_temp.as_user(K1);
  r := studyverse.create_room('quiz', 'ffa', 5, 10, 'Riya', '🦊', 'school-g7', 'mixed');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'parent_off' and r ->> 'msg' like 'Your parent has turned off live game rooms%', 'rooms off: create_room refused with a kind message');
  perform pg_temp.as_user(K2); r := studyverse.create_room('quiz', 'ffa', 5, 10, 'Kabir', '🐼', 'school-g7', 'mixed'); c2 := r ->> 'code';
  perform pg_temp.as_user(K1);
  r := studyverse.join_room(c2, 'Riya', '🦊', 'school-g7');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'parent_off', 'rooms off: join_room refused');
  r := studyverse.join_room(c, 'Riya', '🦊', 'school-g7');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'rooms off: even re-joining her own old room is refused');
  perform pg_temp.as_user(K3); r := studyverse.join_room(c2, 'Meera', '🐨', 'school-g7');
  perform pg_temp.chk((r ->> 'ok')::boolean, 'other children are not affected');
  -- unlinking the parent: controls no longer apply
  reset role; delete from studyverse.parent_links where child_id = K1; set local role authenticated;
  perform pg_temp.as_user(K1);
  perform pg_temp.chk((studyverse.my_social() ->> 'rooms')::boolean, 'no linked parent → controls do not apply');
  reset role; insert into studyverse.parent_links (parent_id, child_id, child_name) values (P1, K1, 'Riya'); set local role authenticated;
  perform pg_temp.as_user(P1); perform studyverse.set_child_social(K1, true, true, true);

  -- ================= 4. report + block =================
  perform pg_temp.as_user(K2);
  r := studyverse.report_user(K3, 'unkind', 'friend', null, null);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'cannot report someone who is not a friend / request / room player');
  r := studyverse.report_user(K1, 'bad', 'friend', null, null);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'only the preset reasons are accepted');
  r := studyverse.report_user(K1, 'unkind', 'friend', null, 'she said mean things');
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.n_reports(K2) = 1 and pg_temp.last_detail(K2) is null, 'friend reported with a preset reason; free text dropped for a child');
  r := studyverse.report_user(K1, 'cheating', 'friend', null, null);
  perform pg_temp.chk((r ->> 'ok')::boolean and (r ->> 'already')::boolean and pg_temp.n_reports(K2) = 1, 'the same person twice in a day: one report');
  -- room report: K3 and K2 are both in room c2
  perform pg_temp.as_user(K3);
  r := studyverse.report_user(K2, 'name', 'room', c2, null);
  perform pg_temp.chk((r ->> 'ok')::boolean, 'room player reported (both in the room)');
  r := studyverse.report_user(K1, 'name', 'room', c2, null);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'cannot report someone who is not in that room');
  -- adult reporter keeps a short note
  reset role; perform pg_temp.befriend(A1, K3); set local role authenticated;
  perform pg_temp.as_user(A1);
  r := studyverse.report_user(K3, 'other', 'friend', null, '  <b>spam</b> links  ');
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.last_detail(A1) = 'b spam /b  links', 'confirmed adult: short note kept (markup removed)');
  -- rate limit
  reset role;
  insert into studyverse.reports (reporter, reported, context, reason) select K3, A1, 'friend', 'other' from generate_series(1, 9);
  set local role authenticated;
  perform pg_temp.as_user(K3);
  r := studyverse.report_user(A1, 'unkind', 'friend', null, null);
  perform pg_temp.chk((r ->> 'already')::boolean, 'rate limit: same person already reported today');
  reset role; perform pg_temp.befriend(K3, K4); set local role authenticated;
  r := studyverse.report_user(K4, 'unkind', 'friend', null, null);
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'limit', 'rate limit: at most 10 reports a day');
  -- block
  perform pg_temp.as_user(K2);
  r := studyverse.squad_block(K3);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'cannot block a stranger (no friendship or request)');
  r := studyverse.squad_block(K1);
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.pair(K1, K2) is null, 'block removes the friendship');
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 0, 'blocked friend is gone from the squad');
  perform pg_temp.as_user(K1);
  r := studyverse.squad_add_friend(pg_temp.code(K2));
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'not_allowed' and pg_temp.pair(K1, K2) is null, 'the blocked person cannot send a new request');
  r := studyverse.squad_cheer(K2, 'clap');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'the blocked person cannot cheer');
  r := studyverse.report_user(K2, 'unkind', 'friend', null, null);
  perform pg_temp.chk((r ->> 'ok')::boolean, 'a blocked pair can still report');

  -- ================= 5. owner =================
  perform pg_temp.as_user(K1);
  perform pg_temp.chk(studyverse.owner_reports('open', 50) is null, 'students cannot read reports');
  perform pg_temp.as_user(O);
  r := studyverse.owner_reports('open', 50);
  perform pg_temp.chk((r ->> 'ok')::boolean and (r ->> 'open')::int >= 4 and r -> 'rows' -> 0 ? 'reported_email', 'owner sees open reports with emails');
  h := studyverse.owner_dash_smart('{"test": true}'::jsonb);
  perform pg_temp.chk((h ->> 'ok')::boolean and exists (select 1 from jsonb_array_elements(h -> 'items') x where x ->> 'kind' = 'report' and (x ->> 'pri')::int = 1 and x -> 'meta' ? 'reason'), 'Pulse Coach lists reports as urgent items of kind report');
  perform pg_temp.chk((select x ->> 'kind' from jsonb_array_elements(h -> 'items') x limit 1) = 'report', 'reports come first');
  r := studyverse.owner_report_set((select (x -> 'meta' ->> 'rid')::bigint from jsonb_array_elements(h -> 'items') x where x ->> 'kind' = 'report' limit 1), 'done');
  perform pg_temp.chk((r ->> 'ok')::boolean and r ->> 'status' = 'done', 'owner marks a report done');
  perform pg_temp.chk(not exists (select 1 from jsonb_array_elements(studyverse.owner_dash_smart('{"test": true}'::jsonb) -> 'items') x where x -> 'meta' ->> 'rid' = (studyverse.owner_reports('done', 5) -> 'rows' -> 0 ->> 'id')), 'a done report leaves Pulse Coach');
  perform pg_temp.chk(jsonb_array_length(studyverse.owner_reports('done', 50) -> 'rows') = 1, 'done reports listed under done');
  perform pg_temp.as_user(K1);
  perform pg_temp.chk(studyverse.owner_dash_smart('{}'::jsonb) is null, 'students get nothing from Pulse');

  -- ================= 6. originals cannot be called directly =================
  begin perform pg_temp.call_base_home(); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'the renamed original squad_home cannot be called by users (no bypass)');
  begin perform studyverse._pr_delete_user_data(K1); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'users cannot call the deletion clean-up');
end $$;

-- ================= 7. account deletion clean-up (service role) =================
reset role;
do $$
declare O uuid := '00000000-0000-0000-0000-0000000000f0'; K1 uuid := '00000000-0000-0000-0000-0000000000f1'; K2 uuid := '00000000-0000-0000-0000-0000000000f2';
  P1 uuid := '00000000-0000-0000-0000-0000000000e1'; P2 uuid := '00000000-0000-0000-0000-0000000000e2'; r jsonb;
begin
  r := pg_temp.del(O);
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'code' = 'owner', 'owner accounts are not deleted from the app');
  r := pg_temp.del(P1);
  perform pg_temp.chk((r ->> 'ok')::boolean and (r ->> 'children_unlinked')::int = 1 and pg_temp.links(P1) = 0, 'parent deleted: child unlinked');
  r := pg_temp.del(P2);
  perform pg_temp.chk((r ->> 'payments_kept')::int = 1 and pg_temp.pay_users('order_PRTEST_1') is null and pg_temp.pay_exists('order_PRTEST_1'), 'payments kept for tax records with the person removed');
  r := pg_temp.del(K2);
  perform pg_temp.chk(not exists (select 1 from studyverse.parent_invites where email = 'kabir@pr.test'), 'invites addressed to the deleted email are removed');
  perform pg_temp.del_auth(P2); perform pg_temp.del_auth(K2);
  perform pg_temp.chk(pg_temp.pay_exists('order_PRTEST_1'), 'deleting the auth user keeps the payment row (FK on delete set null)');
  perform pg_temp.chk(not exists (select 1 from studyverse.squad_profile where user_id = K2) and not exists (select 1 from studyverse.consents where subject_id = K2),
    'deleting the auth user removes squad profile and consent rows (cascade)');
  perform pg_temp.chk(exists (select 1 from studyverse.reports where reporter is null) , 'reports stay for safety, without the deleted reporter');
end $$;

reset role;
set local role anon;
do $$ declare denied boolean; begin
  begin perform studyverse.legal_status(); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'signed-out visitors cannot call legal_status');
  begin perform studyverse.report_user(null, 'unkind', 'friend', null, null); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'signed-out visitors cannot report');
end $$;
reset role;

do $$ begin
  raise notice '% checks, % failed', current_setting('prtest.n'), current_setting('prtest.fails');
  if current_setting('prtest.fails')::int > 0 then raise exception 'play_ready tests failed'; end if;
end $$;
rollback;
