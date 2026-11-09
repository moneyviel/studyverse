-- ============================================================================================
-- StudyVerse LIVE "Puzzle Race" (game 'puzzle') for Game Rooms. ADDITIVE on top of 20261109_live_games.sql
-- (apply that one first). Replaces the need for the unapplied draft 20261109_puzzles.sql ('xword'): do NOT apply both.
--
-- Every puzzle kind of js/puzzles.js (Sudoku, Kakuro, Crossword, Word search, Anagram, Concept sudoku) can be raced:
--   1. host creates / switches a room to game 'puzzle' (create_room / update_room; p_rounds = time limit in MINUTES:
--      3, 5, 8 or 10, default 8; modes 1-v-1 or free-for-all, no teams)
--   2. host picks a puzzle in the lobby → puzzle_set(p_code, p_kind, p_spec, p_info)
--        p_spec = JSON spec from Puzzles.pick() (grade/subject/chapter + seed + size/difficulty) that rebuilds the
--                 IDENTICAL puzzle on any device. Kept in room_keys while in the lobby (not polled by everyone).
--        p_info = small public label { e, n, ch, d } shown in the lobby (emoji, kind name, chapter, detail).
--      Fairness: EVERYONE gets the host's spec — number puzzles (same grid) and chapter puzzles alike (same chapter, same
--      puzzle; the spec carries grade/subject so a friend in another class can still load it).
--   3. host taps Start → the app calls the Edge Function supabase/functions/puzzle-key (host JWT). It checks the room
--      through puzzle_prepare() (service role), builds the puzzle from the spec ON THE SERVER with js/puzzles-core.js
--      (PuzzleCore.solutionOf), stores the canonical answer with puzzle_set_key() (service role → room_keys, which no
--      client can read) and then calls puzzle_start() as the host. puzzle_start() refuses to start without that key, so
--      no player's phone (not even the host's) ever supplies the answer key. Any new puzzle_set() drops the key.
--      puzzle_start: same rules as start_game (host only, lobby, everyone ready, ≥ 2 players, 1-v-1 = exactly 2).
--      The spec is copied to game_rooms.questions under every player's course, so room_state(p_q => true) hands it to
--      each player. state = { puzzle: info, mins, solved: [{u, ms, h, m, w}] }. The race starts 3 s later
--      (state.round_at); deadline = round_at + minutes.
--   4. players: puzzle_progress(p_code, p_done, p_total)   (≤ 1 write per 2 s per player; room_players.answered = %)
--               puzzle_solved(p_code, p_answer, p_hints, p_mistakes)   the player's ANSWER is compared with the stored
--               key. Wrong → { ok: false, code: 'wrong' } and a counted wrong check; right → solved, timed by the
--               SERVER from its own round_at. ≤ 1 check per 3 s. This is the ONLY way to be marked solved.
--      Canonical answers (_puzzle_norm, applied to both the key and the player's answer):
--        sdk / csdk / kak (and any string): the grid row by row, whitespace removed, upper-case
--        xw / ana (and any other array): the words in puzzle order, whitespace removed, upper-case
--        ws: the set of found words (deduplicated, sorted)
--   5. any member: puzzle_advance(p_code) finishes the race when every active player has solved it or the deadline
--      has passed (+1.5 s grace). advance() also routes 'puzzle' rooms here, so an older client can never push a
--      puzzle room through the quiz round logic.
-- Ranking (through the existing _live_finish: score desc, correct desc, total_ms asc):
--      solved   → correct = 1, total_ms = server time, score = 1000 + round(500 × (1 − time / time limit))  (1000–1500)
--      unsolved → correct = 0, total_ms = 0,           score = 4 × progress %  (0–396)
--   so solvers always rank above non-solvers, faster solvers above slower ones, then progress. Scores are in the
--   same range as a 10-question Quiz Race, so results, the weekly board and badges keep working.
-- Limit: each phone builds the puzzle from the spec to show it, so a determined person could run the engine by hand.
-- What the server guarantees: nobody is marked solved without submitting the correct complete answer, the key never
-- comes from a phone and is never readable, and times / order are the server's.
--
-- Changes to existing objects (behaviour for the other games is unchanged):
--   • game_rooms_game_check also allows 'puzzle'
--   • create_room / update_room (the 8- / 6-argument versions) accept 'puzzle'; for other games they are identical
--   • advance(): 'puzzle' rooms go to _puzzle_advance(); other games run exactly the old code
-- Deploy together with the Edge Function puzzle-key (see its header): without it a puzzle race cannot start.
-- Idempotent: safe to run again.
-- ============================================================================================

alter table studyverse.game_rooms drop constraint if exists game_rooms_game_check;
alter table studyverse.game_rooms add constraint game_rooms_game_check check (game in ('snakes', 'quiz', 'relay', 'buzzer', 'duel', 'puzzle'));

-- ---------- internal helpers ----------
-- the room's race should end: everyone active has solved it, or the time limit (+1.5 s grace) is over
create or replace function studyverse._puzzle_over(p_code text) returns boolean
language plpgsql stable security definer set search_path = '' as $$
declare r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = p_code;
  if not found or r.status <> 'playing' or r.game <> 'puzzle' then return false; end if;
  if r.deadline is not null and now() > r.deadline + interval '1.5 seconds' then return true; end if;
  return not exists (select 1 from studyverse.room_players where code = p_code and left_at is null and correct < 1);
end $$;

create or replace function studyverse._puzzle_advance(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = p_code for update;
  if not found or r.status <> 'playing' or r.game <> 'puzzle' then return jsonb_build_object('ok', true, 'changed', false); end if;
  if not studyverse._puzzle_over(p_code) then return jsonb_build_object('ok', true, 'changed', false); end if;
  perform studyverse._live_finish(p_code);
  return jsonb_build_object('ok', true, 'changed', true);
end $$;

revoke all on function studyverse._puzzle_over(text), studyverse._puzzle_advance(text) from public, anon, authenticated;

-- ---------- create_room: + 'puzzle' (p_rounds = minutes 3/5/8/10, default 8; no teams) ----------
create or replace function studyverse.create_room(p_game text, p_mode text, p_rounds int, p_turn_secs int, p_name text, p_avatar text, p_course text, p_level text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); w text := studyverse._live_why(auth.uid()); k text; alph text := 'ABCDEFGHJKLMNPQRSTUVWXYZ'; i int; g text; m text; rd int; ts int;
begin
  if w <> 'ok' then return studyverse._live_err(studyverse._live_msg(w), w); end if;
  if coalesce(p_course, '') !~ '^[a-z0-9-]{2,40}$' then return studyverse._live_err('Unknown course.'); end if;
  g := coalesce(p_game, 'quiz'); m := coalesce(p_mode, 'ffa'); rd := coalesce(p_rounds, 10); ts := coalesce(p_turn_secs, 20);
  if g not in ('snakes', 'quiz', 'relay', 'buzzer', 'duel', 'puzzle') or m not in ('duel', 'ffa', 'teams') then return studyverse._live_err('Unknown game or mode.'); end if;
  if g = 'relay' then m := 'teams'; end if;
  if g = 'puzzle' then
    if m = 'teams' then m := 'ffa'; end if;
    if rd not in (3, 5, 8, 10) then rd := 8; end if; ts := 20;
  elsif g = 'duel' then rd := 10; ts := 72; else rd := greatest(3, least(30, rd)); if ts not in (10, 20, 30) then ts := 20; end if; end if;
  perform studyverse.live_cleanup();
  if (select count(*) from studyverse.game_rooms where host_id = uid and created_at > now() - interval '1 hour') >= 12 then
    return studyverse._live_err('Too many rooms made this hour. Please try again later.');
  end if;
  loop
    k := ''; for i in 1..6 loop k := k || substr(alph, 1 + floor(random() * length(alph))::int, 1); end loop;
    exit when not exists (select 1 from studyverse.game_rooms where code = k);
  end loop;
  insert into studyverse.game_rooms (code, host_id, game, mode, rounds, turn_secs, level)
    values (k, uid, g, m, rd, ts, case when p_level in ('easy', 'moderate', 'hard') then p_level else 'mixed' end);
  insert into studyverse.room_players (code, user_id, name, avatar, course, team, seat, ready)
    values (k, uid, studyverse._live_first(p_name), coalesce(nullif(left(trim(coalesce(p_avatar, '')), 8), ''), '🙂'), p_course, case when m = 'teams' then 0 end, 1, true);
  return jsonb_build_object('ok', true, 'code', k);
end $$;

-- ---------- update_room: + 'puzzle'; leaving 'puzzle' drops the chosen puzzle ----------
create or replace function studyverse.update_room(p_code text, p_game text, p_mode text, p_rounds int, p_turn_secs int, p_level text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; g text; m text; rd int; ts int; n int; pl record; t0 int := 0; t1 int := 0;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> uid then return studyverse._live_err('Only the host can change the game.'); end if;
  if r.status <> 'lobby' then return studyverse._live_err('The game has already started.'); end if;
  g := coalesce(p_game, r.game); m := coalesce(p_mode, r.mode); rd := coalesce(p_rounds, r.rounds); ts := coalesce(p_turn_secs, r.turn_secs);
  if g not in ('snakes', 'quiz', 'relay', 'buzzer', 'duel', 'puzzle') or m not in ('duel', 'ffa', 'teams') then return studyverse._live_err('Unknown game or mode.'); end if;
  if g = 'relay' then m := 'teams'; end if;
  if g = 'puzzle' then
    if m = 'teams' then m := 'ffa'; end if;
    if rd not in (3, 5, 8, 10) then rd := 8; end if; ts := 20;
  elsif g = 'duel' then rd := 10; ts := 72; else rd := greatest(3, least(30, rd)); if ts not in (10, 20, 30) then ts := 20; end if; end if;
  select count(*) into n from studyverse.room_players where code = c;
  if m = 'duel' and n > 2 then return studyverse._live_err('1-v-1 needs exactly 2 players. Remove players first.'); end if;
  if m = 'teams' and r.mode <> 'teams' then
    for pl in select user_id from studyverse.room_players where code = c order by seat loop
      update studyverse.room_players set team = case when t1 < t0 then 1 else 0 end where code = c and user_id = pl.user_id;
      if t1 < t0 then t1 := t1 + 1; else t0 := t0 + 1; end if;
    end loop;
  elsif m <> 'teams' then update studyverse.room_players set team = null where code = c;
  end if;
  if g <> 'puzzle' and r.game = 'puzzle' then delete from studyverse.room_keys where code = c; end if;
  update studyverse.game_rooms set game = g, mode = m, rounds = rd, turn_secs = ts, step = step + 1,
    state = case when g = 'puzzle' then state else state - 'puzzle' end,
    level = case when p_level in ('mixed', 'easy', 'moderate', 'hard') then p_level else level end where code = c;
  return jsonb_build_object('ok', true);
end $$;

-- ---------- host: choose the puzzle (lobby) ----------
-- p_kind: Puzzles.kinds() id ('sdk', 'kak', 'xw', 'ws', 'ana', 'csdk' …); p_spec: Puzzles.pick() result (≤ 40 kB JSON object);
-- p_info: { e: emoji, n: kind name, ch: chapter label, d: detail like "9×9 · hard" } (shown to everyone in the lobby)
create or replace function studyverse.puzzle_set(p_code text, p_kind text, p_spec jsonb, p_info jsonb default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; inf jsonb;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> uid then return studyverse._live_err('Only the host can choose the puzzle.'); end if;
  if r.status <> 'lobby' then return studyverse._live_err('The game has already started.'); end if;
  if r.game <> 'puzzle' then return studyverse._live_err('Switch the room to Puzzle Race first.'); end if;
  if coalesce(p_kind, '') !~ '^[a-z0-9]{2,12}$' then return studyverse._live_err('Unknown puzzle.'); end if;
  if p_spec is null or jsonb_typeof(p_spec) <> 'object' or length(p_spec::text) > 40000 then return studyverse._live_err('That puzzle could not be shared. Try another one.'); end if;
  inf := case when jsonb_typeof(p_info) = 'object' then p_info else '{}'::jsonb end;
  inf := jsonb_build_object('kind', p_kind,
    'e', left(coalesce(case when jsonb_typeof(inf -> 'e') = 'string' then inf ->> 'e' end, '🧩'), 8),
    'n', left(coalesce(case when jsonb_typeof(inf -> 'n') = 'string' then inf ->> 'n' end, 'Puzzle'), 40),
    'ch', left(coalesce(case when jsonb_typeof(inf -> 'ch') = 'string' then inf ->> 'ch' end, ''), 120),
    'd', left(coalesce(case when jsonb_typeof(inf -> 'd') = 'string' then inf ->> 'd' end, ''), 60));
  insert into studyverse.room_keys (code, keys) values (c, jsonb_build_object('puzzle', p_spec, 'kind', p_kind))
    on conflict (code) do update set keys = excluded.keys;
  update studyverse.game_rooms set state = state || jsonb_build_object('puzzle', inf), step = step + 1 where code = c;
  return jsonb_build_object('ok', true, 'puzzle', inf);
end $$;

-- ---------- canonical answer form (used for the stored key AND every player's answer) ----------
-- NULL = not a usable answer. Strings: whitespace removed, upper-case. Arrays (strings only, ≤ 400): each item the same;
-- 'ws' (word search) compares the SET of words (deduplicated, sorted byte-wise); other kinds keep the puzzle order.
-- Grid kinds also accept an array of rows (joined row by row).
create or replace function studyverse._puzzle_norm(p_kind text, p_v jsonb) returns jsonb
language plpgsql immutable set search_path = '' as $$
declare t text; arr text[];
begin
  if p_v is null or length(p_v::text) > 20000 then return null; end if;
  if jsonb_typeof(p_v) = 'string' then
    t := upper(regexp_replace(p_v #>> '{}', '\s', '', 'g'));
    return case when t = '' then null else to_jsonb(t) end;
  end if;
  if jsonb_typeof(p_v) <> 'array' or jsonb_array_length(p_v) = 0 or jsonb_array_length(p_v) > 400 then return null; end if;
  if exists (select 1 from jsonb_array_elements(p_v) e where jsonb_typeof(e) <> 'string') then return null; end if;
  select array_agg(upper(regexp_replace(e #>> '{}', '\s', '', 'g')) order by o) into arr from jsonb_array_elements(p_v) with ordinality x(e, o);
  if p_kind in ('sdk', 'csdk', 'kak') then
    t := array_to_string(arr, ''); return case when t = '' then null else to_jsonb(t) end;
  end if;
  if p_kind = 'ws' then
    select array_agg(w order by w collate "C") into arr from (select distinct w from unnest(arr) w where w <> '') d;
    return case when arr is null then null else to_jsonb(arr) end;
  end if;
  return to_jsonb(arr);
end $$;

-- the start rules shared by puzzle_prepare (Edge Function) and puzzle_start: null = OK, else an error object
create or replace function studyverse._puzzle_problem(p_code text, p_uid uuid) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare r studyverse.game_rooms; act int; notready text;
begin
  select * into r from studyverse.game_rooms where code = p_code;
  if not found or p_uid is null or r.host_id <> p_uid then return studyverse._live_err('Only the host can start the game.'); end if;
  if r.status <> 'lobby' then return studyverse._live_err('The game has already started.'); end if;
  if r.game <> 'puzzle' then return studyverse._live_err('This room is not a Puzzle Race.'); end if;
  select count(*) into act from studyverse.room_players where code = p_code and left_at is null;
  if act < 2 then return studyverse._live_err('You need at least 2 players.'); end if;
  if r.mode = 'duel' and act <> 2 then return studyverse._live_err('1-v-1 needs exactly 2 players.'); end if;
  select string_agg(name, ', ' order by seat) into notready from studyverse.room_players where code = p_code and left_at is null and not ready and user_id <> r.host_id;
  if notready is not null then return studyverse._live_err('Waiting for ' || notready || ' to be ready.', 'not_ready'); end if;
  if r.state -> 'puzzle' is null or not exists (select 1 from studyverse.room_keys where code = p_code and keys ? 'puzzle') then
    return studyverse._live_err('Pick a puzzle first.', 'no_puzzle'); end if;
  return null;
end $$;

revoke all on function studyverse._puzzle_norm(text, jsonb), studyverse._puzzle_problem(text, uuid) from public, anon, authenticated;

-- ---------- Edge Function (service role): what must be solved? ----------
create or replace function studyverse.puzzle_prepare(p_code text, p_user uuid) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, ''))); e jsonb; k jsonb;
begin
  e := studyverse._puzzle_problem(c, p_user); if e is not null then return e; end if;
  select keys into k from studyverse.room_keys where code = c;
  return jsonb_build_object('ok', true, 'kind', k ->> 'kind', 'spec', k -> 'puzzle', 'h', md5((k -> 'puzzle')::text));
end $$;

-- ---------- Edge Function (service role): store the server-computed key for exactly that spec (p_hash) ----------
create or replace function studyverse.puzzle_set_key(p_code text, p_user uuid, p_hash text, p_answer jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; k jsonb; a jsonb;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or p_user is null or r.host_id <> p_user then return studyverse._live_err('Only the host can start the game.'); end if;
  if r.status <> 'lobby' or r.game <> 'puzzle' then return studyverse._live_err('The game has already started.'); end if;
  select keys into k from studyverse.room_keys where code = c for update;
  if k is null or not (k ? 'puzzle') or md5((k -> 'puzzle')::text) is distinct from p_hash then
    return studyverse._live_err('The puzzle was changed. Please tap Start again.', 'changed'); end if;
  a := studyverse._puzzle_norm(k ->> 'kind', p_answer);
  if a is null then return studyverse._live_err('This puzzle could not be prepared. Please pick another one.', 'bad_key'); end if;
  update studyverse.room_keys set keys = keys || jsonb_build_object('answer', a) where code = c;
  return jsonb_build_object('ok', true);
end $$;

-- ---------- host: start the race (same start rules as start_game; needs the server-computed key) ----------
create or replace function studyverse.puzzle_start(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; e jsonb; k jsonb; pub jsonb; mins int;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  e := studyverse._puzzle_problem(c, uid); if e is not null then return e; end if;
  select keys into k from studyverse.room_keys where code = c;
  if k -> 'answer' is null then return studyverse._live_err('The puzzle is not ready yet. Please tap Start again.', 'no_key'); end if;
  -- the same spec for everyone, under each player's course (room_state hands questions -> my course to each player)
  select jsonb_object_agg(course, k -> 'puzzle') into pub from (select distinct course from studyverse.room_players where code = c) s;
  mins := case when r.rounds in (3, 5, 8, 10) then r.rounds else 8 end;
  delete from studyverse.room_answers where code = c;
  delete from studyverse.room_players where code = c and left_at is not null;
  update studyverse.room_players set score = 0, correct = 0, answered = 0, total_ms = 0, pos = 1, qn = 0 where code = c;
  update studyverse.game_rooms set status = 'playing', started_at = now(), finished_at = null, questions = pub, qi = 0, step = step + 1, turn_user = null,
    deadline = now() + interval '3 seconds' + make_interval(mins => mins),
    state = jsonb_build_object('puzzle', r.state -> 'puzzle', 'mins', mins, 'round_at', now() + interval '3 seconds', 'solved', '[]'::jsonb)
  where code = c;
  return jsonb_build_object('ok', true, 'minutes', mins);
end $$;

-- ---------- player: progress (done / total cells or words); at most one write per 2 s ----------
create or replace function studyverse.puzzle_progress(p_code text, p_done int, p_total int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; me studyverse.room_players; pct int; last timestamptz;
begin
  select * into r from studyverse.game_rooms where code = c;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  select * into me from studyverse.room_players where code = c and user_id = uid and left_at is null;
  if not found then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  if r.status <> 'playing' or r.game <> 'puzzle' then return studyverse._live_err('No puzzle race is running.', 'not_playing'); end if;
  if me.correct >= 1 then return jsonb_build_object('ok', true, 'solved', true); end if;
  if now() < (r.state ->> 'round_at')::timestamptz then return studyverse._live_err('Wait for the start!', 'early'); end if;
  if now() > r.deadline + interval '1.5 seconds' then return studyverse._live_err('Time is up.', 'late'); end if;
  if p_total is null or p_total < 1 or p_total > 10000 or p_done is null or p_done < 0 then return studyverse._live_err('Bad progress.'); end if;
  -- rate limit: the progress row (qi = -1) remembers the last write
  select at into last from studyverse.room_answers where code = c and qi = -1 and user_id = uid;
  if last is not null and now() < last + interval '2 seconds' then return jsonb_build_object('ok', true, 'throttled', true); end if;
  pct := least(99, greatest(0, floor(100.0 * least(p_done, p_total) / p_total)::int));      -- 100 % only through a checked solve
  insert into studyverse.room_answers (code, qi, user_id, choice, correct, ms, points, at) values (c, -1, uid, pct, false, 0, 0, now())
    on conflict (code, qi, user_id) do update set choice = excluded.choice, at = excluded.at;
  update studyverse.room_players set answered = pct, score = 4 * pct, last_seen = now() where code = c and user_id = uid;
  return jsonb_build_object('ok', true, 'pct', pct);
end $$;

-- ---------- player: "I think I solved it" → the server checks the ANSWER against the key (≤ 1 check per 3 s) ----------
drop function if exists studyverse.puzzle_solved(text, int, int);          -- earlier local draft without an answer
create or replace function studyverse.puzzle_solved(p_code text, p_answer jsonb, p_hints int default 0, p_mistakes int default 0) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; me studyverse.room_players; k jsonb; last timestamptz; wrong int := 0;
  ms int; lim int; pts int; place int;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  select * into me from studyverse.room_players where code = c and user_id = uid and left_at is null;
  if not found then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  if r.status <> 'playing' or r.game <> 'puzzle' then return studyverse._live_err('No puzzle race is running.', 'not_playing'); end if;
  if me.correct >= 1 then return jsonb_build_object('ok', true, 'already', true, 'ms', me.total_ms); end if;
  if now() < (r.state ->> 'round_at')::timestamptz then return studyverse._live_err('Wait for the start!', 'early'); end if;
  if now() > r.deadline + interval '1.5 seconds' then return studyverse._live_err('Time is up.', 'late'); end if;
  select keys into k from studyverse.room_keys where code = c;
  if k -> 'answer' is null then return studyverse._live_err('This race has no answer key, so it cannot be checked.', 'no_key'); end if;
  -- rate limit + wrong-check counter: the check row (qi = -2): at = last check, points = wrong checks
  select at, points into last, wrong from studyverse.room_answers where code = c and qi = -2 and user_id = uid;
  if last is not null and now() < last + interval '3 seconds' then return studyverse._live_err('Checking… try again in a moment.', 'slow'); end if;
  if studyverse._puzzle_norm(k ->> 'kind', p_answer) is distinct from k -> 'answer' then
    insert into studyverse.room_answers (code, qi, user_id, choice, correct, ms, points, at) values (c, -2, uid, 0, false, 0, 1, now())
      on conflict (code, qi, user_id) do update set points = studyverse.room_answers.points + 1, at = excluded.at;
    return studyverse._live_err('Not solved yet — keep going!', 'wrong') || jsonb_build_object('wrong', coalesce(wrong, 0) + 1);
  end if;
  insert into studyverse.room_answers (code, qi, user_id, choice, correct, ms, points, at) values (c, -2, uid, 1, true, 0, 0, now())
    on conflict (code, qi, user_id) do update set choice = 1, correct = true, at = excluded.at;
  ms := greatest(0, (extract(epoch from (now() - (r.state ->> 'round_at')::timestamptz)) * 1000)::int);
  lim := greatest(1, coalesce((r.state ->> 'mins')::int, 8)) * 60000;
  pts := 1000 + round(500 * greatest(0, 1 - ms::numeric / lim))::int;
  update studyverse.room_players set correct = 1, answered = 100, total_ms = ms, score = pts, last_seen = now() where code = c and user_id = uid;
  place := jsonb_array_length(coalesce(r.state -> 'solved', '[]'::jsonb)) + 1;
  update studyverse.game_rooms set step = step + 1,
    state = jsonb_set(state, '{solved}', coalesce(state -> 'solved', '[]'::jsonb) || jsonb_build_array(jsonb_build_object('u', uid, 'ms', ms,
      'h', least(99, greatest(0, coalesce(p_hints, 0))), 'm', least(999, greatest(0, coalesce(p_mistakes, 0))), 'w', coalesce(wrong, 0))))
  where code = c;
  if studyverse._puzzle_over(c) then perform studyverse._live_finish(c); end if;
  return jsonb_build_object('ok', true, 'ms', ms, 'place', place, 'points', pts);
end $$;

-- ---------- any member: finish the race when it is really over ----------
create or replace function studyverse.puzzle_advance(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, '')));
begin
  if not exists (select 1 from studyverse.room_players where code = c and user_id = auth.uid()) then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  return studyverse._puzzle_advance(c);
end $$;

-- ---------- advance(): unchanged for every other game; 'puzzle' rooms use _puzzle_advance ----------
create or replace function studyverse.advance(p_code text, p_step int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; gone boolean; act int; nout int; reveal interval := interval '2 seconds';
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  if not exists (select 1 from studyverse.room_players where code = c and user_id = uid) then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  if r.game = 'puzzle' then return studyverse._puzzle_advance(c); end if;               -- Puzzle Race: no rounds (ignores p_step)
  if r.status <> 'playing' or p_step is distinct from r.step then return jsonb_build_object('ok', true, 'changed', false); end if;

  if r.game = 'snakes' then
    gone := not exists (select 1 from studyverse.room_players where code = c and user_id = r.turn_user and left_at is null and last_seen > now() - interval '45 seconds');
    if now() <= r.deadline + interval '1.5 seconds' and not gone then return jsonb_build_object('ok', true, 'changed', false); end if;
    if r.state -> 'gate' is not null then perform studyverse._live_gate(c, false, true);
    else
      update studyverse.game_rooms set state = state || jsonb_build_object('last', jsonb_build_object('user', r.turn_user, 'skip', true)) where code = c;
      perform studyverse._live_next_turn(c);
    end if;
    return jsonb_build_object('ok', true, 'changed', true);
  end if;

  if r.game = 'buzzer' then
    if r.turn_user is not null then                                  -- the buzzer ran out of time to answer
      if now() <= r.deadline + interval '1.5 seconds' then return jsonb_build_object('ok', true, 'changed', false); end if;
      select count(*) into act from studyverse.room_players where code = c and left_at is null;
      nout := jsonb_array_length(coalesce(r.state -> 'out', '[]'::jsonb)) + 1;
      update studyverse.game_rooms set turn_user = null, step = step + 1,
        deadline = case when nout >= act then now() else now() + make_interval(secs => r.turn_secs) end,
        state = (state - 'buzz') || jsonb_build_object('out', coalesce(state -> 'out', '[]'::jsonb) || to_jsonb(r.turn_user::text))
                || case when nout >= act then jsonb_build_object('done', true, 'done_at', now()) else '{}'::jsonb end
      where code = c;
      return jsonb_build_object('ok', true, 'changed', true);
    end if;
    if coalesce((r.state ->> 'done')::boolean, false) then
      if now() < (r.state ->> 'done_at')::timestamptz + reveal then return jsonb_build_object('ok', true, 'changed', false); end if;
    elsif now() < r.deadline + reveal then return jsonb_build_object('ok', true, 'changed', false);
    end if;
    perform studyverse._live_next_round(c);
    return jsonb_build_object('ok', true, 'changed', true);
  end if;

  -- quiz / duel / relay
  if not coalesce((r.state ->> 'done')::boolean, false) and studyverse._live_complete(c) then
    update studyverse.game_rooms set state = state || jsonb_build_object('done', true, 'done_at', now()) where code = c;
    return jsonb_build_object('ok', true, 'changed', true);
  end if;
  if coalesce((r.state ->> 'done')::boolean, false) then
    if now() < (r.state ->> 'done_at')::timestamptz + reveal then return jsonb_build_object('ok', true, 'changed', false); end if;
  elsif now() < r.deadline + reveal then return jsonb_build_object('ok', true, 'changed', false);
  end if;
  perform studyverse._live_next_round(c);
  return jsonb_build_object('ok', true, 'changed', true);
end $$;

do $$ declare f text; begin
  foreach f in array array['create_room(text, text, int, int, text, text, text, text)', 'update_room(text, text, text, int, int, text)', 'advance(text, int)',
    'puzzle_set(text, text, jsonb, jsonb)', 'puzzle_start(text)', 'puzzle_progress(text, int, int)', 'puzzle_solved(text, jsonb, int, int)', 'puzzle_advance(text)'] loop
    execute format('revoke all on function studyverse.%s from public, anon', f);
    execute format('grant execute on function studyverse.%s to authenticated', f);
  end loop;
end $$;

-- Edge Function only (service role): never callable by players
revoke all on function studyverse.puzzle_prepare(text, uuid), studyverse.puzzle_set_key(text, uuid, text, jsonb) from public, anon, authenticated;
grant execute on function studyverse.puzzle_prepare(text, uuid), studyverse.puzzle_set_key(text, uuid, text, jsonb) to service_role;

notify pgrst, 'reload schema';
