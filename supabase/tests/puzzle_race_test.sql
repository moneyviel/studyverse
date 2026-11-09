-- ============================================================================================
-- SQL tests for supabase/migrations/20261110_puzzle_race.sql (Puzzle Race in Game Rooms).
-- Run AFTER 20261109_live_games.sql and 20261110_puzzle_race.sql, as a superuser:
--     psql "$DB_URL" -v ON_ERROR_STOP=1 -f supabase/tests/puzzle_race_test.sql
-- Everything happens inside BEGIN … ROLLBACK. Each check prints "PASS …" / "FAIL …" as a NOTICE; the script ends
-- with an ERROR if any check failed. Calls run as role "authenticated" with request.jwt.claims (like PostgREST).
-- Time is simulated by moving a room's clocks back (now() is fixed inside one transaction).
-- The Edge Function puzzle-key is played by pg_temp.key(): as service_role it calls puzzle_prepare + puzzle_set_key.
-- ============================================================================================
begin;
select set_config('pztest.fails', '0', true), set_config('pztest.n', '0', true);

create function pg_temp.chk(c boolean, m text) returns void language plpgsql as $$
begin
  perform set_config('pztest.n', (current_setting('pztest.n')::int + 1)::text, true);
  if coalesce(c, false) then raise notice 'PASS %', m;
  else perform set_config('pztest.fails', (current_setting('pztest.fails')::int + 1)::text, true); raise notice 'FAIL %', m; end if;
end $$;
create function pg_temp.as_user(u uuid) returns void language plpgsql as $$
begin perform set_config('request.jwt.claims', json_build_object('sub', u, 'role', 'authenticated')::text, true); end $$;
-- "time passes": move the room's deadline / start and every progress timestamp back by s seconds
create function pg_temp.rewind(c text, s int) returns void language plpgsql security definer as $$
begin
  update studyverse.game_rooms set deadline = deadline - make_interval(secs => s),
    state = state || case when state ? 'round_at' then jsonb_build_object('round_at', (state ->> 'round_at')::timestamptz - make_interval(secs => s)) else '{}'::jsonb end
  where code = c;
  update studyverse.room_answers set at = at - make_interval(secs => s) where code = c;
end $$;
create function pg_temp.room(c text) returns studyverse.game_rooms language sql security definer as $$ select * from studyverse.game_rooms where code = c $$;
create function pg_temp.pl(c text, u uuid) returns studyverse.room_players language sql security definer as $$ select * from studyverse.room_players where code = c and user_id = u $$;
create function pg_temp.res(c text, u uuid) returns studyverse.game_results language sql security definer as $$ select * from studyverse.game_results where code = c and user_id = u $$;
create function pg_temp.keys(c text) returns jsonb language sql security definer as $$ select keys from studyverse.room_keys where code = c $$;
-- the Edge Function's part: check the room, store the server-computed key (role service_role, like the function)
create function pg_temp.key(c text, host uuid, ans jsonb, bad_hash boolean default false) returns jsonb language plpgsql as $$
declare j jsonb;
begin
  set local role service_role;
  j := studyverse.puzzle_prepare(c, host);
  if (j ->> 'ok')::boolean then j := studyverse.puzzle_set_key(c, host, case when bad_hash then 'x' else j ->> 'h' end, ans); end if;
  set local role authenticated;
  return j;
end $$;
grant execute on all functions in schema pg_temp to authenticated, service_role;

insert into auth.users (id, email) values
  ('00000000-0000-0000-0000-0000000000b1', 'host@pz.test'), ('00000000-0000-0000-0000-0000000000b2', 'asha@pz.test'),
  ('00000000-0000-0000-0000-0000000000b3', 'ca@pz.test'),   ('00000000-0000-0000-0000-0000000000b4', 'out@pz.test');
insert into studyverse.course_access (user_id, course, valid_until, note) values
  ('00000000-0000-0000-0000-0000000000b1', 'school-g6', now() + interval '30 days', 'paid'),
  ('00000000-0000-0000-0000-0000000000b2', 'school-all', now() + interval '20 hours', 'trial'),
  ('00000000-0000-0000-0000-0000000000b3', 'ca-foundation', now() + interval '60 days', 'paid'),
  ('00000000-0000-0000-0000-0000000000b4', 'school-g6', now() + interval '30 days', 'paid');

