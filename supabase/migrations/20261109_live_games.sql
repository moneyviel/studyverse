-- ============================================================================================
-- StudyVerse LIVE "Game Rooms" (multiplayer): rooms, players, answers, results + SECURITY DEFINER RPCs.
-- Schema: studyverse (exposed in the Data API). Live events (moves, buzz, emoji) travel over Supabase
-- Realtime broadcast on topic "room-<CODE>" (public channel); THIS database is the source of truth for
-- turns, deadlines and scores. Clients never write tables directly: RLS allows members to READ their
-- room and its players; every change goes through the functions below.
--
-- Games:  snakes (Snakes & Ladders Battle, turn-based, server rolls the die)
--         quiz   (Quiz Race: everyone answers their own course's question i at the same time)
--         relay  (Team Relay: one runner per team per round, teams only)
--         buzzer (first to buzz answers; a wrong answer re-opens the buzzer for the others)
--         duel   (CA / professional Speed Duel: 10 MCQs, 72 s each)
-- Modes:  duel (exactly 2 players), ffa (2–6), teams (2 teams, 2–6 players, team score = sum)
--
-- Answer keys: the host's app picks questions per course and sends them to start_game; the keys are
-- split off into studyverse.room_keys (no policies = unreadable) and the server checks every answer.
-- Rooms expire 2 hours after creation (or after the last rematch); live_cleanup() deletes them.
-- Snakes board: KEEP IN SYNC with LADDERS / SNAKES in js/arcade.js (studyverse._live_board below).
-- Apply once in the SQL editor (idempotent: safe to run again).
-- ============================================================================================

create table if not exists studyverse.game_rooms (
  code        text primary key check (code ~ '^[A-Z]{6}$'),
  host_id     uuid not null references auth.users(id) on delete cascade,
  game        text not null default 'quiz' check (game in ('snakes', 'quiz', 'relay', 'buzzer', 'duel')),
  mode        text not null default 'ffa' check (mode in ('duel', 'ffa', 'teams')),
  rounds      int  not null default 10 check (rounds between 3 and 30),
  turn_secs   int  not null default 20 check (turn_secs in (10, 20, 30, 72)),
  level       text not null default 'mixed' check (level in ('mixed', 'easy', 'moderate', 'hard')),   -- question level chosen by the host
  status      text not null default 'lobby' check (status in ('lobby', 'playing', 'finished')),
  step        int  not null default 0,          -- bumps on every change; actions carry the step they saw
  qi          int  not null default 0,          -- question / round index (quiz, relay, buzzer, duel)
  turn_user   uuid,                             -- snakes: whose turn; buzzer: who buzzed
  deadline    timestamptz,
  state       jsonb not null default '{}'::jsonb,
  questions   jsonb,                            -- public: { course: [ {q, o:[…], s} ] } (no answers)
  banned      uuid[] not null default '{}',
  created_at  timestamptz not null default now(),
  started_at  timestamptz,
  finished_at timestamptz,
  expires_at  timestamptz not null default now() + interval '2 hours'
);
create index if not exists game_rooms_host_idx on studyverse.game_rooms (host_id, created_at);
create index if not exists game_rooms_exp_idx on studyverse.game_rooms (expires_at);

alter table studyverse.game_rooms add column if not exists level text not null default 'mixed' check (level in ('mixed', 'easy', 'moderate', 'hard'));

create table if not exists studyverse.room_keys (
  code text primary key references studyverse.game_rooms(code) on delete cascade,
  keys jsonb not null                              -- { course: [ {a: int, x: text} ] }
);

create table if not exists studyverse.room_players (
  code      text not null references studyverse.game_rooms(code) on delete cascade,
  user_id   uuid not null references auth.users(id) on delete cascade,
  name      text not null,                         -- first name only
  avatar    text not null default '🙂',
  course    text not null check (course ~ '^[a-z0-9-]{2,40}$'),
  team      smallint check (team in (0, 1)),
  seat      int  not null,
  ready     boolean not null default false,
  score     int  not null default 0,
  correct   int  not null default 0,
  answered  int  not null default 0,
  total_ms  bigint not null default 0,
  pos       int  not null default 1,               -- snakes square
  qn        int  not null default 0,               -- snakes: next question index for this player
  left_at   timestamptz,
  joined_at timestamptz not null default now(),
  last_seen timestamptz not null default now(),
  primary key (code, user_id)
);
create index if not exists room_players_user_idx on studyverse.room_players (user_id);

create table if not exists studyverse.room_answers (
  code    text not null references studyverse.game_rooms(code) on delete cascade,
  qi      int  not null,
  user_id uuid not null,
  choice  int  not null,
  correct boolean not null,
  ms      int  not null,
  points  int  not null,
  at      timestamptz not null default now(),
  primary key (code, qi, user_id)
);

create table if not exists studyverse.game_results (
  id          bigserial primary key,
  code        text not null,
  user_id     uuid not null references auth.users(id) on delete cascade,
  name        text not null,
  avatar      text not null,
  game        text not null,
  mode        text not null,
  team        smallint,
  score       int  not null,
  correct     int  not null default 0,
  rank        int  not null,
  won         boolean not null,
  finished_at timestamptz not null default now()
);
create index if not exists game_results_user_idx on studyverse.game_results (user_id, finished_at);
create index if not exists game_results_code_idx on studyverse.game_results (code);

-- ---------- RLS: members read their room; nobody writes directly ----------
alter table studyverse.game_rooms   enable row level security;
alter table studyverse.room_keys    enable row level security;   -- no policies: answer keys are never readable
alter table studyverse.room_players enable row level security;
alter table studyverse.room_answers enable row level security;   -- no policies: read through room_state()
alter table studyverse.game_results enable row level security;

create or replace function studyverse.is_room_member(p_code text) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.room_players where code = p_code and user_id = auth.uid());
$$;
revoke all on function studyverse.is_room_member(text) from public, anon;
grant execute on function studyverse.is_room_member(text) to authenticated;

