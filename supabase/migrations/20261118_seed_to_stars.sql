-- ============================================================================================
-- 🌱→🌌 Seed to Stars (replaces the small-group Ratna League; owner-only until league_settings.live).
-- Levels 0..7: Seed, Sprout, Bloom, Tree, Summit, Sky, Star, Galaxy.
-- • One board per study level (class / JEE / CA level) per week: rank, percentile, top 10, the 2 just above you.
-- • Climb: reach your level's weekly target (100 + 50 × level) → up one level next Monday (IST).
--   You go down one level only after a week with no study at all. Hall of Fame = everyone who hit their target.
-- • Self-race: last week's points, last week's points by this same day ("ghost"), best week ever.
-- • Most Improved: biggest rise over last week (students who studied both weeks).
-- Points: unchanged rules in league_award (server-set, unique refs, 200/day, 60 right answers/day, rate limit).
-- studyverse schema only.
-- ============================================================================================
delete from studyverse.league_weeks;                        -- only preview rows existed (owner)
alter table studyverse.league_weeks drop column if exists group_id;
drop table if exists studyverse.league_groups;
alter table studyverse.league_profile drop constraint if exists league_profile_tier_check;
alter table studyverse.league_profile add constraint league_profile_tier_check check (tier between 0 and 7);
update studyverse.league_profile set tier = 0, result = null;
drop index if exists studyverse.league_weeks_group;
create index if not exists league_weeks_board on studyverse.league_weeks (week, lvl, points desc);

create or replace function studyverse._lg_target(t int) returns int language sql immutable set search_path = '' as
$$ select 100 + 50 * greatest(0, least(7, t)) $$;

drop function if exists studyverse._lg_join(uuid, text, text, text);
create function studyverse._lg_join(p_uid uuid, p_lvl text, p_name text, p_avatar text)
returns studyverse.league_weeks language plpgsql security definer set search_path = '' as $$
declare wk date := studyverse._lg_week(); r studyverse.league_weeks; lw studyverse.league_weeks; t smallint; nt smallint;
begin
  insert into studyverse.league_profile (user_id, name, avatar) values (p_uid, studyverse._live_first(p_name),
    coalesce(nullif(left(trim(coalesce(p_avatar, '')), 8), ''), '🙂')) on conflict (user_id) do update
    set name = case when trim(coalesce(p_name, '')) = '' then studyverse.league_profile.name else excluded.name end,
        avatar = case when trim(coalesce(p_avatar, '')) = '' then studyverse.league_profile.avatar else excluded.avatar end;
  select tier into t from studyverse.league_profile where user_id = p_uid for update;     -- one join at a time per user
  select * into r from studyverse.league_weeks where user_id = p_uid and week = wk;
  if found then
    if r.lvl <> p_lvl then update studyverse.league_weeks set lvl = p_lvl where user_id = p_uid and week = wk returning * into r; end if;
    return r;
  end if;
  -- settle: look only at the latest earlier week
  select * into lw from studyverse.league_weeks where user_id = p_uid and week < wk order by week desc limit 1;
  if found and not lw.settled then
    nt := case when lw.points >= studyverse._lg_target(lw.tier) and lw.tier < 7 then lw.tier + 1
               when lw.points = 0 and lw.tier > 0 then lw.tier - 1 else lw.tier end;
    if lw.week < wk - 7 and nt > 0 and nt <= lw.tier then nt := nt - 1; end if;     -- missed at least one whole week
    update studyverse.league_profile set tier = nt,
      result = case when nt > lw.tier then 'up:' when nt < lw.tier then 'down:' else 'stay:' end || nt || ':' || lw.points
      where user_id = p_uid;
    update studyverse.league_weeks set settled = true where user_id = p_uid and week < wk;
    t := nt;
  end if;
  insert into studyverse.league_weeks (user_id, week, tier, lvl) values (p_uid, wk, t, p_lvl) returning * into r;
  return r;
end $$;

create or replace function studyverse.league_board(p_lvl text, p_name text default null, p_avatar text default null)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); w studyverse.league_weeks; res text; today int; d date := studyverse._lg_today();
  n int; rk int; tgt int; lastp int; ghost int; best int; top jsonb; near jsonb; hall jsonb; hall_n int; imp jsonb;