set local role authenticated;
do $$
declare H uuid := '00000000-0000-0000-0000-0000000000b1'; A uuid := '00000000-0000-0000-0000-0000000000b2'; B uuid := '00000000-0000-0000-0000-0000000000b3';
  X uuid := '00000000-0000-0000-0000-0000000000b4';
  j jsonb; c text; c2 text; r studyverse.game_rooms; spec jsonb := '{"kind":"sdk","seed":"abc123","size":6,"diff":"easy","grade":6}';
  xw jsonb := '{"kind":"xw","seed":"s9","grade":6,"subject":"science","chapter":"ch03","size":"m"}'; st jsonb;
  sol text := '123456456123231564564231312645645312';     -- the 6×6 grid the server "computed" for spec
begin
  -- ===== create / settings =====
  perform pg_temp.as_user(H);
  j := studyverse.create_room('puzzle', 'teams', 99, 30, 'Riya Sharma', '🦊', 'school-g6-m24', 'mixed'); c := j ->> 'code'; r := pg_temp.room(c);
  perform pg_temp.chk((j ->> 'ok')::boolean and r.game = 'puzzle', 'create_room accepts game puzzle');
  perform pg_temp.chk(r.mode = 'ffa' and r.rounds = 8, 'puzzle: teams → free-for-all, odd minutes → 8');
  j := studyverse.update_room(c, 'puzzle', 'ffa', 5, 20, null); perform pg_temp.chk((pg_temp.room(c)).rounds = 5, 'time limit 5 minutes via update_room');
  j := studyverse.update_room(c, 'puzzle', 'ffa', 7, 20, null); perform pg_temp.chk((pg_temp.room(c)).rounds = 8, 'unsupported time limit falls back to 8');
  j := studyverse.update_room(c, 'puzzle', 'ffa', 3, 20, null);
  -- other games unchanged
  j := studyverse.create_room('quiz', 'ffa', 5, 15, 'Riya', '🦊', 'school-g6', 'easy'); r := pg_temp.room(j ->> 'code');
  perform pg_temp.chk(r.game = 'quiz' and r.rounds = 5 and r.turn_secs = 20 and r.level = 'easy', 'quiz create unchanged');
  j := studyverse.create_room('duel', 'ffa', 5, 10, 'Riya', '🦊', 'school-g6', null); r := pg_temp.room(j ->> 'code');
  perform pg_temp.chk(r.rounds = 10 and r.turn_secs = 72, 'duel create unchanged');
  j := studyverse.create_room('xword', 'ffa', 5, 10, 'Riya', '🦊', 'school-g6', null);
  perform pg_temp.chk(not (j ->> 'ok')::boolean, 'unknown game refused');

  -- ===== lobby: join, pick the puzzle =====
  perform pg_temp.as_user(A); j := studyverse.join_room(c, 'Asha', '🐯', 'school-g3');
  perform pg_temp.as_user(B); j := studyverse.join_room(c, 'Kabir', '🎓', 'ca-foundation');
  perform pg_temp.as_user(H);
  j := studyverse.puzzle_start(c); perform pg_temp.chk(j ->> 'code' = 'not_ready', 'start waits for ready players: ' || (j ->> 'msg'));
  perform pg_temp.as_user(A); perform studyverse.set_ready(c, true);
  perform pg_temp.as_user(B); perform studyverse.set_ready(c, true);
  j := studyverse.puzzle_set(c, 'sdk', spec, null); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'only the host picks the puzzle');
  perform pg_temp.as_user(H);
  j := studyverse.puzzle_start(c); perform pg_temp.chk(j ->> 'code' = 'no_puzzle', 'start needs a puzzle');
  j := studyverse.puzzle_set(c, 'SDK!', spec, null); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bad kind refused');
  j := studyverse.puzzle_set(c, 'sdk', '[1,2]'::jsonb, null); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'spec must be an object');
  j := studyverse.puzzle_set(c, 'sdk', jsonb_build_object('pad', repeat('x', 50000)), null); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'huge spec refused');
  j := studyverse.puzzle_set(c, 'xw', xw, jsonb_build_object('e', '📝', 'n', 'Crossword', 'ch', 'Ch 3 · Fibre to Fabric', 'd', 7));
  perform pg_temp.chk((j ->> 'ok')::boolean, 'host picks a chapter crossword');
  st := (studyverse.room_state(c) -> 'room' -> 'state');
  perform pg_temp.chk(st -> 'puzzle' ->> 'kind' = 'xw' and st -> 'puzzle' ->> 'ch' = 'Ch 3 · Fibre to Fabric' and st -> 'puzzle' ->> 'd' = '', 'lobby state shows the puzzle label (non-string detail dropped)');
  perform pg_temp.chk(not (studyverse.room_state(c)::text like '%s9%'), 'the spec is not in the polled lobby state');
  j := studyverse.update_room(c, 'quiz', 'ffa', 10, 20, null);
  perform pg_temp.chk((pg_temp.room(c)).state -> 'puzzle' is null and pg_temp.keys(c) is null, 'switching to another game drops the puzzle');
  j := studyverse.update_room(c, 'puzzle', 'ffa', 3, 20, null);
  j := studyverse.puzzle_set(c, 'sdk', spec, '{"e":"🔢","n":"Sudoku","d":"6×6 · easy"}');
  perform pg_temp.as_user(A); j := studyverse.puzzle_start(c); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'only the host starts');
  begin perform studyverse._puzzle_advance(c); perform pg_temp.chk(false, 'internal helper must not be callable');
  exception when insufficient_privilege then perform pg_temp.chk(true, '_puzzle_advance is not callable by clients'); end;

  -- ===== the answer key: server only =====
  perform pg_temp.as_user(H);
  j := studyverse.puzzle_start(c); perform pg_temp.chk(j ->> 'code' = 'no_key' and (pg_temp.room(c)).status = 'lobby', 'no server key → the race cannot start');
  begin perform studyverse.puzzle_prepare(c, H); perform pg_temp.chk(false, 'players must not call puzzle_prepare');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'puzzle_prepare is service-role only'); end;
  begin perform studyverse.puzzle_set_key(c, H, 'x', to_jsonb(sol)); perform pg_temp.chk(false, 'players must not set the key');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'puzzle_set_key is service-role only (a phone cannot supply the key)'); end;
  j := pg_temp.key(c, A, to_jsonb(sol)); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'key only for the host''s start');
  j := pg_temp.key(c, H, to_jsonb(sol), true); perform pg_temp.chk(j ->> 'code' = 'changed', 'key must match the current spec (hash)');
  j := pg_temp.key(c, H, '42'); perform pg_temp.chk(j ->> 'code' = 'bad_key', 'unusable key refused');
  j := pg_temp.key(c, H, to_jsonb(sol)); perform pg_temp.chk((j ->> 'ok')::boolean, 'server stores the key');
  j := studyverse.puzzle_set(c, 'sdk', spec, '{"e":"🔢","n":"Sudoku","d":"6×6 · easy"}');
  j := studyverse.puzzle_start(c); perform pg_temp.chk(j ->> 'code' = 'no_key', 'picking again drops the old key');
  j := pg_temp.key(c, H, jsonb_build_array('123456', '456123', '231564', '564231', '312645', '645312'));
  perform pg_temp.chk((j ->> 'ok')::boolean, 'grid key given as rows is stored row by row');
  begin perform count(*) from studyverse.room_keys; perform pg_temp.chk(false, 'keys must be unreadable');
  exception when insufficient_privilege then perform pg_temp.chk(true, 'room_keys is not readable by players'); end;

  -- ===== start =====
  perform pg_temp.as_user(H); j := studyverse.puzzle_start(c); r := pg_temp.room(c);
  perform pg_temp.chk((j ->> 'ok')::boolean and r.status = 'playing' and (j ->> 'minutes')::int = 3, 'race starts (3 min)');
  perform pg_temp.chk(r.deadline = (r.state ->> 'round_at')::timestamptz + interval '3 minutes', 'deadline = start + time limit');
  perform pg_temp.as_user(A); j := studyverse.room_state(c, true);
  perform pg_temp.chk(j -> 'questions' = spec, 'Class 3 player gets the host''s spec');
  perform pg_temp.as_user(B); j := studyverse.room_state(c, true);
  perform pg_temp.chk(j -> 'questions' = spec and j -> 'room' -> 'state' -> 'puzzle' ->> 'n' = 'Sudoku', 'CA player gets the same spec + label');
  perform pg_temp.as_user(X); j := studyverse.puzzle_progress(c, 1, 10); perform pg_temp.chk(j ->> 'code' = 'not_member', 'outsider cannot report');
  j := studyverse.join_room(c, 'Late', '🐢', 'school-g6'); perform pg_temp.chk(j ->> 'code' = 'started', 'no new players after the start');
  perform pg_temp.as_user(A);
  j := studyverse.puzzle_solved(c, to_jsonb(sol)); perform pg_temp.chk(j ->> 'code' = 'early', 'no solve before the countdown ends');
  perform pg_temp.chk(not (studyverse.room_state(c, true)::text like '%' || sol || '%'), 'the key is not in room_state');
  j := studyverse.puzzle_progress(c, 3, 10); perform pg_temp.chk(j ->> 'code' = 'early', 'no progress before the countdown ends');

  -- ===== progress =====
  perform pg_temp.rewind(c, 3);                             -- countdown over
  j := studyverse.puzzle_progress(c, 3, 10); perform pg_temp.chk((j ->> 'pct')::int = 30 and (pg_temp.pl(c, A)).answered = 30, 'progress 3/10 = 30 %');
  j := studyverse.puzzle_progress(c, 5, 10); perform pg_temp.chk((j ->> 'throttled')::boolean and (pg_temp.pl(c, A)).answered = 30, 'progress is rate-limited (2 s)');
  perform pg_temp.rewind(c, 3);
  j := studyverse.puzzle_progress(c, 12, 10); perform pg_temp.chk((pg_temp.pl(c, A)).answered = 99, 'progress capped at 99 % until solved');
  j := studyverse.puzzle_progress(c, 1, 0); perform pg_temp.chk(not (j ->> 'ok')::boolean, 'bad totals refused');
  perform pg_temp.chk(not exists (select 1 from jsonb_array_elements_text(studyverse.room_state(c) -> 'room' -> 'answered_ids')), 'progress rows do not show up as quiz answers');
  perform pg_temp.as_user(B); perform pg_temp.rewind(c, 3); j := studyverse.puzzle_progress(c, 2, 8);
  perform pg_temp.chk((pg_temp.pl(c, B)).answered = 25 and (pg_temp.pl(c, B)).score = 100, 'Kabir 25 % (score 100)');

  -- ===== advance does nothing before the end (also through the old advance()) =====
  j := studyverse.advance(c, (pg_temp.room(c)).step); perform pg_temp.chk(not (j ->> 'changed')::boolean and (pg_temp.room(c)).status = 'playing' and (pg_temp.room(c)).qi = 0, 'advance() leaves a running race alone');
  j := studyverse.puzzle_advance(c); perform pg_temp.chk(not (j ->> 'changed')::boolean, 'puzzle_advance waits');

  -- ===== checked solves: server time =====
  perform pg_temp.rewind(c, 40);                            -- countdown + 3 + 3 + 40 = 46 s since the start
  perform pg_temp.as_user(A);
  j := studyverse.puzzle_solved(c, to_jsonb(overlay(sol placing '9' from 1 for 1)), 0, 0);
  perform pg_temp.chk(j ->> 'code' = 'wrong' and j ->> 'msg' = 'Not solved yet — keep going!' and (j ->> 'wrong')::int = 1, 'wrong grid rejected: ' || j::text);
  perform pg_temp.chk((pg_temp.pl(c, A)).correct = 0 and (pg_temp.room(c)).state -> 'solved' = '[]'::jsonb, 'a wrong answer does not solve');
  j := studyverse.puzzle_solved(c, to_jsonb(sol)); perform pg_temp.chk(j ->> 'code' = 'slow', 'checks are rate-limited (3 s)');
  perform pg_temp.rewind(c, 4);
  j := studyverse.puzzle_solved(c, null::jsonb); perform pg_temp.chk(j ->> 'code' = 'wrong' and (j ->> 'wrong')::int = 2, 'no answer = not solved (counted)');
  perform pg_temp.rewind(c, 4);
  j := studyverse.puzzle_solved(c, '["123456"]'); perform pg_temp.chk(j ->> 'code' = 'wrong', 'part of the grid is not solved');
  perform pg_temp.rewind(c, 4);                             -- 46 + 12 = 58 s
  j := studyverse.puzzle_solved(c, to_jsonb(E' 123456 456123\n231564 564231 312645 645312 '::text), 1, 2);
  perform pg_temp.chk((j ->> 'ok')::boolean and (j ->> 'ms')::int = 58000 and (j ->> 'place')::int = 1, 'right grid (spaces ignored) → Asha first in 58 s (server time): ' || j::text);
  perform pg_temp.chk((pg_temp.pl(c, A)).correct = 1 and (pg_temp.pl(c, A)).answered = 100 and (pg_temp.pl(c, A)).total_ms = 58000, 'solve stored');
  perform pg_temp.chk((pg_temp.pl(c, A)).score between 1000 and 1500, 'solver score 1000–1500: ' || (pg_temp.pl(c, A)).score);
  j := studyverse.puzzle_solved(c, to_jsonb(sol)); perform pg_temp.chk((j ->> 'already')::boolean and (pg_temp.pl(c, A)).total_ms = 58000, 'only one solve per player');
  j := studyverse.puzzle_progress(c, 1, 10); perform pg_temp.chk((pg_temp.pl(c, A)).answered = 100, 'progress after solving is ignored');
  st := (pg_temp.room(c)).state;
  perform pg_temp.chk(jsonb_array_length(st -> 'solved') = 1 and st -> 'solved' -> 0 ->> 'u' = A::text and (st -> 'solved' -> 0 ->> 'h')::int = 1
    and (st -> 'solved' -> 0 ->> 'w')::int = 3, 'solved list with hints + server-counted wrong checks');
  perform pg_temp.rewind(c, 20);
  perform pg_temp.as_user(H); j := studyverse.puzzle_solved(c, to_jsonb(lower(sol)));
  perform pg_temp.chk((j ->> 'ms')::int = 78000 and (j ->> 'place')::int = 2 and (pg_temp.pl(c, H)).score < (pg_temp.pl(c, A)).score, 'host solves second, lower score');
  perform pg_temp.chk((pg_temp.room(c)).status = 'playing', 'race goes on while Kabir is still solving');

  -- ===== deadline =====
  perform pg_temp.as_user(B);
  perform pg_temp.rewind(c, 3 * 60);
  j := studyverse.puzzle_solved(c, to_jsonb(sol)); perform pg_temp.chk(j ->> 'code' = 'late', 'no solve after the deadline');
  j := studyverse.advance(c, -5); perform pg_temp.chk((j ->> 'changed')::boolean and (pg_temp.room(c)).status = 'finished', 'deadline: advance() (any step) finishes the race');
  perform pg_temp.chk((pg_temp.res(c, A)).rank = 1 and (pg_temp.res(c, A)).won and (pg_temp.res(c, H)).rank = 2 and (pg_temp.res(c, B)).rank = 3 and not (pg_temp.res(c, B)).won,
    'ranking: Asha (fastest), Riya, Kabir (unsolved)');
  perform pg_temp.chk((pg_temp.res(c, A)).game = 'puzzle' and (pg_temp.room(c)).state -> 'puzzle' ->> 'n' = 'Sudoku', 'results keep the game + puzzle label');
  j := studyverse.weekly_board(); perform pg_temp.chk(jsonb_array_length(j) = 3, 'weekly board counts the race');

  -- ===== rematch → lobby, puzzle must be picked again =====
  perform pg_temp.as_user(H); j := studyverse.rematch(c); r := pg_temp.room(c);
  perform pg_temp.chk(r.status = 'lobby' and r.game = 'puzzle' and r.rounds = 3 and r.state -> 'puzzle' is null, 'rematch: same game + time, new puzzle to pick');

  -- ===== everyone solves → finishes at once; leaving + unsolved =====
  j := studyverse.create_room('puzzle', 'duel', 10, 20, 'Riya', '🦊', 'school-g6', null); c2 := j ->> 'code';
  perform pg_temp.as_user(A); perform studyverse.join_room(c2, 'Asha', '🐯', 'school-g3'); perform studyverse.set_ready(c2, true);
  perform pg_temp.as_user(B); j := studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation'); perform pg_temp.chk(j ->> 'code' = 'full', '1-v-1 puzzle room is full at 2');
  perform pg_temp.as_user(H); perform studyverse.puzzle_set(c2, 'kak', '{"seed":1}', '{"e":"➕","n":"Kakuro"}');
  perform pg_temp.key(c2, H, '"#12#34#56"'); j := studyverse.puzzle_start(c2);
  perform pg_temp.chk((j ->> 'minutes')::int = 10, '10-minute race');
  perform pg_temp.rewind(c2, 10);
  j := studyverse.puzzle_solved(c2, '"#12#34#56"');
  perform pg_temp.as_user(A); perform pg_temp.rewind(c2, 5); j := studyverse.puzzle_solved(c2, '"#12#34#56"');
  perform pg_temp.chk((pg_temp.room(c2)).status = 'finished', 'everyone solved → race finishes at once');
  perform pg_temp.chk((pg_temp.res(c2, H)).won and not (pg_temp.res(c2, A)).won, 'faster solver wins');
  -- a player leaves: the other one alone → finished (existing leave_room rule)
  -- word search = a SET of words (any order, case, duplicates); crossword = words in entry order
  perform pg_temp.as_user(H); perform studyverse.rematch(c2); perform studyverse.puzzle_set(c2, 'ws', '{"seed":2}', null);
  perform pg_temp.as_user(A); perform studyverse.set_ready(c2, true);
  perform pg_temp.as_user(H); perform pg_temp.key(c2, H, '["EMU","cat","Dog"]'); perform studyverse.puzzle_start(c2); perform pg_temp.rewind(c2, 4);
  j := studyverse.puzzle_solved(c2, '["dog","CAT"]'); perform pg_temp.chk(j ->> 'code' = 'wrong', 'word search: a missing word is not solved');
  perform pg_temp.rewind(c2, 4);
  j := studyverse.puzzle_solved(c2, '["dog","emu","CAT","cat"]'); perform pg_temp.chk((j ->> 'ok')::boolean, 'word search: all words in any order → solved');
  perform pg_temp.as_user(A); perform studyverse.leave_room(c2);
  perform pg_temp.chk((pg_temp.room(c2)).status = 'finished' and (pg_temp.res(c2, H)).won, 'opponent leaves → race over, host wins');
  perform pg_temp.as_user(H); perform studyverse.rematch(c2); perform studyverse.puzzle_set(c2, 'xw', xw, null);
  perform pg_temp.as_user(B); perform studyverse.join_room(c2, 'Kabir', '🎓', 'ca-foundation'); perform studyverse.set_ready(c2, true);
  perform pg_temp.key(c2, H, '["FIBRE","WOOL","SILK"]');
  perform pg_temp.as_user(H); perform studyverse.puzzle_start(c2); perform pg_temp.rewind(c2, 4);
  perform pg_temp.as_user(B);
  j := studyverse.puzzle_solved(c2, '["WOOL","FIBRE","SILK"]'); perform pg_temp.chk(j ->> 'code' = 'wrong', 'crossword: words in the wrong entries are not solved');
  perform pg_temp.rewind(c2, 4);
  j := studyverse.puzzle_solved(c2, '[1,2,3]'); perform pg_temp.chk(j ->> 'code' = 'wrong', 'crossword: non-text answer refused');
  perform pg_temp.rewind(c2, 4);
  j := studyverse.puzzle_solved(c2, '["fibre","wool","silk"]'); perform pg_temp.chk((j ->> 'ok')::boolean, 'crossword: right words in entry order → solved');
  -- no key in the room (e.g. stored key lost) → nobody can solve
  reset role; update studyverse.room_keys set keys = keys - 'answer' where code = c2; set local role authenticated;
  perform pg_temp.as_user(H);
  j := studyverse.puzzle_solved(c2, '["FIBRE","WOOL","SILK"]'); perform pg_temp.chk(j ->> 'code' = 'no_key' and (pg_temp.pl(c2, H)).correct = 0, 'no key → cannot be marked solved');
  perform pg_temp.chk(not exists (select 1 from pg_proc p join pg_namespace n on n.oid = p.pronamespace where n.nspname = 'studyverse' and p.proname = 'puzzle_solved' and pronargs = 3),
    'no answer-less puzzle_solved left');
end $$;

reset role;
do $$ begin
  raise notice '% checks, % failed', current_setting('pztest.n'), current_setting('pztest.fails');
  if current_setting('pztest.fails')::int > 0 then raise exception 'puzzle race tests: % FAILED', current_setting('pztest.fails'); end if;
end $$;
rollback;