drop policy if exists game_rooms_read on studyverse.game_rooms;
create policy game_rooms_read on studyverse.game_rooms for select to authenticated using ((select studyverse.is_room_member(code)));
drop policy if exists room_players_read on studyverse.room_players;
create policy room_players_read on studyverse.room_players for select to authenticated using ((select studyverse.is_room_member(code)));
drop policy if exists game_results_read on studyverse.game_results;
create policy game_results_read on studyverse.game_results for select to authenticated using (user_id = (select auth.uid()));

revoke all on studyverse.game_rooms, studyverse.room_keys, studyverse.room_players, studyverse.room_answers, studyverse.game_results from anon, authenticated;
grant select on studyverse.game_rooms, studyverse.room_players, studyverse.game_results to authenticated;
grant all on studyverse.game_rooms, studyverse.room_keys, studyverse.room_players, studyverse.room_answers, studyverse.game_results to service_role;
grant usage, select on sequence studyverse.game_results_id_seq to service_role;

-- ============================================================================================
-- internal helpers (not callable by clients)
-- ============================================================================================

-- ladders go up, snakes go down. KEEP IN SYNC with js/arcade.js (LADDERS, SNAKES)
create or replace function studyverse._live_board() returns jsonb language sql immutable set search_path = '' as $$
  select '{"2":23,"4":14,"8":30,"11":32,"15":44,"20":41,"25":46,"28":76,"36":57,"40":59,"42":60,"50":69,"52":72,"58":78,"63":82,"68":88,"71":92,"75":86,"79":94,"81":97,
           "17":7,"19":5,"33":12,"38":18,"47":26,"49":31,"55":35,"62":43,"66":45,"73":53,"77":60,"84":64,"87":24,"89":67,"91":70,"93":74,"95":56,"96":85,"98":80,"99":61}'::jsonb;
$$;

-- who may play: owner/admin always; parents never; students with any live course access (paid, code or the 24-hour trial)
create or replace function studyverse._live_why(p_uid uuid) returns text
language plpgsql stable security definer set search_path = '' as $$
begin
  if p_uid is null then return 'signin'; end if;
  if p_uid = auth.uid() and studyverse.is_admin() then return 'ok'; end if;            -- owner / admin (testing)
  if (select role from studyverse.profiles where user_id = p_uid) = 'parent' then return 'parent'; end if;
  if exists (select 1 from studyverse.course_access where user_id = p_uid and (valid_until is null or valid_until > now())) then return 'ok'; end if;
  return 'free';
end $$;

create or replace function studyverse._live_msg(p_why text) returns text language sql immutable set search_path = '' as $$
  select case p_why when 'signin' then 'Please sign in first.'
                    when 'parent' then 'Game Rooms are for students.'
                    when 'free' then 'Game Rooms are part of StudyVerse plans.'
                    else 'Not allowed.' end;
$$;

create or replace function studyverse._live_first(p_name text) returns text language sql immutable set search_path = '' as $$
  select coalesce(nullif(left(split_part(regexp_replace(trim(coalesce(p_name, '')), '\s+', ' ', 'g'), ' ', 1), 20), ''), 'Player');
$$;

create or replace function studyverse._live_err(p_msg text, p_code text default null) returns jsonb language sql immutable set search_path = '' as $$
  select jsonb_build_object('ok', false, 'msg', p_msg) || case when p_code is null then '{}'::jsonb else jsonb_build_object('code', p_code) end;
$$;

-- relay: the runner of each team for round p_qi (members by seat, taking turns)
create or replace function studyverse._live_runners(p_code text, p_qi int) returns jsonb
language sql stable security definer set search_path = '' as $$
  select coalesce(jsonb_agg(user_id order by team), '[]'::jsonb) from (
    select distinct on (team) team, user_id from (
      select team, user_id, row_number() over (partition by team order by seat) - 1 as i, count(*) over (partition by team) as n
      from studyverse.room_players where code = p_code and left_at is null and team is not null) s
    where i = p_qi % n order by team) t;
$$;

create or replace function studyverse._live_finish(p_code text) returns void
language plpgsql security definer set search_path = '' as $$
declare r studyverse.game_rooms; t0 int := 0; t1 int := 0; wt int;
begin
  select * into r from studyverse.game_rooms where code = p_code for update;
  if not found or r.status = 'finished' then return; end if;
  if r.mode = 'teams' then
    select coalesce(sum(score) filter (where team = 0), 0), coalesce(sum(score) filter (where team = 1), 0) into t0, t1
      from studyverse.room_players where code = p_code;
    wt := case when t0 > t1 then 0 when t1 > t0 then 1 else null end;
  end if;
  insert into studyverse.game_results (code, user_id, name, avatar, game, mode, team, score, correct, rank, won)
  select p_code, user_id, name, avatar, r.game, r.mode, team, score, correct, rk,
         left_at is null and case when r.mode = 'teams' then wt is not null and team = wt else rk = 1 end
  from (select *, rank() over (order by score desc, correct desc, total_ms asc) as rk from studyverse.room_players where code = p_code) s;
  update studyverse.game_rooms set status = 'finished', finished_at = now(), deadline = null, turn_user = null, step = step + 1,
    state = (state - 'gate') || jsonb_build_object('teams', jsonb_build_array(t0, t1), 'win_team', wt)
  where code = p_code;
end $$;

