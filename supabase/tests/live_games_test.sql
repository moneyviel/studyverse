-- ============================================================================================
-- SQL tests for supabase/migrations/20261109_live_games.sql (Game Rooms RPCs).
-- Run AFTER the migration, as a superuser (e.g. the SQL editor, or psql as postgres):
--     psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/live_games_test.sql
-- Everything happens inside BEGIN … ROLLBACK: test users, rooms and results are thrown away.
-- Each check prints "PASS …" / "FAIL …" as a NOTICE; the script ends with an ERROR if any check failed.
-- Calls are made as the "authenticated" role with request.jwt.claims set, exactly like PostgREST does.
-- Time is simulated by moving a room's deadlines back (now() is fixed inside one transaction).
-- ============================================================================================
begin;
select set_config('lvtest.fails', '0', true), set_config('lvtest.n', '0', true);

create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('lvtest.n', (current_setting('lvtest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('lvtest.fails', (current_setting('lvtest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
-- act as a user (like PostgREST: role authenticated + JWT claims)
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
-- "time passes": move every clock of a room back by s seconds
create function pg_temp.rewind(c text, s int) returns void language plpgsql security definer as $$
begin
  update studyverse.game_rooms set deadline = deadline - make_interval(secs => s),
    state = state || case when state ? 'round_at' then jsonb_build_object('round_at', (state ->> 'round_at')::timestamptz - make_interval(secs => s)) else '{}'::jsonb end
                  || case when state ? 'done_at' then jsonb_build_object('done_at', (state ->> 'done_at')::timestamptz - make_interval(secs => s)) else '{}'::jsonb end
  where code = c;
end $$;
create function pg_temp.room(c text) returns studyverse.game_rooms language sql security definer as $$ select * from studyverse.game_rooms where code = c $$;
create function pg_temp.pl(c text, u uuid) returns studyverse.room_players language sql security definer as $$ select * from studyverse.room_players where code = c and user_id = u $$;
create function pg_temp.nres(c text, w boolean) returns int language sql security definer as $$ select count(*)::int from studyverse.game_results where code = c and (w is null or won = w) $$;
create function pg_temp.key(c text, crs text, i int) returns int language sql security definer as $$ select (keys -> crs -> i ->> 'a')::int from studyverse.room_keys where code = c $$;
create function pg_temp.qs(n int, crs text) returns jsonb language sql as $$
  select jsonb_agg(jsonb_build_object('q', crs || ' question ' || i, 'o', jsonb_build_array('A' || i, 'B' || i, 'C' || i), 'a', i % 3, 's', 'Test', 'x', 'Because ' || i)) from generate_series(0, n - 1) i $$;
grant execute on all functions in schema pg_temp to authenticated;

-- ---------- fixtures ----------
insert into auth.users (id, email) values
  ('00000000-0000-0000-0000-0000000000a1', 'host@t.test'), ('00000000-0000-0000-0000-0000000000a2', 'asha@t.test'),
  ('00000000-0000-0000-0000-0000000000a3', 'ca@t.test'),   ('00000000-0000-0000-0000-0000000000a4', 'free@t.test'),
  ('00000000-0000-0000-0000-0000000000a5', 'parent@t.test'), ('00000000-0000-0000-0000-0000000000a6', 'owner@t.test'),
  ('00000000-0000-0000-0000-0000000000a7', 'expired@t.test');
insert into studyverse.course_access (user_id, course, valid_until, note) values
  ('00000000-0000-0000-0000-0000000000a1', 'school-g6', now() + interval '30 days', 'paid s68-month'),
  ('00000000-0000-0000-0000-0000000000a2', 'school-all', now() + interval '20 hours', 'trial'),
  ('00000000-0000-0000-0000-0000000000a3', 'ca-foundation', now() + interval '60 days', 'paid ca-month'),
  ('00000000-0000-0000-0000-0000000000a7', 'school-all', now() - interval '1 hour', 'trial');
insert into studyverse.profiles (user_id, role) values ('00000000-0000-0000-0000-0000000000a5', 'parent') on conflict (user_id) do update set role = 'parent';
insert into studyverse.course_access (user_id, course, valid_until, note) values ('00000000-0000-0000-0000-0000000000a5', 'school-all', now() + interval '1 day', 'trial');
insert into studyverse.admins (user_id) values ('00000000-0000-0000-0000-0000000000a6') on conflict do nothing;

set local role authenticated;
do $$
declare H uuid := '00000000-0000-0000-0000-0000000000a1'; A uuid := '00000000-0000-0000-0000-0000000000a2'; B uuid := '00000000-0000-0000-0000-0000000000a3';
  F uuid := '00000000-0000-0000-0000-0000000000a4'; PAR uuid := '00000000-0000-0000-0000-0000000000a5'; O uuid := '00000000-0000-0000-0000-0000000000a6';
  X uuid := '00000000-0000-0000-0000-0000000000a7';
  j jsonb; c text; c2 text; r studyverse.game_rooms; pp studyverse.room_players; st int; k int; n int; qs jsonb; i int; u uuid;
begin
  -- ===== eligibility =====
  perform pg_temp.as_user(H); j := studyverse.live_eligibility(); perform pg_temp.chk((j ->> 'ok')::boolean, 'paid student is eligible');
  perform pg_temp.as_user(A); j := studyverse.live_eligibility(); perform pg_temp.chk((j ->> 'ok')::boolean, 'trial student is eligible');
  perform pg_temp.as_user(F); j := studyverse.live_eligibility(); perform pg_temp.chk(j ->> 'reason' = 'free', 'free plan is blocked');
  perform pg_temp.as_user(X); j := studyverse.live_eligibility(); perform pg_temp.chk(j ->> 'reason' = 'free', 'ended trial counts as free plan');
  perform pg_temp.as_user(PAR); j := studyverse.live_eligibility(); perform pg_temp.chk(j ->> 'reason' = 'parent', 'parent is blocked (even with access rows)');
  perform pg_temp.as_user(O); j := studyverse.live_eligibility(); perform pg_temp.chk((j ->> 'ok')::boolean and (j ->> 'admin')::boolean, 'owner/admin allowed');
  perform pg_temp.as_user(F); j := studyverse.create_room('quiz', 'ffa', 5, 10, 'Free Kid', '🐼', 'school-g6');
  perform pg_temp.chk(not (j ->> 'ok')::boolean and j ->> 'code' = 'free', 'free plan cannot create a room');

  -- ===== create / join / lobby =====
  perform pg_temp.as_user(H); j := studyverse.create_room('quiz', 'ffa', 3, 10, '  Riya   Sharma ', '🦊', 'school-g6');
  c := j ->> 'code'; perform pg_temp.chk((j ->> 'ok')::boolean and c ~ '^[A-Z]{6}$', 'create_room gives a 6-letter code: ' || coalesce(c, '?'));
  pp := pg_temp.pl(c, H); perform pg_temp.chk(pp.name = 'Riya' and pp.ready and pp.seat = 1, 'host stored with first name only, ready, seat 1');
  perform pg_temp.as_user(F); j := studyverse.join_room(c, 'Free', '🐼', 'school-g6'); perform pg_temp.chk(j ->> 'code' = 'free', 'free plan cannot join');
  perform pg_temp.as_user(PAR); j := studyverse.join_room(c, 'Mum', '👩', 'school-g6'); perform pg_temp.chk(j ->> 'code' = 'parent', 'parent cannot join');
  perform pg_temp.as_user(A); j := studyverse.join_room(lower(c), 'Asha', '🐯', 'school-g3'); perform pg_temp.chk((j ->> 'ok')::boolean, 'trial student joins (code is case-insensitive)');
  perform pg_temp.as_user(B); j := studyverse.join_room(c, 'Kabir', '🎓', 'ca-foundation'); perform pg_temp.chk((j ->> 'ok')::boolean, 'CA student joins');
  j := studyverse.join_room('ZZZZZZ', 'Kabir', '🎓', 'ca-foundation'); perform pg_temp.chk(j ->> 'code' = 'not_found', 'unknown code rejected');
  j := studyverse.join_room(c, 'Kabir', '🎓', 'Bad Course!'); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bad course key rejected');
  -- members read via RLS; others do not
  select count(*) into n from studyverse.room_players where code = c; perform pg_temp.chk(n = 3, 'member reads all 3 players through RLS');
  perform pg_temp.as_user(F); select count(*) into n from studyverse.room_players where code = c; perform pg_temp.chk(n = 0, 'non-member reads nothing (RLS)');
  select count(*) into n from studyverse.game_rooms where code = c; perform pg_temp.chk(n = 0, 'non-member cannot see the room');
  begin perform 1 from studyverse.room_keys limit 1; perform pg_temp.chk(false, 'room_keys must not be readable');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'room_keys not readable by clients'); end;
  begin update studyverse.room_players set score = 999 where code = c; perform pg_temp.chk(false, 'direct update must fail');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'clients cannot write room_players directly'); end;

  perform pg_temp.as_user(A); j := studyverse.room_state(c, false);
  perform pg_temp.chk((j ->> 'ok')::boolean and jsonb_array_length(j -> 'players') = 3 and j -> 'room' ->> 'status' = 'lobby', 'room_state shows the lobby');
  perform pg_temp.as_user(H); j := studyverse.start_game(c, jsonb_build_object('school-g6', pg_temp.qs(5, 'g6'), 'school-g3', pg_temp.qs(5, 'g3'), 'ca-foundation', pg_temp.qs(5, 'ca')));
  perform pg_temp.chk(j ->> 'code' = 'not_ready', 'cannot start before everyone is ready: ' || (j ->> 'msg'));
  perform pg_temp.as_user(A); perform studyverse.set_ready(c, true);
  perform pg_temp.as_user(B); perform studyverse.set_ready(c, true);
  perform pg_temp.as_user(A); j := studyverse.start_game(c, '{}'::jsonb); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'only the host can start');
  perform pg_temp.as_user(H); j := studyverse.start_game(c, jsonb_build_object('school-g6', pg_temp.qs(5, 'g6'), 'school-g3', pg_temp.qs(2, 'g3')));
  perform pg_temp.chk(j ->> 'code' = 'need_questions' and j -> 'need' ? 'school-g3' and j -> 'need' ? 'ca-foundation', 'start refuses when a course has too few questions');
  -- host changes settings
  j := studyverse.update_room(c, 'quiz', 'duel', 3, 10); perform pg_temp.chk(not (j ->> 'ok')::boolean, '1-v-1 refused with 3 players');
  j := studyverse.update_room(c, 'quiz', 'ffa', 3, 15); perform pg_temp.chk((pg_temp.room(c)).turn_secs = 20, 'odd turn time falls back to 20 s');
  j := studyverse.update_room(c, 'quiz', 'ffa', 3, 10);
  perform pg_temp.as_user(A); j := studyverse.update_room(c, 'snakes', 'ffa', 3, 10); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'non-host cannot change settings');

  -- ===== Quiz Race =====
  perform pg_temp.as_user(H);
  j := studyverse.start_game(c, jsonb_build_object('school-g6', pg_temp.qs(5, 'g6'), 'school-g3', pg_temp.qs(5, 'g3'), 'ca-foundation', pg_temp.qs(5, 'ca')));
  perform pg_temp.chk((j ->> 'ok')::boolean, 'quiz race starts');
  r := pg_temp.room(c); st := r.step;
  perform pg_temp.chk(r.status = 'playing' and not (r.questions -> 'school-g6' -> 0) ? 'a', 'public questions carry no answer key');
  perform pg_temp.as_user(A); j := studyverse.room_state(c, true);
  perform pg_temp.chk(j -> 'questions' -> 0 ->> 'q' = 'g3 question 0' and j -> 'me' -> 'reveal' = 'null'::jsonb, 'each player gets their own course questions; no reveal yet');
  j := studyverse.submit_answer(c, st, 0); perform pg_temp.chk(j ->> 'code' = 'early', 'answers before the 3-2-1 countdown are refused');
  perform pg_temp.rewind(c, 4);    -- countdown over, 1 s into the question
  perform pg_temp.as_user(H); j := studyverse.submit_answer(c, st, pg_temp.key(c, 'school-g6', 0));
  perform pg_temp.chk((j ->> 'correct')::boolean and (j ->> 'points')::int between 50 and 100, 'right answer scores 50–100 points (speed bonus): ' || (j ->> 'points'));
  j := studyverse.submit_answer(c, st, 0); perform pg_temp.chk(j ->> 'code' = 'answered', 'cannot answer twice');
  perform pg_temp.as_user(A); j := studyverse.submit_answer(c, st, (pg_temp.key(c, 'school-g3', 0) + 1) % 3);
  perform pg_temp.chk(not (j ->> 'correct')::boolean and (j ->> 'answer')::int = pg_temp.key(c, 'school-g3', 0), 'wrong answer: 0 points, key revealed after answering');
  perform pg_temp.chk((pg_temp.pl(c, A)).score = 0 and (pg_temp.pl(c, H)).score > 0, 'scores recorded server-side');
  j := studyverse.advance(c, st); perform pg_temp.chk(not (j ->> 'changed')::boolean, 'advance does nothing while the round is open');
  perform pg_temp.as_user(B); j := studyverse.submit_answer(c, st, pg_temp.key(c, 'ca-foundation', 0));
  perform pg_temp.chk(((pg_temp.room(c)).state ->> 'done')::boolean, 'round marked done when everyone answered');
  j := studyverse.advance(c, st); perform pg_temp.chk(not (j ->> 'changed')::boolean, 'reveal pause (2 s) before the next question');
  perform pg_temp.rewind(c, 3); j := studyverse.advance(c, st);
  r := pg_temp.room(c); perform pg_temp.chk((j ->> 'changed')::boolean and r.qi = 1 and r.step = st + 1, 'advance moves to question 2');
  j := studyverse.advance(c, st); perform pg_temp.chk(not (j ->> 'changed')::boolean, 'stale advance (old step) is ignored');
  st := r.step;
  -- round 2: only the host answers; deadline expiry moves on (others get 0)
  perform pg_temp.rewind(c, 1); perform pg_temp.as_user(H); perform studyverse.submit_answer(c, st, pg_temp.key(c, 'school-g6', 1));
  perform pg_temp.as_user(A); j := studyverse.advance(c, st); perform pg_temp.chk(not (j ->> 'changed')::boolean, 'cannot skip others before the deadline');
  perform pg_temp.rewind(c, 12); j := studyverse.submit_answer(c, st, 0); perform pg_temp.chk(j ->> 'code' = 'late', 'answer after the deadline refused');
  j := studyverse.room_state(c, false); perform pg_temp.chk((j -> 'me' -> 'reveal' ->> 'answer')::int = pg_temp.key(c, 'school-g3', 1), 'answer revealed after the deadline');
  j := studyverse.advance(c, st); perform pg_temp.chk((j ->> 'changed')::boolean and (pg_temp.room(c)).qi = 2, 'deadline passed: any member can advance');
  st := (pg_temp.room(c)).step; perform pg_temp.rewind(c, 13);
  perform pg_temp.as_user(B); j := studyverse.advance(c, st);
  r := pg_temp.room(c); perform pg_temp.chk(r.status = 'finished', 'quiz finishes after the last round');
  perform pg_temp.chk(pg_temp.nres(c, null) = 3, 'results saved for all players');
  perform pg_temp.as_user(H); select count(*) into n from studyverse.game_results where code = c and won; perform pg_temp.chk(n = 1, 'host (most points) is the winner (own row visible)');

  -- weekly leaderboard
  j := studyverse.weekly_board(); perform pg_temp.chk(jsonb_array_length(j) = 3 and (j -> 0 ->> 'me')::boolean and (j -> 0 ->> 'wins')::int = 1, 'weekly friends board lists the 3 players, winner first');
  perform pg_temp.as_user(F); j := studyverse.weekly_board(); perform pg_temp.chk(jsonb_array_length(j) = 0, 'outsider sees an empty board');

  -- rematch → lobby, then Buzzer
  perform pg_temp.as_user(A); j := studyverse.rematch(c); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'only the host can rematch');
  perform pg_temp.as_user(H); j := studyverse.rematch(c); r := pg_temp.room(c);
  perform pg_temp.chk(r.status = 'lobby' and not (pg_temp.pl(c, A)).ready and (pg_temp.pl(c, H)).score = 0, 'rematch: back to lobby, scores reset, ready cleared');
  perform studyverse.update_room(c, 'buzzer', 'ffa', 3, 10);
  perform pg_temp.as_user(A); perform studyverse.set_ready(c, true); perform pg_temp.as_user(B); perform studyverse.set_ready(c, true);
  perform pg_temp.as_user(H); j := studyverse.start_game(c, jsonb_build_object('school-g6', pg_temp.qs(5, 'g6'), 'school-g3', pg_temp.qs(5, 'g3'), 'ca-foundation', pg_temp.qs(5, 'ca')));
  perform pg_temp.chk((j ->> 'ok')::boolean, 'buzzer starts');
  perform pg_temp.rewind(c, 4); st := (pg_temp.room(c)).step;
  perform pg_temp.as_user(A); j := studyverse.submit_answer(c, st, 0); perform pg_temp.chk(j ->> 'code' = 'not_your_turn', 'cannot answer without buzzing');
  j := studyverse.buzz(c, st); perform pg_temp.chk((j ->> 'ok')::boolean, 'Asha buzzes first');
  perform pg_temp.as_user(B); j := studyverse.buzz(c, st); perform pg_temp.chk(j ->> 'code' = 'taken', 'second buzz is refused');
  st := (pg_temp.room(c)).step;
  perform pg_temp.as_user(A); j := studyverse.submit_answer(c, st, (pg_temp.key(c, 'school-g3', 0) + 1) % 3);
  r := pg_temp.room(c); perform pg_temp.chk(not (j ->> 'correct')::boolean and r.turn_user is null and r.state -> 'out' ? A::text, 'wrong buzz answer locks Asha out and re-opens the buzzer');
  st := r.step; j := studyverse.buzz(c, st); perform pg_temp.chk(j ->> 'code' = 'out', 'locked-out player cannot buzz again');
  perform pg_temp.as_user(B); j := studyverse.buzz(c, st); st := (pg_temp.room(c)).step;
  perform pg_temp.rewind(c, 12); perform pg_temp.as_user(H); j := studyverse.advance(c, st);
  r := pg_temp.room(c); perform pg_temp.chk(r.turn_user is null and r.state -> 'out' ? B::text and r.qi = 0, 'buzzer who runs out of time is locked out too');
  st := r.step; perform pg_temp.as_user(H); perform studyverse.buzz(c, st); st := (pg_temp.room(c)).step;
  j := studyverse.submit_answer(c, st, pg_temp.key(c, 'school-g6', 0));
  perform pg_temp.chk((j ->> 'correct')::boolean and (pg_temp.pl(c, H)).score = 100 and ((pg_temp.room(c)).state ->> 'done')::boolean, 'right buzz answer: +100 and the round ends');
  st := (pg_temp.room(c)).step; perform pg_temp.rewind(c, 3); j := studyverse.advance(c, st);
  perform pg_temp.chk((pg_temp.room(c)).qi = 1, 'next buzzer question');
  st := (pg_temp.room(c)).step; perform pg_temp.rewind(c, 13); j := studyverse.advance(c, st);
  perform pg_temp.chk((pg_temp.room(c)).qi = 2, 'nobody buzzed: moves on after the deadline');
  perform pg_temp.as_user(H); j := studyverse.finish_game(c); perform pg_temp.chk((pg_temp.room(c)).status = 'finished', 'host can end the game early');

  -- ===== Teams + Relay =====
  perform pg_temp.as_user(O); j := studyverse.create_room('relay', 'ffa', 4, 10, 'Owner', '🔑', 'school-g6'); c2 := j ->> 'code';
  perform pg_temp.chk((pg_temp.room(c2)).mode = 'teams', 'relay forces teams mode (owner can create without a plan)');
  perform pg_temp.as_user(A); perform studyverse.join_room(c2, 'Asha', '🐯', 'school-g3');
  perform pg_temp.as_user(H); perform studyverse.join_room(c2, 'Riya', '🦊', 'school-g6');
  perform pg_temp.as_user(B); perform studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation');
  select count(*) filter (where team = 0), count(*) filter (where team = 1) into k, n from studyverse.room_players where code = c2;
  perform pg_temp.chk(k = 2 and n = 2, 'teams auto-balanced 2 v 2');
  perform pg_temp.as_user(A); j := studyverse.set_team(c2, 0); j := studyverse.set_team(c2, 1);
  perform pg_temp.chk((pg_temp.pl(c2, A)).team = 1, 'player can switch team in the lobby');
  perform studyverse.set_ready(c2, true); perform pg_temp.as_user(H); perform studyverse.set_ready(c2, true); perform pg_temp.as_user(B); perform studyverse.set_ready(c2, true);
  perform pg_temp.as_user(O); j := studyverse.start_game(c2, jsonb_build_object('school-g6', pg_temp.qs(6, 'g6'), 'school-g3', pg_temp.qs(6, 'g3'), 'ca-foundation', pg_temp.qs(6, 'ca')));
  r := pg_temp.room(c2); perform pg_temp.chk((j ->> 'ok')::boolean and jsonb_array_length(r.state -> 'runners') = 2, 'relay starts with one runner per team');
  perform pg_temp.rewind(c2, 4); st := r.step;
  -- the non-runner of a team is refused
  select user_id into u from studyverse.room_players p where p.code = c2 and not ((r.state -> 'runners') ? p.user_id::text) limit 1;
  perform pg_temp.as_user(u); j := studyverse.submit_answer(c2, st, 0); perform pg_temp.chk(j ->> 'code' = 'not_your_turn', 'teammate who is not running is refused (wrong turn)');
  for i in 0..1 loop
    u := (r.state -> 'runners' ->> i)::uuid; perform pg_temp.as_user(u);
    j := studyverse.submit_answer(c2, st, (pg_temp.key(c2, (pg_temp.pl(c2, u)).course, 0) + i) % 3);   -- runner 1 answers wrong
  end loop;
  perform pg_temp.chk(((pg_temp.room(c2)).state ->> 'done')::boolean, 'relay round done when both runners answered');
  qs := r.state -> 'runners';
  perform pg_temp.rewind(c2, 3); perform studyverse.advance(c2, st); r := pg_temp.room(c2);
  perform pg_temp.chk(r.qi = 1 and jsonb_array_length(r.state -> 'runners') = 2 and r.state -> 'runners' <> qs, 'runners rotate next round');
  perform pg_temp.as_user(O); perform studyverse.finish_game(c2); r := pg_temp.room(c2);
  n := pg_temp.nres(c2, true);
  perform pg_temp.chk(r.status = 'finished' and jsonb_array_length(r.state -> 'teams') = 2 and n = 2, 'team game: both players of the winning team win');

  -- ===== Snakes & Ladders Battle =====
  perform pg_temp.as_user(H); j := studyverse.create_room('snakes', 'ffa', 10, 10, 'Riya', '🦊', 'school-g6'); c2 := j ->> 'code';
  perform pg_temp.as_user(A); perform studyverse.join_room(c2, 'Asha', '🐯', 'school-g3'); perform studyverse.set_ready(c2, true);
  perform pg_temp.as_user(H); j := studyverse.start_game(c2, jsonb_build_object('school-g6', pg_temp.qs(6, 'g6'), 'school-g3', pg_temp.qs(6, 'g3')));
  r := pg_temp.room(c2); st := r.step;
  perform pg_temp.chk((j ->> 'ok')::boolean and r.turn_user = H, 'snakes starts with the host''s turn');
  perform pg_temp.as_user(A); j := studyverse.submit_move(c2, st); perform pg_temp.chk(j ->> 'code' = 'not_your_turn', 'wrong-turn roll rejected');
  perform pg_temp.as_user(H); perform set_config('studyverse.test_roll', '1', true);
  j := studyverse.submit_move(c2, st); r := pg_temp.room(c2);
  perform pg_temp.chk((j ->> 'to')::int = 2 and j -> 'gate' ->> 'kind' = 'lad' and r.state -> 'gate' is not null and r.turn_user = H, 'roll 1 → square 2: ladder gate opens');
  j := studyverse.submit_move(c2, r.step); perform pg_temp.chk(j ->> 'code' = 'gate', 'cannot roll again before answering');
  j := studyverse.submit_answer(c2, r.step, pg_temp.key(c2, 'school-g6', 0));
  perform pg_temp.chk((j ->> 'correct')::boolean and (pg_temp.pl(c2, H)).pos = 23, 'right answer climbs the ladder 2 → 23');
  r := pg_temp.room(c2); perform pg_temp.chk(r.turn_user = A, 'turn passes to Asha');
  -- Asha misses her turn (timer) → skipped
  perform pg_temp.as_user(H); j := studyverse.advance(c2, r.step); perform pg_temp.chk(not (j ->> 'changed')::boolean, 'cannot skip a player before the turn timer ends');
  perform pg_temp.rewind(c2, 20); j := studyverse.advance(c2, r.step); r := pg_temp.room(c2);
  perform pg_temp.chk((j ->> 'changed')::boolean and r.turn_user = H and (r.state -> 'last' ->> 'skip')::boolean, 'missed turn is skipped after the timer');
  -- host: snake gate, wrong answer → slides
  begin update studyverse.room_players set pos = 99 where code = c2 and user_id = H; exception when insufficient_privilege then null; end;
  perform pg_temp.chk((pg_temp.pl(c2, H)).pos = 23, 'direct position change has no effect');
  perform set_config('studyverse.test_roll', '5', true); perform pg_temp.as_user(H);
  j := studyverse.submit_move(c2, r.step); r := pg_temp.room(c2);        -- 23 + 5 = 28: ladder to 76
  j := studyverse.submit_answer(c2, r.step, (pg_temp.key(c2, 'school-g6', 1) + 1) % 3);
  perform pg_temp.chk(not (j ->> 'correct')::boolean and (pg_temp.pl(c2, H)).pos = 28, 'wrong answer on a ladder: stay on 28');
  -- Asha: offline (last seen long ago) → her turn is skipped at once
  r := pg_temp.room(c2); perform pg_temp.chk(r.turn_user = A, 'Asha''s turn');
  reset role; update studyverse.room_players set last_seen = now() - interval '2 minutes' where code = c2 and user_id = A; set local role authenticated;
  perform pg_temp.as_user(H); j := studyverse.advance(c2, r.step); r := pg_temp.room(c2);
  perform pg_temp.chk((j ->> 'changed')::boolean and r.turn_user = H, 'offline player''s turn auto-skips');
  -- host becomes host-handover candidate check: Asha comes back (room_state) and sees she is not host
  perform pg_temp.as_user(A); j := studyverse.room_state(c2, false); perform pg_temp.chk((j -> 'room' ->> 'host_id')::uuid = H, 'online host keeps the host role');
  -- exact 100 rule
  reset role; update studyverse.room_players set pos = 97, score = 97 where code = c2 and user_id = H; set local role authenticated;
  perform pg_temp.as_user(H); perform set_config('studyverse.test_roll', '5', true);
  j := studyverse.submit_move(c2, r.step); perform pg_temp.chk((j ->> 'over')::boolean and (pg_temp.pl(c2, H)).pos = 97, 'roll past 100 = stay on 97 (exact roll needed)');
  r := pg_temp.room(c2); perform pg_temp.as_user(A); perform set_config('studyverse.test_roll', '2', true);
  j := studyverse.submit_move(c2, r.step); r := pg_temp.room(c2);                -- Asha 1 → 3 (plain square)
  perform pg_temp.as_user(H); perform set_config('studyverse.test_roll', '3', true);
  j := studyverse.submit_move(c2, r.step); r := pg_temp.room(c2);
  perform pg_temp.chk((pg_temp.pl(c2, H)).pos = 100 and r.status = 'finished', 'exact roll lands on 100 and wins');
  perform pg_temp.chk(pg_temp.nres(c2, true) = 1, 'snakes winner recorded');
  perform pg_temp.chk(r.rounds >= 3 and (r.state ->> 'round')::int <= r.rounds + 100, 'snakes ran without a round limit');
  perform pg_temp.as_user(H); j := studyverse.create_room('quiz', 'ffa', 5, 10, 'Riya', '🦊', 'school-g6', 'hard');
  perform pg_temp.chk((j ->> 'ok')::boolean and (select level from studyverse.game_rooms where code = j ->> 'code') = 'hard', 'room question level stored (hard)');
  j := studyverse.update_room(j ->> 'code', null, null, null, null, 'easy');
  perform pg_temp.chk((j ->> 'ok')::boolean, 'host can change the level');

  -- ===== disconnect / rejoin / host handover / kick =====
  perform pg_temp.as_user(H); j := studyverse.create_room('quiz', 'ffa', 3, 10, 'Riya', '🦊', 'school-g6'); c2 := j ->> 'code';
  perform pg_temp.as_user(A); perform studyverse.join_room(c2, 'Asha', '🐯', 'school-g3');
  perform pg_temp.as_user(B); perform studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation');
  perform pg_temp.as_user(H); j := studyverse.kick_player(c2, B); perform pg_temp.chk((j ->> 'ok')::boolean and (pg_temp.pl(c2, B)).user_id is null, 'host removes a player');
  perform pg_temp.as_user(B); j := studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation'); perform pg_temp.chk(j ->> 'code' = 'banned', 'removed player cannot rejoin');
  perform pg_temp.as_user(A); j := studyverse.kick_player(c2, H); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'only the host can remove players');
  -- host goes silent for 2 minutes → next player becomes host on their next poll
  reset role; update studyverse.room_players set last_seen = now() - interval '2 minutes' where code = c2 and user_id = H; set local role authenticated;
  perform pg_temp.as_user(A); j := studyverse.room_state(c2, false); perform pg_temp.chk((j -> 'room' ->> 'host_id')::uuid = A, 'host gone → next player becomes host');
  perform pg_temp.chk(not (j -> 'players' -> 0 ->> 'online')::boolean, 'silent player is shown offline');
  perform pg_temp.as_user(H); j := studyverse.join_room(c2, 'Riya', '🦊', 'school-g6'); perform pg_temp.chk((j ->> 'rejoin')::boolean, 'rejoin by link works for a member');
  perform pg_temp.as_user(A); j := studyverse.leave_room(c2); perform pg_temp.chk((pg_temp.room(c2)).host_id = H, 'host leaves → remaining player becomes host');
  perform pg_temp.as_user(H); j := studyverse.leave_room(c2); perform pg_temp.chk((pg_temp.room(c2)).code is null, 'last player leaving the lobby deletes the room');
  -- 1-v-1 capacity, leaving mid-game ends it
  perform pg_temp.as_user(H); j := studyverse.create_room('quiz', 'duel', 3, 10, 'Riya', '🦊', 'school-g6'); c2 := j ->> 'code';
  perform pg_temp.as_user(A); perform studyverse.join_room(c2, 'Asha', '🐯', 'school-g3'); perform studyverse.set_ready(c2, true);
  perform pg_temp.as_user(B); j := studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation'); perform pg_temp.chk(j ->> 'code' = 'full', '1-v-1 room is full at 2');
  perform pg_temp.as_user(H); perform studyverse.start_game(c2, jsonb_build_object('school-g6', pg_temp.qs(3, 'g6'), 'school-g3', pg_temp.qs(3, 'g3')));
  perform pg_temp.as_user(B); j := studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation'); perform pg_temp.chk(j ->> 'code' in ('started', 'full'), 'cannot join a started game');
  perform pg_temp.as_user(A); j := studyverse.leave_room(c2); perform pg_temp.chk((pg_temp.room(c2)).status = 'finished', 'opponent leaving a 1-v-1 ends the game');
  -- Speed duel normalises to 10 × 72 s
  perform pg_temp.as_user(B); j := studyverse.create_room('duel', 'duel', 5, 10, 'Kabir', '🎓', 'ca-foundation'); r := pg_temp.room(j ->> 'code');
  perform pg_temp.chk(r.rounds = 10 and r.turn_secs = 72, 'Speed Duel = 10 MCQs × 72 s');
  -- expired rooms are cleaned up
  reset role; update studyverse.game_rooms set expires_at = now() - interval '1 minute' where code = r.code; perform studyverse.live_cleanup(); set local role authenticated;
  perform pg_temp.chk((pg_temp.room(r.code)).code is null, 'expired room removed by live_cleanup()');
  begin perform studyverse.live_cleanup(); perform pg_temp.chk(false, 'clients must not run cleanup');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'live_cleanup is not callable by clients'); end;
end $$;

reset role;
do $$ begin
  raise notice '% checks, % failed', current_setting('lvtest.n'), current_setting('lvtest.fails');
  if current_setting('lvtest.fails')::int > 0 then raise exception 'live games tests: % FAILED', current_setting('lvtest.fails'); end if;
end $$;
rollback;