begin
  if uid is null then return jsonb_build_object('ok', false, 'why', 'auth'); end if;
  if not studyverse._lg_open() then return jsonb_build_object('ok', false, 'why', 'off'); end if;
  if coalesce(p_lvl, '') !~ '^[a-z0-9-]{2,30}$' then return jsonb_build_object('ok', false, 'why', 'bad'); end if;
  w := studyverse._lg_join(uid, p_lvl, p_name, p_avatar);
  select result into res from studyverse.league_profile where user_id = uid;
  update studyverse.league_profile set result = null where user_id = uid and result is not null;
  select coalesce(sum(pts), 0) into today from studyverse.league_events where user_id = uid and day = d;
  tgt := studyverse._lg_target(w.tier);

  -- the board: everyone at this level this week
  select count(*) into n from studyverse.league_weeks where week = w.week and lvl = w.lvl;
  select count(*) + 1 into rk from studyverse.league_weeks where week = w.week and lvl = w.lvl and points > w.points;
  select coalesce(jsonb_agg(jsonb_build_object('n', p.name, 'a', p.avatar, 'p', x.points, 't', x.tier, 'me', x.user_id = uid) order by x.points desc, p.name), '[]')
    into top from (select * from studyverse.league_weeks where week = w.week and lvl = w.lvl order by points desc limit 10) x
    join studyverse.league_profile p on p.user_id = x.user_id;
  select coalesce(jsonb_agg(jsonb_build_object('n', y.name, 'a', y.avatar, 'p', y.points, 'gap', y.points - w.points) order by y.points), '[]')
    into near from (select p.name, p.avatar, x.points from studyverse.league_weeks x join studyverse.league_profile p on p.user_id = x.user_id
                    where x.week = w.week and x.lvl = w.lvl and x.points > w.points order by x.points asc limit 2) y;

  -- Hall of Fame: reached their own level's target this week
  select count(*) into hall_n from studyverse.league_weeks where week = w.week and lvl = w.lvl and points >= studyverse._lg_target(tier);
  select coalesce(jsonb_agg(jsonb_build_object('n', p.name, 'a', p.avatar, 't', x.tier, 'me', x.user_id = uid) order by x.points desc), '[]')
    into hall from (select * from studyverse.league_weeks where week = w.week and lvl = w.lvl and points >= studyverse._lg_target(tier)
                    order by points desc limit 20) x join studyverse.league_profile p on p.user_id = x.user_id;

  -- Most Improved: biggest rise over last week (studied both weeks)
  select coalesce(jsonb_agg(jsonb_build_object('n', z.name, 'a', z.avatar, 'g', z.gain, 'me', z.user_id = uid) order by z.gain desc), '[]')
    into imp from (select p.name, p.avatar, x.user_id, x.points - l.points gain from studyverse.league_weeks x
                   join studyverse.league_weeks l on l.user_id = x.user_id and l.week = w.week - 7 and l.points > 0
                   join studyverse.league_profile p on p.user_id = x.user_id
                   where x.week = w.week and x.lvl = w.lvl and x.points > l.points order by x.points - l.points desc limit 5) z;

  -- racing yourself
  select points into lastp from studyverse.league_weeks where user_id = uid and week = w.week - 7;
  select coalesce(sum(pts), 0) into ghost from studyverse.league_events where user_id = uid and day between w.week - 7 and d - 7;
  select coalesce(max(points), 0) into best from studyverse.league_weeks where user_id = uid and week < w.week;

  return jsonb_build_object('ok', true, 'tier', w.tier, 'week', w.week, 'points', w.points, 'today', today, 'cap', 200, 'target', tgt,
    'ends', ((w.week + 7)::timestamp at time zone 'Asia/Kolkata'), 'result', res,
    'n', n, 'rank', rk, 'top', top, 'near', near, 'hall', hall, 'hall_n', hall_n, 'improved', imp,
    'last', lastp, 'ghost', case when lastp is null then null else ghost end, 'best', best);
end $$;

revoke all on function studyverse._lg_join(uuid, text, text, text), studyverse._lg_target(int) from public, anon, authenticated;
revoke all on function studyverse.league_board(text, text, text) from public, anon;
grant execute on function studyverse.league_board(text, text, text) to authenticated;