-- snakes: pass the turn to the next active player (finish after the last round)
create or replace function studyverse._live_next_turn(p_code text) returns void
language plpgsql security definer set search_path = '' as $$
declare r studyverse.game_rooms; ord jsonb; n int; ti int; rnd int; i int; cand uuid := null;
begin
  select * into r from studyverse.game_rooms where code = p_code for update;
  if r.status <> 'playing' then return; end if;
  ord := r.state -> 'order'; n := jsonb_array_length(ord); ti := (r.state ->> 'ti')::int; rnd := (r.state ->> 'round')::int;
  for i in 1..n loop
    ti := ti + 1;
    if ti >= n then ti := 0; rnd := rnd + 1; end if;
    if exists (select 1 from studyverse.room_players where code = p_code and user_id = (ord ->> ti)::uuid and left_at is null) then
      cand := (ord ->> ti)::uuid; exit;
    end if;
  end loop;
  -- Snakes & Ladders ends only when someone reaches 100 (or fewer than 2 players are left), never on a round count
  if cand is null or (select count(*) from studyverse.room_players where code = p_code and left_at is null) < 2 then perform studyverse._live_finish(p_code); return; end if;
  update studyverse.game_rooms set turn_user = cand, deadline = now() + make_interval(secs => r.turn_secs + 2), step = step + 1,
    state = (state - 'gate') || jsonb_build_object('ti', ti, 'round', rnd)
  where code = p_code;
end $$;

-- quiz / relay / buzzer / duel: next question for everyone (finish after the last one)
create or replace function studyverse._live_next_round(p_code text) returns void
language plpgsql security definer set search_path = '' as $$
declare r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = p_code for update;
  if r.status <> 'playing' then return; end if;
  if r.qi + 1 >= r.rounds then perform studyverse._live_finish(p_code); return; end if;
  update studyverse.game_rooms set qi = qi + 1, step = step + 1, turn_user = null, deadline = now() + make_interval(secs => r.turn_secs),
    state = jsonb_build_object('round_at', now(), 'done', false, 'out', '[]'::jsonb)
            || case when r.game = 'relay' then jsonb_build_object('runners', studyverse._live_runners(p_code, r.qi + 1)) else '{}'::jsonb end
  where code = p_code;
end $$;

-- quiz / duel / relay: has everyone who should answer this round answered?
create or replace function studyverse._live_complete(p_code text) returns boolean
language plpgsql stable security definer set search_path = '' as $$
declare r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = p_code;
  if r.game = 'relay' then
    return not exists (select 1 from jsonb_array_elements_text(coalesce(r.state -> 'runners', '[]'::jsonb)) u
      where exists (select 1 from studyverse.room_players p where p.code = p_code and p.user_id = u::uuid and p.left_at is null)
        and not exists (select 1 from studyverse.room_answers a where a.code = p_code and a.qi = r.qi and a.user_id = u::uuid));
  end if;
  return not exists (select 1 from studyverse.room_players p where p.code = p_code and p.left_at is null
    and not exists (select 1 from studyverse.room_answers a where a.code = p_code and a.qi = r.qi and a.user_id = p.user_id));
end $$;

-- snakes: settle a ladder / snake question (right: climb or escape; wrong or too late: stay or slide)
create or replace function studyverse._live_gate(p_code text, p_ok boolean, p_timeout boolean) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r studyverse.game_rooms; g jsonb; uid uuid; np int; at_ int; to_ int;
begin
  select * into r from studyverse.game_rooms where code = p_code for update;
  g := r.state -> 'gate'; uid := (g ->> 'user')::uuid; at_ := (g ->> 'at')::int; to_ := (g ->> 'to')::int;
  np := case when g ->> 'kind' = 'lad' then case when p_ok then to_ else at_ end else case when p_ok then at_ else to_ end end;
  update studyverse.room_players set pos = np, score = np, answered = answered + 1, correct = correct + case when p_ok then 1 else 0 end, qn = qn + 1
    where code = p_code and user_id = uid;
  update studyverse.game_rooms set state = (state - 'gate') || jsonb_build_object('last',
      jsonb_build_object('user', uid, 'kind', g ->> 'kind', 'ok', p_ok, 'timeout', p_timeout, 'from', at_, 'to', np, 'roll', (state -> 'last' ->> 'roll')::int))
    where code = p_code;
  if np >= 100 then perform studyverse._live_finish(p_code); else perform studyverse._live_next_turn(p_code); end if;
  return jsonb_build_object('pos', np);
end $$;

revoke all on function studyverse._live_board(), studyverse._live_why(uuid), studyverse._live_msg(text), studyverse._live_first(text), studyverse._live_err(text, text),
  studyverse._live_runners(text, int), studyverse._live_finish(text), studyverse._live_next_turn(text), studyverse._live_next_round(text),
  studyverse._live_complete(text), studyverse._live_gate(text, boolean, boolean) from public, anon, authenticated;

-- ============================================================================================
-- client RPCs
-- ============================================================================================

create or replace function studyverse.live_cleanup() returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  delete from studyverse.game_rooms where expires_at < now();
  get diagnostics n = row_count;
  delete from studyverse.game_results where finished_at < now() - interval '60 days';
  return n;
end $$;
revoke all on function studyverse.live_cleanup() from public, anon, authenticated;
grant execute on function studyverse.live_cleanup() to service_role;

create or replace function studyverse.live_eligibility() returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare w text := studyverse._live_why(auth.uid());
begin
  return jsonb_build_object('ok', w = 'ok', 'reason', w, 'admin', coalesce(studyverse.is_admin(), false));
end $$;

create or replace function studyverse.create_room(p_game text, p_mode text, p_rounds int, p_turn_secs int, p_name text, p_avatar text, p_course text, p_level text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); w text := studyverse._live_why(auth.uid()); k text; alph text := 'ABCDEFGHJKLMNPQRSTUVWXYZ'; i int; g text; m text; rd int; ts int;
begin
  if w <> 'ok' then return studyverse._live_err(studyverse._live_msg(w), w); end if;
  if coalesce(p_course, '') !~ '^[a-z0-9-]{2,40}$' then return studyverse._live_err('Unknown course.'); end if;
  g := coalesce(p_game, 'quiz'); m := coalesce(p_mode, 'ffa'); rd := coalesce(p_rounds, 10); ts := coalesce(p_turn_secs, 20);
  if g not in ('snakes', 'quiz', 'relay', 'buzzer', 'duel') or m not in ('duel', 'ffa', 'teams') then return studyverse._live_err('Unknown game or mode.'); end if;
  if g = 'relay' then m := 'teams'; end if;
  if g = 'duel' then rd := 10; ts := 72; else rd := greatest(3, least(30, rd)); if ts not in (10, 20, 30) then ts := 20; end if; end if;
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

