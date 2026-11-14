-- ============================================================================================
-- 💎 Ratna League: weekly league of up to 30 students at the same level. Points come only from learning
-- (topics/units finished, right answers, fixing past mistakes, revision) and are set HERE, never by the app.
-- Top 5 move up a tier on Monday (IST), bottom 5 move down (groups of 10+ only). Tiers 0..6:
-- Mitti, Tamba, Chandi, Sona, Heera, Navratna, Kohinoor.
-- Owner-only until studyverse.league_settings.live = true. studyverse schema only. Idempotent.
-- ============================================================================================
create table if not exists studyverse.league_settings (id int primary key default 1 check (id = 1), live boolean not null default false);
insert into studyverse.league_settings (id, live) values (1, false) on conflict (id) do nothing;

create table if not exists studyverse.league_profile (
  user_id uuid primary key references auth.users(id) on delete cascade,
  tier smallint not null default 0 check (tier between 0 and 6),
  name text not null default 'Student', avatar text not null default '🙂',
  last_day date, result text, created_at timestamptz not null default now());

create table if not exists studyverse.league_groups (
  id bigserial primary key, week date not null, lvl text not null, tier smallint not null, n int not null default 0);
create index if not exists league_groups_find on studyverse.league_groups (week, lvl, tier, n);

create table if not exists studyverse.league_weeks (
  user_id uuid not null references auth.users(id) on delete cascade, week date not null,
  group_id bigint not null references studyverse.league_groups(id) on delete cascade,
  tier smallint not null, lvl text not null, points int not null default 0, settled boolean not null default false,
  primary key (user_id, week));
create index if not exists league_weeks_group on studyverse.league_weeks (group_id, points desc);

create table if not exists studyverse.league_events (
  user_id uuid not null references auth.users(id) on delete cascade, ref text not null, pts int not null,
  day date not null, at timestamptz not null default now(), primary key (user_id, ref));
create index if not exists league_events_day on studyverse.league_events (user_id, day);

alter table studyverse.league_settings enable row level security;
alter table studyverse.league_profile enable row level security;
alter table studyverse.league_groups enable row level security;
alter table studyverse.league_weeks enable row level security;
alter table studyverse.league_events enable row level security;
revoke all on studyverse.league_settings, studyverse.league_profile, studyverse.league_groups,
              studyverse.league_weeks, studyverse.league_events from anon, authenticated;

create or replace function studyverse._lg_today() returns date language sql stable set search_path = '' as
$$ select (now() at time zone 'Asia/Kolkata')::date $$;
create or replace function studyverse._lg_week() returns date language sql stable set search_path = '' as
$$ select date_trunc('week', (now() at time zone 'Asia/Kolkata'))::date $$;
create or replace function studyverse._lg_open() returns boolean language sql stable security definer set search_path = '' as
$$ select coalesce((select live from studyverse.league_settings where id = 1), false) or studyverse.is_admin() $$;

-- settle the user's finished week(s) and put them in a group for this week
create or replace function studyverse._lg_join(p_uid uuid, p_lvl text, p_name text, p_avatar text)
returns studyverse.league_weeks language plpgsql security definer set search_path = '' as $$
declare wk date := studyverse._lg_week(); r studyverse.league_weeks; o record; rk int; t smallint; g bigint;
begin
  insert into studyverse.league_profile (user_id, name, avatar) values (p_uid, studyverse._live_first(p_name),
    coalesce(nullif(left(trim(coalesce(p_avatar, '')), 8), ''), '🙂')) on conflict (user_id) do update
    set name = excluded.name, avatar = case when trim(coalesce(p_avatar, '')) = '' then studyverse.league_profile.avatar else excluded.avatar end;
  select tier into t from studyverse.league_profile where user_id = p_uid for update;     -- one join at a time per user
  select * into r from studyverse.league_weeks where user_id = p_uid and week = wk;
  if found then return r; end if;
  for o in select w.* , gr.n from studyverse.league_weeks w join studyverse.league_groups gr on gr.id = w.group_id
           where w.user_id = p_uid and w.week < wk and not w.settled order by w.week loop
    select x.rk into rk from (select user_id, rank() over (order by points desc) rk from studyverse.league_weeks where group_id = o.group_id) x
      where x.user_id = p_uid;
    if o.points > 0 and rk <= 5 and o.tier < 6 then t := o.tier + 1; update studyverse.league_profile set result = 'up:' || t where user_id = p_uid;
    elsif o.n >= 10 and rk > o.n - 5 and o.tier > 0 then t := o.tier - 1; update studyverse.league_profile set result = 'down:' || t where user_id = p_uid;
    else t := o.tier; update studyverse.league_profile set result = 'stay:' || t where user_id = p_uid; end if;
    update studyverse.league_weeks set settled = true where user_id = p_uid and week = o.week;
  end loop;
  update studyverse.league_profile set tier = t where user_id = p_uid;
  select id into g from studyverse.league_groups where week = wk and lvl = p_lvl and tier = t and n < 30 order by n desc, id limit 1 for update;
  if not found then insert into studyverse.league_groups (week, lvl, tier) values (wk, p_lvl, t) returning id into g; end if;
  update studyverse.league_groups set n = n + 1 where id = g;
  insert into studyverse.league_weeks (user_id, week, group_id, tier, lvl) values (p_uid, wk, g, t, p_lvl) returning * into r;
  return r;
