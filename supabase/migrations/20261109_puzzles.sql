-- StudyVerse Puzzles: LIVE "Crossword Race" for Game Rooms (NOT APPLIED — review first).
-- Same crossword for every player in the room; each word is checked on the server; the fastest player to solve the
-- whole grid wins (ranking = score desc, then total_ms asc, through the existing studyverse._live_finish()).
--
-- Additive only: it does not replace any function from 20261109_live_games.sql. A room is created as usual
-- (create_room, any game), then the host calls xword_start() from the lobby, which switches the room to game 'xword'.
--   xword_start(p_code, p_puzzle, p_answers, p_minutes)  host only, lobby, everyone ready, ≥ 2 players
--       p_puzzle  = public part made by js/puzzles-core.js chapterCrossword(): { w, h, grid: ["#..#", …] (letters
--                   replaced by '.'), entries: [{ n, dir: 'A'|'D', r, c, len, clue, enum }] }  (no answers)
--       p_answers = ["WORD", …] in the same order as entries (kept in room_keys, never readable by clients)
--   xword_submit(p_code, p_entry, p_answer)  → { ok, correct, solved: n, total, done }   one word at a time
--   xword_advance(p_code)                    finishes the race after the deadline or when everyone has solved it
-- Players read the puzzle through the existing room_state(p_q => true) (questions -> their course) and their
-- progress through room_players (score, correct, answered, total_ms).
-- Points: 10 per letter of each solved word; total_ms = time from the start to the last word (only when every
-- word is solved), so among complete grids the fastest wins. Wrong tries are counted (answered) but not punished.
-- Known limit: the host's phone builds the puzzle, so the host could read the answers from memory. For fair
-- competitive play move puzzle generation to an Edge Function (same js/puzzles-core.js code runs in Deno).

alter table studyverse.game_rooms drop constraint if exists game_rooms_game_check;
alter table studyverse.game_rooms add constraint game_rooms_game_check check (game in ('snakes', 'quiz', 'relay', 'buzzer', 'duel', 'xword'));

create or replace function studyverse.xword_start(p_code text, p_puzzle jsonb, p_answers jsonb, p_minutes int default 8)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; act int; notready text;
  n int; i int; e jsonb; a text; pub jsonb := '{}'::jsonb; crs text; mins int := greatest(3, least(20, coalesce(p_minutes, 8)));
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> uid then return studyverse._live_err('Only the host can start the game.'); end if;
  if r.status <> 'lobby' then return studyverse._live_err('The game has already started.'); end if;
  select count(*) into act from studyverse.room_players where code = c and left_at is null;
  if act < 2 then return studyverse._live_err('You need at least 2 players.'); end if;
  select string_agg(name, ', ' order by seat) into notready from studyverse.room_players where code = c and left_at is null and not ready and user_id <> r.host_id;
  if notready is not null then return studyverse._live_err('Waiting for ' || notready || ' to be ready.', 'not_ready'); end if;
  -- validate the puzzle: 8–15 entries, answers A–Z 3–12 matching each entry's length, nothing longer than the grid
  if p_puzzle is null or jsonb_typeof(p_puzzle -> 'entries') <> 'array' or jsonb_typeof(p_answers) <> 'array' or length(p_puzzle::text) > 60000 then
    return studyverse._live_err('The crossword is missing.'); end if;
  n := jsonb_array_length(p_puzzle -> 'entries');
  if n not between 8 and 15 or jsonb_array_length(p_answers) <> n then return studyverse._live_err('The crossword needs 8–15 words.'); end if;
  if (p_puzzle ->> 'w')::int not between 3 and 15 or (p_puzzle ->> 'h')::int not between 3 and 15 then return studyverse._live_err('The crossword grid is too big.'); end if;
  for i in 0 .. n - 1 loop
    e := p_puzzle -> 'entries' -> i; a := p_answers ->> i;
    if a !~ '^[A-Z]{3,12}$' or length(a) <> (e ->> 'len')::int or (e ->> 'dir') not in ('A', 'D')
       or jsonb_typeof(e -> 'clue') <> 'string' or length(e ->> 'clue') not between 3 and 300 then
      return studyverse._live_err('Word ' || (i + 1) || ' of the crossword is not valid.');
    end if;
    if position(a in upper(regexp_replace(e ->> 'clue', '[^A-Za-z]', '', 'g'))) > 0 then
      return studyverse._live_err('A clue gives its own answer away.');
    end if;
  end loop;
  -- every player gets the same public puzzle under their own course (room_state returns questions -> course)
  for crs in select distinct course from studyverse.room_players where code = c and left_at is null loop
    pub := pub || jsonb_build_object(crs, jsonb_build_object('w', p_puzzle -> 'w', 'h', p_puzzle -> 'h', 'grid', p_puzzle -> 'grid',
      'entries', (select jsonb_agg(jsonb_build_object('n', x -> 'n', 'dir', x -> 'dir', 'r', x -> 'r', 'c', x -> 'c', 'len', x -> 'len',
                    'clue', left(x ->> 'clue', 300), 'enum', left(coalesce(x ->> 'enum', ''), 20))) from jsonb_array_elements(p_puzzle -> 'entries') x)));
  end loop;
  insert into studyverse.room_keys (code, keys) values (c, jsonb_build_object('xword', p_answers)) on conflict (code) do update set keys = excluded.keys;
  delete from studyverse.room_answers where code = c;
  delete from studyverse.room_players where code = c and left_at is not null;
  update studyverse.room_players set score = 0, correct = 0, answered = 0, total_ms = 0, pos = 1, qn = 0 where code = c;
  update studyverse.game_rooms set game = 'xword', status = 'playing', started_at = now() + interval '3 seconds', finished_at = null, questions = pub, qi = 0,
    rounds = least(30, greatest(3, n)), step = step + 1, turn_user = null, deadline = now() + interval '3 seconds' + make_interval(mins => mins),
    state = jsonb_build_object('xword', true, 'words', n, 'round_at', now() + interval '3 seconds', 'solved', '[]'::jsonb)
  where code = c;
  return jsonb_build_object('ok', true, 'words', n, 'minutes', mins);