create or replace function studyverse.join_room(p_code text, p_name text, p_avatar text, p_course text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); w text := studyverse._live_why(auth.uid()); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; n int; t0 int; t1 int;
begin
  if w <> 'ok' then return studyverse._live_err(studyverse._live_msg(w), w); end if;
  if coalesce(p_course, '') !~ '^[a-z0-9-]{2,40}$' then return studyverse._live_err('Unknown course.'); end if;
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.expires_at < now() then return studyverse._live_err('Room not found. Check the code and try again.', 'not_found'); end if;
  if uid = any (r.banned) then return studyverse._live_err('The host removed you from this room.', 'banned'); end if;
  if exists (select 1 from studyverse.room_players where code = c and user_id = uid) then      -- rejoin (link, reload, reconnect)
    update studyverse.room_players set left_at = null, last_seen = now(), name = studyverse._live_first(p_name),
      avatar = coalesce(nullif(left(trim(coalesce(p_avatar, '')), 8), ''), avatar) where code = c and user_id = uid;
    update studyverse.game_rooms set step = step + 1 where code = c;
    return jsonb_build_object('ok', true, 'code', c, 'rejoin', true);
  end if;
  if r.status <> 'lobby' then return studyverse._live_err('This game has already started. Ask for a new room code.', 'started'); end if;
  select count(*), count(*) filter (where team = 0), count(*) filter (where team = 1) into n, t0, t1 from studyverse.room_players where code = c;
  if n >= (case when r.mode = 'duel' then 2 else 6 end) then return studyverse._live_err('This room is full.', 'full'); end if;
  insert into studyverse.room_players (code, user_id, name, avatar, course, team, seat)
    values (c, uid, studyverse._live_first(p_name), coalesce(nullif(left(trim(coalesce(p_avatar, '')), 8), ''), '🙂'), p_course,
            case when r.mode = 'teams' then case when t1 < t0 then 1 else 0 end end,
            coalesce((select max(seat) from studyverse.room_players where code = c), 0) + 1);
  update studyverse.game_rooms set step = step + 1 where code = c;
  return jsonb_build_object('ok', true, 'code', c);
end $$;

create or replace function studyverse.leave_room(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; nh uuid; act int;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or not exists (select 1 from studyverse.room_players where code = c and user_id = uid) then return jsonb_build_object('ok', true); end if;
  if r.status = 'playing' then update studyverse.room_players set left_at = now() where code = c and user_id = uid;
  else delete from studyverse.room_players where code = c and user_id = uid; end if;
  select count(*) into act from studyverse.room_players where code = c and left_at is null;
  if act = 0 then
    if r.status = 'playing' then perform studyverse._live_finish(c); else delete from studyverse.game_rooms where code = c; end if;
    return jsonb_build_object('ok', true);
  end if;
  if r.host_id = uid then
    select user_id into nh from studyverse.room_players where code = c and left_at is null order by (last_seen > now() - interval '60 seconds') desc, seat limit 1;
    update studyverse.game_rooms set host_id = nh where code = c;
  end if;
  update studyverse.game_rooms set step = step + 1 where code = c;
  if r.status = 'playing' then
    if act < 2 then perform studyverse._live_finish(c);
    elsif r.game = 'snakes' and r.turn_user = uid then perform studyverse._live_next_turn(c);
    end if;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.kick_player(p_code text, p_user uuid) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; act int;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> uid then return studyverse._live_err('Only the host can remove players.'); end if;
  if p_user = uid then return studyverse._live_err('Use Leave room to leave.'); end if;
  if not exists (select 1 from studyverse.room_players where code = c and user_id = p_user) then return jsonb_build_object('ok', true); end if;
  update studyverse.game_rooms set banned = array_append(banned, p_user), step = step + 1 where code = c;
  if r.status = 'playing' then update studyverse.room_players set left_at = now() where code = c and user_id = p_user;
  else delete from studyverse.room_players where code = c and user_id = p_user; end if;
  if r.status = 'playing' then
    select count(*) into act from studyverse.room_players where code = c and left_at is null;
    if act < 2 then perform studyverse._live_finish(c);
    elsif r.game = 'snakes' and r.turn_user = p_user then perform studyverse._live_next_turn(c); end if;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.update_room(p_code text, p_game text, p_mode text, p_rounds int, p_turn_secs int, p_level text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; g text; m text; rd int; ts int; n int; pl record; t0 int := 0; t1 int := 0;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> uid then return studyverse._live_err('Only the host can change the game.'); end if;
  if r.status <> 'lobby' then return studyverse._live_err('The game has already started.'); end if;
  g := coalesce(p_game, r.game); m := coalesce(p_mode, r.mode); rd := coalesce(p_rounds, r.rounds); ts := coalesce(p_turn_secs, r.turn_secs);
  if g not in ('snakes', 'quiz', 'relay', 'buzzer', 'duel') or m not in ('duel', 'ffa', 'teams') then return studyverse._live_err('Unknown game or mode.'); end if;
  if g = 'relay' then m := 'teams'; end if;
  if g = 'duel' then rd := 10; ts := 72; else rd := greatest(3, least(30, rd)); if ts not in (10, 20, 30) then ts := 20; end if; end if;
  select count(*) into n from studyverse.room_players where code = c;
  if m = 'duel' and n > 2 then return studyverse._live_err('1-v-1 needs exactly 2 players. Remove players first.'); end if;
  if m = 'teams' and r.mode <> 'teams' then
    for pl in select user_id from studyverse.room_players where code = c order by seat loop
      update studyverse.room_players set team = case when t1 < t0 then 1 else 0 end where code = c and user_id = pl.user_id;
      if t1 < t0 then t1 := t1 + 1; else t0 := t0 + 1; end if;
    end loop;
  elsif m <> 'teams' then update studyverse.room_players set team = null where code = c;
  end if;
  update studyverse.game_rooms set game = g, mode = m, rounds = rd, turn_secs = ts, step = step + 1,
    level = case when p_level in ('mixed', 'easy', 'moderate', 'hard') then p_level else level end where code = c;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.set_ready(p_code text, p_ready boolean) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, '')));
