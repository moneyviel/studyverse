-- ============================================================================================
-- 👨‍👩‍👧 Family play across devices: a PARENT account may join a Game Room that their OWN linked child is hosting
-- (studyverse.parent_links). Everything else about rooms is unchanged: parents still cannot create rooms, and the
-- host (the student) still needs live access (paid, code or trial). Grown-ups play with course 'gk'
-- (general knowledge, picked by the host's app). Only _pr_base_join_room changes (join_room wraps it).
-- Idempotent.
-- ============================================================================================
create or replace function studyverse._pr_base_join_room(p_code text, p_name text, p_avatar text, p_course text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); w text := studyverse._live_why(auth.uid()); c text := upper(trim(coalesce(p_code, ''))); r studyverse.game_rooms; n int; t0 int; t1 int;
begin
  if w = 'parent' and exists (select 1 from studyverse.game_rooms g join studyverse.parent_links pl on pl.child_id = g.host_id
                              where g.code = c and pl.parent_id = uid) then
    w := 'ok';                                                              -- a parent joining their own child's room
  end if;
  if w = 'parent' then return studyverse._live_err('Ask your child to start a family room in their app, then type its code here. Only rooms started by your linked child can be joined.', 'parent'); end if;
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
