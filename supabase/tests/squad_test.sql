-- ============================================================================================
-- SQL tests for supabase/migrations/20261110_squad.sql (🦁 Squad: weekly stars, class league, friends, cheers,
-- parent challenge). Run AFTER 20261108_parent_role.sql, 20261109_institutions.sql and 20261110_squad.sql, as a superuser:
--     psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/squad_test.sql
-- Everything is inside BEGIN … ROLLBACK. Each check prints PASS / FAIL as a NOTICE; the script ends with an ERROR if any
-- failed. Calls run as role "authenticated" with request.jwt.claims (like PostgREST).
-- ============================================================================================
begin;
select set_config('sqtest.fails', '0', true), set_config('sqtest.n', '0', true);
create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('sqtest.n', (current_setting('sqtest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('sqtest.fails', (current_setting('sqtest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
-- raw helpers that bypass RLS (test only)
create function pg_temp.code(u uuid) returns text language sql security definer as $$ select code from studyverse.squad_profile where user_id = u $$;
create function pg_temp.stars(u uuid, d date) returns int language sql security definer as $$ select stars from studyverse.squad_stars where user_id = u and day = d $$;
create function pg_temp.prof(u uuid) returns studyverse.squad_profile language sql security definer as $$ select * from studyverse.squad_profile where user_id = u $$;
create function pg_temp.befriend(x uuid, y uuid) returns void language sql security definer as $$
  insert into studyverse.squad_friends (a, b, requested_by, status, accepted_at) values (least(x, y), greatest(x, y), x, 'accepted', now()) $$;
create function pg_temp.fake_cheers(f uuid, t uuid, n int) returns void language sql security definer as $$
  insert into studyverse.squad_cheers (from_id, to_id, kind) select f, t, 'star' from generate_series(1, n) $$;
create function pg_temp.unlink(p uuid, c uuid) returns void language sql security definer as $$ delete from studyverse.parent_links where parent_id = p and child_id = c $$;
create function pg_temp.wk() returns date language sql as $$ select date_trunc('week', (now() at time zone 'Asia/Kolkata')::date)::date $$;
create function pg_temp.td() returns date language sql as $$ select (now() at time zone 'Asia/Kolkata')::date $$;
create function pg_temp.add_events(u uuid, k text, n int) returns void language sql security definer as $$
  insert into studyverse.squad_events (user_id, kind) select u, k from generate_series(1, n) $$;
create function pg_temp.qs(ks jsonb, ans int[]) returns jsonb language sql as $$
  select jsonb_agg(jsonb_build_object('k', k, 'q', 'Q' || n || '?', 'o', '["A","B","C","D"]'::jsonb, 'a', ans[n], 'x', 'Because ' || n) order by n)
  from jsonb_array_elements_text(ks) with ordinality t(k, n) $$;
create function pg_temp.rewind(c uuid, side text, secs int) returns void language sql security definer as $$
  update studyverse.parent_challenges set parent_started = case when side = 'parent' then parent_started - make_interval(secs => secs) else parent_started end,
    child_started = case when side = 'child' then child_started - make_interval(secs => secs) else child_started end where id = c $$;
grant execute on all functions in schema pg_temp to authenticated, anon;

-- ---------- fixtures ----------
-- school: Green Valley — 7-A (s1 Riya, s2 Kabir, s3 Meera), 7-B (s4 Aarav), 7-C (empty), 8-A (s5, other course)
-- other school: Hill View 7-A (s6). Retail students r1–r4, parents p1 (linked to r1) and p2 (linked to nobody).
insert into auth.users (id, email) values
  ('00000000-0000-0000-0000-0000000000a1', 's1@sq.test'), ('00000000-0000-0000-0000-0000000000a2', 's2@sq.test'),
  ('00000000-0000-0000-0000-0000000000a3', 's3@sq.test'), ('00000000-0000-0000-0000-0000000000a4', 's4@sq.test'),
  ('00000000-0000-0000-0000-0000000000a5', 's5@sq.test'), ('00000000-0000-0000-0000-0000000000a6', 's6@sq.test'),
  ('00000000-0000-0000-0000-0000000000b1', 'r1@sq.test'), ('00000000-0000-0000-0000-0000000000b2', 'r2@sq.test'),
  ('00000000-0000-0000-0000-0000000000b3', 'r3@sq.test'), ('00000000-0000-0000-0000-0000000000b4', 'r4@sq.test'),
  ('00000000-0000-0000-0000-0000000000c1', 'p1@sq.test'), ('00000000-0000-0000-0000-0000000000c2', 'p2@sq.test');
insert into studyverse.profiles (user_id, role) values ('00000000-0000-0000-0000-0000000000c1', 'parent'), ('00000000-0000-0000-0000-0000000000c2', 'parent');
insert into studyverse.parent_links (parent_id, child_id, child_name) values ('00000000-0000-0000-0000-0000000000c1', '00000000-0000-0000-0000-0000000000b1', 'Ishaan');
insert into studyverse.institutions (id, name) values ('10000000-0000-0000-0000-000000000001', 'Green Valley School'), ('10000000-0000-0000-0000-000000000002', 'Hill View School');
insert into studyverse.inst_classes (id, institution_id, grade, section, course, name) values
  ('20000000-0000-0000-0000-00000000007a', '10000000-0000-0000-0000-000000000001', 7, 'A', 'school-g7', 'Class 7-A'),
  ('20000000-0000-0000-0000-00000000007b', '10000000-0000-0000-0000-000000000001', 7, 'B', 'school-g7', 'Class 7-B'),
  ('20000000-0000-0000-0000-00000000007c', '10000000-0000-0000-0000-000000000001', 7, 'C', 'school-g7', 'Class 7-C'),
  ('20000000-0000-0000-0000-00000000008a', '10000000-0000-0000-0000-000000000001', 8, 'A', 'school-g8', 'Class 8-A'),
  ('20000000-0000-0000-0000-0000000000f7', '10000000-0000-0000-0000-000000000002', 7, 'A', 'school-g7', 'Class 7-A');
insert into studyverse.institution_members (institution_id, user_id, role, class_id, display_name) values
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-0000000000a1', 'student', '20000000-0000-0000-0000-00000000007a', 'Riya Sharma'),
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-0000000000a2', 'student', '20000000-0000-0000-0000-00000000007a', 'Kabir'),
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-0000000000a3', 'student', '20000000-0000-0000-0000-00000000007a', 'Meera'),
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-0000000000a4', 'student', '20000000-0000-0000-0000-00000000007b', 'Aarav'),
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-0000000000a5', 'student', '20000000-0000-0000-0000-00000000008a', 'Dev'),
  ('10000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-0000000000a6', 'student', '20000000-0000-0000-0000-0000000000f7', 'Zoya');

set local role authenticated;
do $$
declare S1 uuid := '00000000-0000-0000-0000-0000000000a1'; S2 uuid := '00000000-0000-0000-0000-0000000000a2'; S3 uuid := '00000000-0000-0000-0000-0000000000a3';
  S4 uuid := '00000000-0000-0000-0000-0000000000a4'; S5 uuid := '00000000-0000-0000-0000-0000000000a5'; S6 uuid := '00000000-0000-0000-0000-0000000000a6';
  R1 uuid := '00000000-0000-0000-0000-0000000000b1'; R2 uuid := '00000000-0000-0000-0000-0000000000b2'; R3 uuid := '00000000-0000-0000-0000-0000000000b3';
  R4 uuid := '00000000-0000-0000-0000-0000000000b4'; P1 uuid := '00000000-0000-0000-0000-0000000000c1'; P2 uuid := '00000000-0000-0000-0000-0000000000c2';
  wk date := pg_temp.wk(); td date := pg_temp.td(); lw date := pg_temp.wk() - 3;   -- lw: a day of last week
  r jsonb; h jsonb; cl jsonb; i int; cid uuid; k5 jsonb := '["g7-maths-01-01#0","g7-maths-01-02#1","g7-maths-02-01#2","g7-maths-03-01#0","g7-maths-04-02#3"]';
  denied boolean;
begin
  -- ================= 1. weekly stars sync =================
  perform pg_temp.as_user(S1);
  r := studyverse.squad_sync(jsonb_build_object(td::text, 5000, (td + 1)::text, 300, (wk - 20)::text, 400, '2026-02-30', 10, 'x', 5), 4, td::text, '  Riya   Sharma ', '🦊', '{"sdk4-easy": 95, "BAD KEY": 3, "kak-hard": 1}', 'school');
  perform pg_temp.chk((r ->> 'ok')::boolean and pg_temp.stars(S1, td) = 1500, 'stars per day are capped at 1500 (5000 sent)');
  perform pg_temp.chk(pg_temp.stars(S1, td + 1) is null and pg_temp.stars(S1, wk - 20) is null, 'future days and days older than last week are ignored');
  perform pg_temp.chk((r ->> 'week')::int = 1500, 'sync returns this week''s total');
  perform pg_temp.chk((pg_temp.prof(S1)).name = 'Riya' and (pg_temp.prof(S1)).avatar = '🦊', 'only the first name is stored');
  perform pg_temp.chk((pg_temp.prof(S1)).pz = '{"sdk4-easy": 95}'::jsonb, 'puzzle best times: bad keys and impossible times dropped');
  r := studyverse.squad_sync(jsonb_build_object(td::text, 20), 4, td::text, 'Ri<y>a', '<script>', null, 'school');
  perform pg_temp.chk(pg_temp.stars(S1, td) = 1500, 'a day''s stars never go down (another phone sent less)');
  perform pg_temp.chk((pg_temp.prof(S1)).name = 'Riya' and (pg_temp.prof(S1)).avatar = '🙂', 'markup is stripped from name and avatar');
  -- reset S1 to a normal number for the league: use a fresh day of last week instead
  perform pg_temp.as_user(P1);
  r := studyverse.squad_sync(jsonb_build_object(td::text, 50), 0, null, 'Mum', '👩', null, 'school');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'parent accounts cannot sync stars');
  r := studyverse.squad_home();
  perform pg_temp.chk((r ->> 'parent')::boolean, 'parent accounts get no squad');

  -- ================= 2. class vs class league =================
  -- 7-A: Riya 1500 this week, Kabir 0 this week but 60 last week (active), Meera never → avg 1500 / 2 = 750
  -- 7-B: Aarav 900 → avg 900. 7-C: nobody → 0. 8-A (other course) and Hill View are not shown.
  perform pg_temp.as_user(S2); perform studyverse.squad_sync(jsonb_build_object(lw::text, 60), 0, null, 'Kabir', '🐼', null, 'school');
  perform pg_temp.as_user(S4); perform studyverse.squad_sync(jsonb_build_object(td::text, 900), 2, td::text, 'Aarav', '🐯', null, 'school');
  perform pg_temp.as_user(S5); perform studyverse.squad_sync(jsonb_build_object(td::text, 1400), 0, null, 'Dev', '🐨', null, 'school');
  perform pg_temp.as_user(S6); perform studyverse.squad_sync(jsonb_build_object(td::text, 1400), 0, null, 'Zoya', '🐨', null, 'school');
  perform pg_temp.as_user(S1);
  h := studyverse.squad_home(); cl := h -> 'league' -> 'classes';
  perform pg_temp.chk(h -> 'league' ->> 'kind' = 'class' and h -> 'league' ->> 'inst' = 'Green Valley School', 'enrolled student gets the class league of their school');
  perform pg_temp.chk(jsonb_array_length(cl) = 3, 'league shows the 3 sections of Class 7 only (not 8-A, not another school)');
  perform pg_temp.chk(cl -> 0 ->> 'name' = 'Class 7-B' and cl -> 1 ->> 'name' = 'Class 7-A' and cl -> 2 ->> 'name' = 'Class 7-C', 'ranked by average stars per active student: 7-B 900 > 7-A 750 > 7-C 0');
  perform pg_temp.chk((cl -> 1 ->> 'avg')::numeric = 750 and (cl -> 1 ->> 'active')::int = 2 and (cl -> 1 ->> 'size')::int = 3, '7-A: 1500 stars / 2 active (Kabir active last week, Meera not) = 750');
  perform pg_temp.chk((cl -> 1 ->> 'me')::boolean and not (cl -> 0 ->> 'me')::boolean, 'my own class is marked');
  perform pg_temp.chk(position('Kabir' in cl::text) = 0 and position('Aarav' in cl::text) = 0 and position('@' in h::text) = 0, 'league shows no student names and no emails');
  perform pg_temp.as_user(S5);
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'league' -> 'classes') = 4, 'only section of its course: the league shows all classes of the school');
  perform pg_temp.as_user(R1);
  h := studyverse.squad_home();
  perform pg_temp.chk(h -> 'league' = 'null'::jsonb and length(h -> 'me' ->> 'code') = 6, 'retail student: no class league, gets a 6-letter friend code');

  -- ================= 3. friends (request → accept), privacy =================
  perform studyverse.squad_sync(jsonb_build_object(td::text, 120), 5, td::text, 'Ishaan', '🦁', '{"sdk4-easy": 140}', 'school');
  perform pg_temp.as_user(R2); perform studyverse.squad_sync(jsonb_build_object(td::text, 140), 5, (td - 1)::text, 'Riya', '🦊', '{"sdk4-easy": 95}', 'school');
  perform pg_temp.as_user(R3); perform studyverse.squad_sync(jsonb_build_object(td::text, 10), 1, (td - 5)::text, 'Meera', '🐨', null, 'school');
  perform pg_temp.as_user(R4); perform studyverse.squad_home();
  perform pg_temp.as_user(R1);
  r := studyverse.squad_add_friend(lower(pg_temp.code(R2)));
  perform pg_temp.chk(r ->> 'status' = 'pending', 'entering a friend code sends a request (lower case works)');
  perform pg_temp.chk(position('Riya' in r::text) = 0, 'the reply does not reveal who owns the code');
  r := studyverse.squad_add_friend(pg_temp.code(R2));
  perform pg_temp.chk(r ->> 'status' = 'pending', 'asking twice keeps one waiting request');
  r := studyverse.squad_add_friend(pg_temp.code(R1));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'own code is refused');
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 0 and (h ->> 'outgoing')::int = 1, 'before acceptance the sender sees nobody (only "1 waiting")');
  r := studyverse.squad_cheer(R2, 'clap');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'cannot cheer someone who has not accepted');
  perform pg_temp.as_user(R2);
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 0 and h -> 'incoming' -> 0 ->> 'name' = 'Ishaan', 'receiver sees the request (first name) but no friend yet');
  r := studyverse.squad_answer(R1, true);
  perform pg_temp.chk(r ->> 'status' = 'friends', 'request accepted');
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 1 and h -> 'friends' -> 0 ->> 'name' = 'Ishaan' and (h -> 'friends' -> 0 ->> 'week')::int = 120, 'friends leaderboard: name + weekly stars');
  perform pg_temp.chk((h -> 'friends' -> 0 ->> 'streak')::int = 5 and h -> 'friends' -> 0 -> 'pz' ->> 'sdk4-easy' = '140', 'friend''s streak and puzzle best are shared');
  perform pg_temp.chk(position('@' in h::text) = 0 and not (h -> 'friends' -> 0 ? 'email'), 'no email anywhere in the squad data');
  perform pg_temp.as_user(R3);
  r := studyverse.squad_add_friend(pg_temp.code(R1));
  perform pg_temp.as_user(R1);
  r := studyverse.squad_add_friend(pg_temp.code(R3));
  perform pg_temp.chk(r ->> 'status' = 'friends', 'typing the code of someone who already asked you makes you friends');
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 2 and h -> 'friends' -> 0 ->> 'name' = 'Riya', 'sender now sees both friends, most stars first');
  perform pg_temp.chk((h -> 'friends' -> 1 ->> 'streak')::int = 0, 'a streak not updated for 5 days shows as 0');
  perform pg_temp.as_user(R4);
  r := studyverse.squad_add_friend(pg_temp.code(R1)); r := studyverse.squad_cancel_requests();
  perform pg_temp.chk((r ->> 'removed')::int = 1, 'a waiting request can be taken back');
  perform pg_temp.as_user(P1);
  r := studyverse.squad_add_friend(pg_temp.code(R1));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'parent accounts cannot add friends');
  -- wrong codes: 20 a day, then even a right code is refused
  perform pg_temp.as_user(R4);
  for i in 1..20 loop r := studyverse.squad_add_friend('ZZZZZ' || i); end loop;
  perform pg_temp.chk(r ->> 'msg' like 'No friend found%', 'wrong code says so');
  r := studyverse.squad_add_friend(pg_temp.code(R2));
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'msg' like 'Too many%', 'after 20 wrong codes in a day, adding is paused');
  -- 10 requests a day (10 already logged today for Riya S1)
  reset role; perform pg_temp.add_events(S1, 'add', 10); set local role authenticated;
  perform pg_temp.as_user(S1);
  r := studyverse.squad_add_friend(pg_temp.code(S2));
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'msg' like 'You sent 10 requests%', 'at most 10 friend requests a day');
  r := studyverse.squad_new_code();
  perform pg_temp.chk((r ->> 'ok')::boolean and r ->> 'code' <> '' , 'a new friend code can be made');

  -- ================= 4. cheers =================
  perform pg_temp.as_user(R1);
  r := studyverse.squad_cheer(R2, 'clap');
  perform pg_temp.chk((r ->> 'ok')::boolean, 'cheer a friend with a preset cheer');
  r := studyverse.squad_cheer(R2, 'fire');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'msg' like 'You already cheered%', 'one cheer per friend per day');
  r := studyverse.squad_cheer(R3, 'You are dumb');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'free text is not a cheer');
  perform pg_temp.as_user(R2);
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'cheers') = 1 and h -> 'cheers' -> 0 ->> 'kind' = 'clap' and h -> 'cheers' -> 0 ->> 'name' = 'Ishaan', 'friend sees the cheer next time they open Squad');
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'cheers') = 0, 'a cheer is shown once');
  reset role; perform pg_temp.befriend(R1, R4); perform pg_temp.fake_cheers(R1, R3, 9); set local role authenticated;
  perform pg_temp.as_user(R1);
  r := studyverse.squad_cheer(R4, 'star');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'msg' like '%10 cheers%', 'at most 10 cheers a day');
  r := studyverse.squad_remove(R2);
  h := studyverse.squad_home();
  perform pg_temp.chk(not exists (select 1 from jsonb_array_elements(h -> 'friends') f where f ->> 'name' = 'Riya'), 'remove friend: gone from my list');
  perform pg_temp.as_user(R2);
  h := studyverse.squad_home(); r := studyverse.squad_cheer(R1, 'wave');
  perform pg_temp.chk(jsonb_array_length(h -> 'friends') = 0 and not (r ->> 'ok')::boolean, 'remove friend: gone for them too, and no more cheers');

  -- ================= 5. parent challenge (only linked parent ↔ child; scores computed by the server) =================
  -- answer key used below: 1, 0, 3, 2, 1
  perform pg_temp.as_user(P2);
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,3,2,1}'));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'a parent who is not linked cannot challenge the child');
  perform pg_temp.as_user(R2);
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,3,2,1}'));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'a student cannot create a parent challenge');
  perform pg_temp.as_user(P1);
  r := studyverse.pc_create(R1, 'g7/science', 'Science', pg_temp.qs(k5, '{1,0,3,2,1}'));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'question keys must belong to the chosen subject');
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs('["g7-maths-01-01#0","g7-maths-01-01#0","g7-maths-02-01#2","g7-maths-03-01#0","g7-maths-04-02#3"]', '{1,0,3,2,1}'));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'the same question twice is refused');
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', jsonb_build_array(pg_temp.qs(k5, '{1,0,3,2,1}') -> 0));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'exactly 5 questions');
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,7,2,1}'));
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'a correct option that does not exist is refused');
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,3,2,1}'));
  perform pg_temp.chk((r ->> 'ok')::boolean, 'linked parent starts a 5-question challenge');
  perform pg_temp.chk(position('"a"' in r::text) = 0 and not (r ? 'answers'), 'creating returns no answer key');
  cid := (r -> 'challenge' ->> 'id')::uuid;
  perform pg_temp.as_user(R1);
  h := studyverse.squad_home();
  perform pg_temp.chk(jsonb_array_length(h -> 'challenges') = 1 and not (h -> 'challenges' -> 0 ->> 'parent_done')::boolean and position('answers' in h::text) = 0, 'child sees the challenge (no answers)');
  r := studyverse.pc_submit(cid, '{1,0,3,2,1}');
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'msg' like 'Open the challenge%', 'cannot submit before opening (pc_start starts the clock)');
  r := studyverse.pc_start(cid);
  perform pg_temp.chk((r ->> 'ok')::boolean and jsonb_array_length(r -> 'questions') = 5 and r -> 'questions' -> 0 ->> 'q' = 'Q1?'
    and jsonb_array_length(r -> 'questions' -> 0 -> 'o') = 4, 'child opens it: 5 questions with their options');
  perform pg_temp.chk(not (r -> 'questions' -> 0 ? 'a') and not (r -> 'questions' -> 0 ? 'x') and not (r ? 'answers') and position('Because' in r::text) = 0,
    'the questions carry no correct option and no explanation');
  -- the parent plays: 3 right (q1, q2, q5), 70 s on the server clock
  perform pg_temp.as_user(P1);
  r := studyverse.pc_start(cid);
  reset role; perform pg_temp.rewind(cid, 'parent', 70); set local role authenticated;
  r := studyverse.pc_submit(cid, '{1,0,0,0,1}');
  perform pg_temp.chk((r ->> 'ok')::boolean and (r ->> 'score')::int = 3 and (r -> 'challenge' ->> 'parent_score')::int = 3, 'server scores the parent''s picks: 3/5');
  perform pg_temp.chk((r ->> 'ms')::int = 70000, 'time comes from the server clock (70 s), not from the phone');
  perform pg_temp.chk(r -> 'answers' = '[1,0,3,2,1]'::jsonb and r -> 'explains' ->> 0 = 'Because 1', 'after submitting, the parent gets the right answers + explanations');
  r := studyverse.pc_submit(cid, '{1,0,3,2,1}');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'parent cannot play twice');
  r := studyverse.pc_start(cid);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'parent cannot reopen after playing');
  perform pg_temp.as_user(R1);
  h := studyverse.squad_home();
  perform pg_temp.chk((h -> 'challenges' -> 0 ->> 'parent_done')::boolean and h -> 'challenges' -> 0 -> 'parent_score' = 'null'::jsonb, 'child knows the parent played but not the score before playing');
  r := studyverse.pc_submit(cid, '{1,0,3}');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'fewer than 5 picks is refused');
  r := studyverse.pc_submit(cid, '{1,0,9,2,1}');
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'an impossible option number is refused');
  begin r := studyverse.pc_submit(cid, 5, 1000); r := '{"ok":true}'; exception when undefined_function then r := '{"ok":false}'; end;
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'there is no way to send a score');
  reset role; perform pg_temp.rewind(cid, 'child', 50); set local role authenticated;
  r := studyverse.pc_submit(cid, '{1,0,3,2,-1}');
  perform pg_temp.chk((r ->> 'ok')::boolean and (r ->> 'score')::int = 4 and (r -> 'challenge' ->> 'parent_score')::int = 3 and (r -> 'challenge' ->> 'child_ms')::int = 50000,
    'child: 4 right + 1 skipped = 4/5 in 50 s, and now sees the parent''s 3/5');
  perform pg_temp.as_user(R2);
  r := studyverse.pc_start(cid);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'another student cannot open it');
  perform pg_temp.as_user(P2);
  r := studyverse.pc_list(R1);
  perform pg_temp.chk(not (r ->> 'ok')::boolean, 'an unlinked parent cannot list the child''s challenges');
  perform pg_temp.as_user(P1);
  r := studyverse.pc_list(R1);
  perform pg_temp.chk((r -> 'challenges' -> 0 ->> 'child_score')::int = 4 and (r -> 'challenges' -> 0 ->> 'child_ms')::int = 50000, 'parent sees the child''s result');
  r := studyverse.pc_create(R1, 'ca/foundation/fnd-p1', 'Accounting', pg_temp.qs('["fnd-p1-ch01-u01#m1","fnd-p1-ch01-u01#m2","fnd-p1-ch02-u01#m1","fnd-p1-ch02-u01#m3","fnd-p1-ch03-u02#m4"]', '{0,1,2,3,0}'));
  perform pg_temp.chk((r ->> 'ok')::boolean, 'CA challenge from a paper''s units');
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,3,2,1}')); r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,3,2,1}'));
  r := studyverse.pc_create(R1, 'g7/maths', 'Maths', pg_temp.qs(k5, '{1,0,3,2,1}'));
  perform pg_temp.chk(not (r ->> 'ok')::boolean and r ->> 'msg' like '3 challenges%', 'at most 3 challenges waiting for one child');
  begin perform 1 from studyverse.parent_challenge_answers limit 1; denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'the answer key table cannot be read by any app user');
  reset role; perform pg_temp.unlink(P1, R1); set local role authenticated;
  perform pg_temp.as_user(R1);
  h := studyverse.squad_home(); r := studyverse.pc_start(cid);
  perform pg_temp.chk(jsonb_array_length(h -> 'challenges') = 0 and not (r ->> 'ok')::boolean, 'after unlinking, the child no longer sees or opens the parent''s challenges');

  -- ================= 6. direct table access is closed =================
  begin perform 1 from studyverse.squad_stars limit 1; denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'students cannot read the stars table directly');
  begin perform 1 from studyverse.squad_friends limit 1; denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'students cannot read the friends table directly');
  begin insert into studyverse.squad_cheers (from_id, to_id, kind) values (R1, R2, 'star'); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'students cannot write cheers directly');
end $$;

reset role;
set local role anon;
do $$ declare denied boolean; begin
  begin perform studyverse.squad_home(); denied := false; exception when insufficient_privilege then denied := true; end;
  perform pg_temp.chk(denied, 'signed-out visitors cannot call squad_home');
end $$;
reset role;

do $$ begin
  raise notice '% checks, % failed', current_setting('sqtest.n'), current_setting('sqtest.fails');
  if current_setting('sqtest.fails')::int > 0 then raise exception 'squad tests failed'; end if;
end $$;
rollback;