begin
  update studyverse.room_players p set ready = coalesce(p_ready, false), last_seen = now()
    from studyverse.game_rooms r where r.code = p.code and p.code = c and p.user_id = auth.uid() and r.status = 'lobby';
  if not found then return studyverse._live_err('You are not in this room.'); end if;
  update studyverse.game_rooms set step = step + 1 where code = c;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.set_team(p_code text, p_team int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, '')));
begin
  if p_team not in (0, 1) then return studyverse._live_err('Unknown team.'); end if;
  update studyverse.room_players p set team = p_team
    from studyverse.game_rooms r where r.code = p.code and p.code = c and p.user_id = auth.uid() and r.status = 'lobby' and r.mode = 'teams';
  if not found then return studyverse._live_err('Teams can be changed in the lobby of a team game.'); end if;
  update studyverse.game_rooms set step = step + 1 where code = c;
  return jsonb_build_object('ok', true);
end $$;

-- host starts: p_questions = { course: [ {q, o:[2–4 options], a: right option index, s?: source label, x?: explanation} ] }
create or replace function studyverse.start_game(p_code text, p_questions jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; need int; crs text; lst jsonb; it jsonb;
  missing text[] := '{}'; notready text; pub jsonb := '{}'::jsonb; ks jsonb := '{}'::jsonb; pa jsonb; ka jsonb; act int; t0 int; t1 int; ord jsonb; first uuid;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> uid then return studyverse._live_err('Only the host can start the game.'); end if;
  if r.status <> 'lobby' then return studyverse._live_err('The game has already started.'); end if;
  select count(*), count(*) filter (where team = 0), count(*) filter (where team = 1) into act, t0, t1 from studyverse.room_players where code = c and left_at is null;
  if act < 2 then return studyverse._live_err('You need at least 2 players.'); end if;
  if r.mode = 'duel' and act <> 2 then return studyverse._live_err('1-v-1 needs exactly 2 players.'); end if;
  if r.mode = 'teams' and (t0 = 0 or t1 = 0) then return studyverse._live_err('Both teams need at least one player.'); end if;
  select string_agg(name, ', ' order by seat) into notready from studyverse.room_players where code = c and left_at is null and not ready and user_id <> r.host_id;
  if notready is not null then return studyverse._live_err('Waiting for ' || notready || ' to be ready.', 'not_ready'); end if;
  if p_questions is null or jsonb_typeof(p_questions) <> 'object' or length(p_questions::text) > 800000 then return studyverse._live_err('Questions are missing.'); end if;
  need := case when r.game = 'snakes' then 5 else r.rounds end;
  for crs in select distinct course from studyverse.room_players where code = c and left_at is null loop
    lst := p_questions -> crs; pa := '[]'::jsonb; ka := '[]'::jsonb;
    if lst is not null and jsonb_typeof(lst) = 'array' then
      for it in select value from jsonb_array_elements(lst) limit 60 loop
        if jsonb_typeof(it -> 'q') = 'string' and length(it ->> 'q') between 1 and 1500 and jsonb_typeof(it -> 'o') = 'array'
           and jsonb_array_length(it -> 'o') between 2 and 4
           and not exists (select 1 from jsonb_array_elements(it -> 'o') o where jsonb_typeof(o) <> 'string' or length(o #>> '{}') not between 1 and 500)
           and jsonb_typeof(it -> 'a') = 'number' and (it ->> 'a') ~ '^\d+$' and (it ->> 'a')::int < jsonb_array_length(it -> 'o') then
          pa := pa || jsonb_build_array(jsonb_build_object('q', it -> 'q', 'o', it -> 'o', 's', left(coalesce(it ->> 's', ''), 120)));
          ka := ka || jsonb_build_array(jsonb_build_object('a', (it ->> 'a')::int, 'x', left(coalesce(it ->> 'x', ''), 600)));
        end if;
      end loop;
    end if;
    if jsonb_array_length(pa) < need then missing := array_append(missing, crs);
    else pub := pub || jsonb_build_object(crs, pa); ks := ks || jsonb_build_object(crs, ka); end if;
  end loop;
  if cardinality(missing) > 0 then
    return studyverse._live_err('Not enough questions for: ' || array_to_string(missing, ', '), 'need_questions') || jsonb_build_object('need', to_jsonb(missing), 'count', need);
  end if;
  insert into studyverse.room_keys (code, keys) values (c, ks) on conflict (code) do update set keys = excluded.keys;
  delete from studyverse.room_answers where code = c;
  delete from studyverse.room_players where code = c and left_at is not null;
  update studyverse.room_players set score = 0, correct = 0, answered = 0, total_ms = 0, pos = 1, qn = 0 where code = c;
  if r.game = 'snakes' then
    select jsonb_agg(user_id order by rn, team nulls first, seat) into ord from (
      select user_id, team, seat, row_number() over (partition by team order by seat) as rn from studyverse.room_players where code = c and left_at is null) s;
    first := (ord ->> 0)::uuid;
    update studyverse.game_rooms set status = 'playing', started_at = now(), finished_at = null, questions = pub, qi = 0, step = step + 1,
      turn_user = first, deadline = now() + make_interval(secs => r.turn_secs + 3),
      state = jsonb_build_object('order', ord, 'ti', 0, 'round', 1, 'round_at', now() + interval '3 seconds')
    where code = c;
  else
    update studyverse.game_rooms set status = 'playing', started_at = now(), finished_at = null, questions = pub, qi = 0, step = step + 1, turn_user = null,
      deadline = now() + make_interval(secs => r.turn_secs + 3),
      state = jsonb_build_object('round_at', now() + interval '3 seconds', 'done', false, 'out', '[]'::jsonb)
              || case when r.game = 'relay' then jsonb_build_object('runners', studyverse._live_runners(c, 0)) else '{}'::jsonb end
    where code = c;
  end if;
  return jsonb_build_object('ok', true);
end $$;

-- snakes: roll the die (the server rolls). Exact roll needed to land on 100: a roll past 100 = stay.
create or replace function studyverse.submit_move(p_code text, p_step int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; me studyverse.room_players; roll int; np int; dest int; tr text; nk int;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  select * into me from studyverse.room_players where code = c and user_id = uid and left_at is null;
  if not found then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  update studyverse.room_players set last_seen = now() where code = c and user_id = uid;
  if r.status <> 'playing' or r.game <> 'snakes' then return studyverse._live_err('No game is running.', 'not_playing'); end if;
  if p_step is distinct from r.step then return studyverse._live_err('That move is out of date.', 'stale'); end if;
  if r.turn_user is distinct from uid then return studyverse._live_err('It is not your turn.', 'not_your_turn'); end if;
  if r.state -> 'gate' is not null then return studyverse._live_err('Answer the question first.', 'gate'); end if;
  if now() > r.deadline + interval '1.5 seconds' then return studyverse._live_err('Too late — your turn is over.', 'late'); end if;
  tr := current_setting('studyverse.test_roll', true);      -- SQL tests only (PostgREST cannot set this)
  roll := case when tr ~ '^[1-6]$' then tr::int else 1 + floor(random() * 6)::int end;
  np := me.pos + roll;
  if np > 100 then np := me.pos; end if;                    -- too big: wait for the exact number
  update studyverse.room_players set pos = np, score = np where code = c and user_id = uid;
  dest := (studyverse._live_board() ->> np::text)::int;
  select greatest(1, coalesce(jsonb_array_length(keys -> me.course), 1)) into nk from studyverse.room_keys where code = c;
  me.qn := me.qn % coalesce(nk, 1);                          -- long games: reuse the question list from the start
  if np <> me.pos and dest is not null then
    update studyverse.game_rooms set step = step + 1, deadline = now() + make_interval(secs => r.turn_secs + 2),
      state = state || jsonb_build_object('gate', jsonb_build_object('user', uid, 'kind', case when dest > np then 'lad' else 'snk' end, 'at', np, 'to', dest, 'qi', me.qn),
                                          'last', jsonb_build_object('user', uid, 'roll', roll, 'from', me.pos, 'to', np))
    where code = c;
    return jsonb_build_object('ok', true, 'roll', roll, 'from', me.pos, 'to', np, 'gate', jsonb_build_object('kind', case when dest > np then 'lad' else 'snk' end, 'to', dest, 'qi', me.qn));
  end if;
  update studyverse.game_rooms set state = state || jsonb_build_object('last', jsonb_build_object('user', uid, 'roll', roll, 'from', me.pos, 'to', np, 'over', np = me.pos))
    where code = c;
  if np >= 100 then perform studyverse._live_finish(c); else perform studyverse._live_next_turn(c); end if;
  return jsonb_build_object('ok', true, 'roll', roll, 'from', me.pos, 'to', np, 'over', np = me.pos);
end $$;

-- buzzer: first to buzz gets to answer
create or replace function studyverse.buzz(p_code text, p_step int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  if not exists (select 1 from studyverse.room_players where code = c and user_id = uid and left_at is null) then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  update studyverse.room_players set last_seen = now() where code = c and user_id = uid;
  if r.status <> 'playing' or r.game <> 'buzzer' then return studyverse._live_err('No buzzer round is running.', 'not_playing'); end if;
  if r.turn_user is not null then return studyverse._live_err('Someone buzzed first!', 'taken'); end if;
  if p_step is distinct from r.step then return studyverse._live_err('That buzz is out of date.', 'stale'); end if;
  if coalesce((r.state ->> 'done')::boolean, false) or now() > r.deadline + interval '1 second' then return studyverse._live_err('This round is over.', 'late'); end if;
  if now() < (r.state ->> 'round_at')::timestamptz then return studyverse._live_err('Wait for the question.', 'early'); end if;
  if (r.state -> 'out') ? uid::text then return studyverse._live_err('You already tried this one.', 'out'); end if;
  update studyverse.game_rooms set turn_user = uid, step = step + 1, deadline = now() + make_interval(secs => r.turn_secs),
    state = state || jsonb_build_object('buzz', uid) where code = c;
  return jsonb_build_object('ok', true, 'step', r.step + 1);
end $$;

create or replace function studyverse.submit_answer(p_code text, p_step int, p_choice int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; me studyverse.room_players; k jsonb; lst jsonb; i int;
  ok boolean; ms int; pts int := 0; act int; nout int;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  select * into me from studyverse.room_players where code = c and user_id = uid and left_at is null;
  if not found then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
  update studyverse.room_players set last_seen = now() where code = c and user_id = uid;
  if r.status <> 'playing' then return studyverse._live_err('No game is running.', 'not_playing'); end if;
  if p_step is distinct from r.step then return studyverse._live_err('That answer is out of date.', 'stale'); end if;
  if now() > r.deadline + interval '1.5 seconds' then return studyverse._live_err('Too late — time is up.', 'late'); end if;
  select keys -> me.course into lst from studyverse.room_keys where code = c;
  if lst is null then return studyverse._live_err('No questions for your course.'); end if;

  if r.game = 'snakes' then
    if r.state -> 'gate' is null or (r.state -> 'gate' ->> 'user')::uuid is distinct from uid then return studyverse._live_err('It is not your turn.', 'not_your_turn'); end if;
    i := (r.state -> 'gate' ->> 'qi')::int % jsonb_array_length(lst); k := lst -> i;
    ok := coalesce(p_choice = (k ->> 'a')::int, false);
    perform studyverse._live_gate(c, ok, false);
    return jsonb_build_object('ok', true, 'correct', ok, 'answer', (k ->> 'a')::int, 'explain', k ->> 'x', 'qi', i);
  end if;

  k := lst -> r.qi;
  if k is null then return studyverse._live_err('No question here.'); end if;
  if now() < (r.state ->> 'round_at')::timestamptz then return studyverse._live_err('Wait for the question.', 'early'); end if;
  ok := coalesce(p_choice = (k ->> 'a')::int, false);
  ms := greatest(0, least(600000, (extract(epoch from (now() - (r.state ->> 'round_at')::timestamptz)) * 1000)::int));

  if r.game = 'buzzer' then
    if r.turn_user is distinct from uid then return studyverse._live_err('Buzz first!', 'not_your_turn'); end if;
    insert into studyverse.room_answers (code, qi, user_id, choice, correct, ms, points) values (c, r.qi, uid, coalesce(p_choice, -1), ok, ms, case when ok then 100 else 0 end)
      on conflict (code, qi, user_id) do nothing;
    update studyverse.room_players set answered = answered + 1, correct = correct + case when ok then 1 else 0 end,
      score = score + case when ok then 100 else 0 end, total_ms = total_ms + case when ok then ms else 0 end where code = c and user_id = uid;
    if ok then
      update studyverse.game_rooms set turn_user = null, step = step + 1, deadline = now(),
        state = (state - 'buzz') || jsonb_build_object('done', true, 'done_at', now(), 'winner', uid) where code = c;
    else
      select count(*) into act from studyverse.room_players where code = c and left_at is null;
      nout := jsonb_array_length(coalesce(r.state -> 'out', '[]'::jsonb)) + 1;
      update studyverse.game_rooms set turn_user = null, step = step + 1,
        deadline = case when nout >= act then now() else now() + make_interval(secs => r.turn_secs) end,
        state = (state - 'buzz') || jsonb_build_object('out', coalesce(state -> 'out', '[]'::jsonb) || to_jsonb(uid::text))
                || case when nout >= act then jsonb_build_object('done', true, 'done_at', now()) else '{}'::jsonb end
      where code = c;
    end if;
    return jsonb_build_object('ok', true, 'correct', ok, 'answer', (k ->> 'a')::int, 'explain', k ->> 'x', 'points', case when ok then 100 else 0 end);
  end if;

  -- quiz / duel / relay
  if coalesce((r.state ->> 'done')::boolean, false) then return studyverse._live_err('Too late — time is up.', 'late'); end if;
  if r.game = 'relay' and not ((r.state -> 'runners') ? uid::text) then return studyverse._live_err('It is your teammate''s turn.', 'not_your_turn'); end if;
  if exists (select 1 from studyverse.room_answers where code = c and qi = r.qi and user_id = uid) then return studyverse._live_err('You already answered.', 'answered'); end if;
  if ok then pts := 50 + round(50 * greatest(0, 1 - ms / (r.turn_secs * 1000.0)))::int; end if;
  insert into studyverse.room_answers (code, qi, user_id, choice, correct, ms, points) values (c, r.qi, uid, coalesce(p_choice, -1), ok, ms, pts);
  update studyverse.room_players set answered = answered + 1, correct = correct + case when ok then 1 else 0 end, score = score + pts,
    total_ms = total_ms + ms where code = c and user_id = uid;
  if studyverse._live_complete(c) then
    update studyverse.game_rooms set state = state || jsonb_build_object('done', true, 'done_at', now()) where code = c;
  end if;
  return jsonb_build_object('ok', true, 'correct', ok, 'answer', (k ->> 'a')::int, 'explain', k ->> 'x', 'points', pts, 'ms', ms);
end $$;

-- any member may call this; it only acts when the turn / round is really over (deadline passed, everyone answered,
-- or the player whose turn it is has gone offline), so a game can never stall and nobody can skip others early
create or replace function studyverse.advance(p_code text, p_step int) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; gone boolean; act int; nout int; reveal interval := interval '2 seconds';
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found then return studyverse._live_err('Room not found.', 'not_found'); end if;
  if not exists (select 1 from studyverse.room_players where code = c and user_id = uid) then return studyverse._live_err('You are not in this room.', 'not_member'); end if;
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

create or replace function studyverse.finish_game(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> auth.uid() then return studyverse._live_err('Only the host can end the game.'); end if;
  if r.status <> 'playing' then return jsonb_build_object('ok', true); end if;
  perform studyverse._live_finish(c);
  return jsonb_build_object('ok', true);
end $$;

-- host: back to the lobby with the same players for another game
create or replace function studyverse.rematch(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms;
begin
  select * into r from studyverse.game_rooms where code = c for update;
  if not found or r.host_id <> auth.uid() then return studyverse._live_err('Only the host can start a new game.'); end if;
  if r.status <> 'finished' then return studyverse._live_err('The game is not over yet.'); end if;
  delete from studyverse.room_players where code = c and left_at is not null;
  delete from studyverse.room_answers where code = c;
  delete from studyverse.room_keys where code = c;
  update studyverse.room_players set ready = (user_id = r.host_id), score = 0, correct = 0, answered = 0, total_ms = 0, pos = 1, qn = 0 where code = c;
  update studyverse.game_rooms set status = 'lobby', step = step + 1, qi = 0, turn_user = null, deadline = null, state = '{}'::jsonb, questions = null,
    started_at = null, finished_at = null, expires_at = now() + interval '2 hours' where code = c;
  return jsonb_build_object('ok', true);
end $$;

-- everything a member's app needs, in one call (polled every few seconds and after every live "sync" event).
-- Also: marks the caller as seen (online), and hands the host role on if the host has gone (60 s).
create or replace function studyverse.room_state(p_code text, p_q boolean default false) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; me studyverse.room_players; nh uuid; pl jsonb; mine jsonb := null; rv jsonb := null; k jsonb; ended boolean; ids jsonb := '[]'::jsonb;
begin
  if uid is null then return studyverse._live_err('Please sign in first.', 'signin'); end if;
  select * into r from studyverse.game_rooms where code = c;
  if not found or r.expires_at < now() then return studyverse._live_err('This room has closed.', 'not_found'); end if;
  select * into me from studyverse.room_players where code = c and user_id = uid;
  if not found then return studyverse._live_err('You are not in this room.', 'not_member') || jsonb_build_object('banned', uid = any (r.banned)); end if;
  update studyverse.room_players set last_seen = now() where code = c and user_id = uid;
  if r.status <> 'finished' and me.left_at is null and r.host_id <> uid
     and not exists (select 1 from studyverse.room_players where code = c and user_id = r.host_id and left_at is null and last_seen > now() - interval '60 seconds') then
    select user_id into nh from studyverse.room_players where code = c and left_at is null and (last_seen > now() - interval '60 seconds' or user_id = uid) order by seat limit 1;
    if nh is not null then
      update studyverse.game_rooms set host_id = nh, step = step + 1 where code = c and host_id = r.host_id;
      select * into r from studyverse.game_rooms where code = c;
    end if;
  end if;
  select coalesce(jsonb_agg(jsonb_build_object('user_id', user_id, 'name', name, 'avatar', avatar, 'course', course, 'team', team, 'seat', seat, 'ready', ready,
           'score', score, 'correct', correct, 'answered', answered, 'total_ms', total_ms, 'pos', pos, 'left', left_at is not null,
           'online', left_at is null and (user_id = uid or last_seen > now() - interval '45 seconds')) order by seat), '[]'::jsonb)
    into pl from studyverse.room_players where code = c;
  if r.status <> 'lobby' and r.game <> 'snakes' then
    select coalesce(jsonb_agg(user_id), '[]'::jsonb) into ids from studyverse.room_answers where code = c and qi = r.qi;
    select jsonb_build_object('qi', qi, 'choice', choice, 'correct', correct, 'points', points) into mine from studyverse.room_answers where code = c and qi = r.qi and user_id = uid;
    ended := r.status = 'finished' or coalesce((r.state ->> 'done')::boolean, false) or now() > r.deadline + interval '1.5 seconds';
    if mine is not null or ended then
      select keys -> me.course -> r.qi into k from studyverse.room_keys where code = c;
      if k is not null then rv := jsonb_build_object('qi', r.qi, 'answer', (k ->> 'a')::int, 'explain', k ->> 'x'); end if;
    end if;
  end if;
  return jsonb_build_object('ok', true, 'now', extract(epoch from now()) * 1000,
    'room', jsonb_build_object('code', r.code, 'host_id', r.host_id, 'game', r.game, 'mode', r.mode, 'rounds', r.rounds, 'turn_secs', r.turn_secs, 'level', r.level,
       'status', r.status, 'step', r.step, 'qi', r.qi, 'turn_user', r.turn_user, 'deadline', extract(epoch from r.deadline) * 1000,
       'round_at', extract(epoch from (r.state ->> 'round_at')::timestamptz) * 1000,
       'done_at', extract(epoch from (r.state ->> 'done_at')::timestamptz) * 1000,
       'state', r.state - 'round_at' - 'done_at', 'expires_at', r.expires_at, 'answered_ids', ids),
    'players', pl, 'me', jsonb_build_object('user_id', uid, 'course', me.course, 'left', me.left_at is not null, 'answer', mine, 'reveal', rv),
    'questions', case when p_q and r.questions is not null then r.questions -> me.course end);
end $$;

-- this week's friends leaderboard: everyone you finished a game with in the last 7 days (first name + avatar only)
create or replace function studyverse.weekly_board() returns jsonb
language sql stable security definer set search_path = '' as $$
  with mine as (select distinct code from studyverse.game_results where user_id = auth.uid() and finished_at > now() - interval '7 days'),
  pals as (select distinct user_id from studyverse.game_results where code in (select code from mine) union select auth.uid()),
  agg as (select g.user_id, count(*) as games, count(*) filter (where won) as wins, sum(score) as points,
                 (array_agg(name order by finished_at desc))[1] as name, (array_agg(avatar order by finished_at desc))[1] as avatar
          from studyverse.game_results g where g.user_id in (select user_id from pals) and g.finished_at > now() - interval '7 days' group by g.user_id)
  select coalesce(jsonb_agg(jsonb_build_object('name', name, 'avatar', avatar, 'games', games, 'wins', wins, 'points', points, 'me', user_id = auth.uid())
                            order by wins desc, games desc, points desc), '[]'::jsonb)
  from (select * from agg order by wins desc, games desc, points desc limit 20) t;
$$;

do $$ declare f text; begin
  foreach f in array array['live_eligibility()', 'create_room(text, text, int, int, text, text, text, text)', 'join_room(text, text, text, text)', 'leave_room(text)',
    'kick_player(text, uuid)', 'update_room(text, text, text, int, int, text)', 'set_ready(text, boolean)', 'set_team(text, int)', 'start_game(text, jsonb)',
    'submit_move(text, int)', 'buzz(text, int)', 'submit_answer(text, int, int)', 'advance(text, int)', 'finish_game(text)', 'rematch(text)',
    'room_state(text, boolean)', 'weekly_board()'] loop
    execute format('revoke all on function studyverse.%s from public, anon', f);
    execute format('grant execute on function studyverse.%s to authenticated', f);
  end loop;
end $$;

-- Optional: hourly cleanup with pg_cron (if the extension is on):
--   select cron.schedule('studyverse-live-cleanup', '17 * * * *', $$select studyverse.live_cleanup()$$);
notify pgrst, 'reload schema';