end $$;

create or replace function studyverse.league_award(p_kind text, p_ref text, p_lvl text, p_name text default null, p_avatar text default null)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); d date := studyverse._lg_today(); v int; today int; recent int; k text; w studyverse.league_weeks; ld date; bonus int := 0;
begin
  if uid is null then return jsonb_build_object('ok', false, 'why', 'auth'); end if;
  if not studyverse._lg_open() then return jsonb_build_object('ok', false, 'why', 'off'); end if;
  if coalesce(p_lvl, '') !~ '^[a-z0-9-]{2,30}$' or coalesce(p_ref, '') !~ '^[A-Za-z0-9:_./-]{1,100}$' then
    return jsonb_build_object('ok', false, 'why', 'bad'); end if;
  v := case p_kind when 'topic' then 20 when 'unit' then 20 when 'revise' then 10 when 'fix' then 4 when 'right' then 2 else null end;
  if v is null then return jsonb_build_object('ok', false, 'why', 'bad'); end if;
  k := p_kind || ':' || p_ref || case when p_kind in ('right', 'fix', 'revise') then ':' || d else '' end;
  if exists (select 1 from studyverse.league_events where user_id = uid and ref = k) then return jsonb_build_object('ok', true, 'pts', 0, 'dup', true); end if;
  select count(*) into recent from studyverse.league_events where user_id = uid and at > now() - interval '1 minute';
  if recent >= 30 then return jsonb_build_object('ok', true, 'pts', 0, 'slow', true); end if;
  -- right answers alone can give at most 120 a day (60 × 2), so finishing and fixing always matter
  if p_kind = 'right' and (select count(*) from studyverse.league_events where user_id = uid and day = d and ref like 'right:%') >= 60 then
    return jsonb_build_object('ok', true, 'pts', 0, 'cap', true); end if;
  select coalesce(sum(pts), 0) into today from studyverse.league_events where user_id = uid and day = d;
  if today >= 200 then return jsonb_build_object('ok', true, 'pts', 0, 'cap', true); end if;
  w := studyverse._lg_join(uid, p_lvl, p_name, p_avatar);
  select last_day into ld from studyverse.league_profile where user_id = uid;
  if ld is not null and ld <= d - 3 then bonus := 15; end if;
  v := least(v + bonus, 200 - today);
  insert into studyverse.league_events (user_id, ref, pts, day) values (uid, k, v, d) on conflict do nothing;
  if not found then return jsonb_build_object('ok', true, 'pts', 0, 'dup', true); end if;
  update studyverse.league_weeks set points = points + v where user_id = uid and week = w.week;
  update studyverse.league_profile set last_day = d where user_id = uid;
  return jsonb_build_object('ok', true, 'pts', v, 'comeback', bonus > 0, 'today', today + v);
end $$;

create or replace function studyverse.league_board(p_lvl text, p_name text default null, p_avatar text default null)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); w studyverse.league_weeks; res text; rs jsonb; today int;
begin
  if uid is null then return jsonb_build_object('ok', false, 'why', 'auth'); end if;
  if not studyverse._lg_open() then return jsonb_build_object('ok', false, 'why', 'off'); end if;
  if coalesce(p_lvl, '') !~ '^[a-z0-9-]{2,30}$' then return jsonb_build_object('ok', false, 'why', 'bad'); end if;
  w := studyverse._lg_join(uid, p_lvl, p_name, p_avatar);
  select result into res from studyverse.league_profile where user_id = uid;
  update studyverse.league_profile set result = null where user_id = uid and result is not null;
  select coalesce(sum(pts), 0) into today from studyverse.league_events where user_id = uid and day = studyverse._lg_today();
  select coalesce(jsonb_agg(jsonb_build_object('n', p.name, 'a', p.avatar, 'p', x.points, 'me', x.user_id = uid) order by x.points desc, p.name), '[]')
    into rs from studyverse.league_weeks x join studyverse.league_profile p on p.user_id = x.user_id where x.group_id = w.group_id;
  return jsonb_build_object('ok', true, 'tier', w.tier, 'week', w.week, 'points', w.points, 'today', today, 'cap', 200,
    'ends', ((w.week + 7)::timestamp at time zone 'Asia/Kolkata'), 'result', res, 'rows', rs);
end $$;

revoke all on function studyverse._lg_join(uuid, text, text, text), studyverse._lg_open(), studyverse._lg_today(), studyverse._lg_week() from public, anon, authenticated;
revoke all on function studyverse.league_award(text, text, text, text, text), studyverse.league_board(text, text, text) from public, anon;
grant execute on function studyverse.league_award(text, text, text, text, text), studyverse.league_board(text, text, text) to authenticated;