end $$;

create or replace function studyverse.xword_submit(p_code text, p_entry int, p_answer text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; me studyverse.room_players;
  key text; ans text := upper(regexp_replace(coalesce(p_answer, ''), '[^A-Za-z]', '', 'g')); ok boolean; n int; got int; ms int; pts int; everyone boolean;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.game <> 'xword' then return studyverse._live_err('No crossword race here.'); end if;
  if r.status <> 'playing' then return studyverse._live_err('The race is over.', 'over'); end if;
  if now() < (r.state ->> 'round_at')::timestamptz then return studyverse._live_err('Wait for the start!', 'early'); end if;
  if now() > r.deadline then perform studyverse.xword_advance(c); return studyverse._live_err('Time is up.', 'over'); end if;
  select * into me from studyverse.room_players where code = c and user_id = uid and left_at is null;
  if not found then return studyverse._live_err('You are not in this race.', 'not_member'); end if;
  n := (r.state ->> 'words')::int;
  if p_entry is null or p_entry < 0 or p_entry >= n then return studyverse._live_err('Unknown word.'); end if;
  if me.answered >= 400 then return studyverse._live_err('Too many tries.'); end if;
  if exists (select 1 from studyverse.room_answers where code = c and qi = p_entry and user_id = uid and correct) then
    return jsonb_build_object('ok', true, 'correct', true, 'already', true);
  end if;
  select keys -> 'xword' ->> p_entry into key from studyverse.room_keys where code = c;
  ok := key is not null and ans = key;
  ms := (extract(epoch from (now() - (r.state ->> 'round_at')::timestamptz)) * 1000)::int;
  update studyverse.room_players set answered = answered + 1 where code = c and user_id = uid;
  if not ok then return jsonb_build_object('ok', true, 'correct', false); end if;
  pts := 10 * length(key);
  insert into studyverse.room_answers (code, qi, user_id, choice, correct, ms, points) values (c, p_entry, uid, 0, true, ms, pts)
    on conflict (code, qi, user_id) do update set correct = true, ms = excluded.ms, points = excluded.points;
  select count(*) into got from studyverse.room_answers where code = c and user_id = uid and correct;
  update studyverse.room_players set score = score + pts, correct = got, total_ms = case when got >= n then ms else 0 end where code = c and user_id = uid;
  if got >= n then
    update studyverse.game_rooms set step = step + 1, state = jsonb_set(state, '{solved}', coalesce(state -> 'solved', '[]'::jsonb) || to_jsonb(uid::text)) where code = c;
  else
    update studyverse.game_rooms set step = step + 1 where code = c;
  end if;
  select bool_and(p.correct >= n) into everyone from studyverse.room_players p where p.code = c and p.left_at is null;
  if coalesce(everyone, false) then perform studyverse._live_finish(c); end if;
  return jsonb_build_object('ok', true, 'correct', true, 'solved', got, 'total', n, 'done', got >= n, 'points', pts);
end $$;

-- any member may call this; it only acts when the race is really over (deadline passed, or everyone solved the grid)
create or replace function studyverse.xword_advance(p_code text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; n int; everyone boolean;
begin
  if not studyverse.is_room_member(c) and auth.uid() is not null then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  select * into r from studyverse.game_rooms where code = c;
  if not found or r.game <> 'xword' or r.status <> 'playing' then return jsonb_build_object('ok', true, 'changed', false); end if;
  n := (r.state ->> 'words')::int;
  select bool_and(correct >= n) into everyone from studyverse.room_players where code = c and left_at is null;
  if now() > r.deadline or coalesce(everyone, false) then perform studyverse._live_finish(c); return jsonb_build_object('ok', true, 'changed', true); end if;
  return jsonb_build_object('ok', true, 'changed', false);
end $$;

revoke all on function studyverse.xword_start(text, jsonb, jsonb, int), studyverse.xword_submit(text, int, text), studyverse.xword_advance(text) from public, anon;
grant execute on function studyverse.xword_start(text, jsonb, jsonb, int), studyverse.xword_submit(text, int, text), studyverse.xword_advance(text) to authenticated;
