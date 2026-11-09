-- ============================================================================================
-- StudyVerse 🦁 Squad (school) / 👥 Group (CA) — schema studyverse.
--   1. Weekly stars: the app sends its stars per day (ST.xpLog) with rpc squad_sync (debounced, about once a minute
--      at most when something changed). Each day is capped at 1500 stars and can only go up. Weeks start on MONDAY
--      (India time, Asia/Kolkata). Rows older than 3 weeks are removed.
--   2. Class vs class league: students enrolled by a school / coaching (institution_members.role = 'student' with a
--      class) see the classes of their institution with the same course (7-A vs 7-B vs 7-C; all classes if their
--      course has only one), ranked by AVERAGE weekly stars per ACTIVE student (active = earned stars this week or
--      last week). Only class names and numbers are shown, never a student's name.
--   3. Friends: a 6-letter friend code per student. Entering a code sends a REQUEST; nobody sees anybody until the
--      request is accepted (children's safety — we do not know ages, so this applies to everyone). Only first name +
--      avatar + weekly stars + streak + puzzle best times are shared with accepted friends; never the email.
--      Limits: 50 friends, 10 requests a day, 20 wrong codes a day, 5 new codes a day.
--   4. Cheers: preset kinds only (no free text): clap, fire, star, strong, wave, rocket. One cheer per friend per
--      day, 10 a day. Received cheers are returned once by squad_home (then marked seen).
--   5. Parent challenge: a linked parent (studyverse.parent_links) starts a 5-question duel on a subject of the
--      child's course. SERVER-VERIFIED: the 5 questions (text + options) are stored in parent_challenges, their correct
--      options in parent_challenge_answers, which no client can read. Each side calls pc_start (gets the questions, the
--      server notes the start time — once), then pc_submit with the option indexes it picked; the SERVER computes the
--      score and the time. Nobody can send a score. The correct options are returned to a side only after it submitted.
--      Only that parent and that child can read or play it, and only while they are still linked.
--      5 new challenges a day, 3 open per child; 7 days to play.
-- Tables have RLS on and no policies: everything goes through the SECURITY DEFINER functions below.
-- Needs (already in the project): auth.users, studyverse.profiles (role), parent_links, institutions,
-- inst_classes, institution_members (20261109_institutions.sql). Idempotent: safe to run again.
-- ============================================================================================

-- ---------- tables ----------
create table if not exists studyverse.squad_profile (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  code       text unique check (code ~ '^[A-HJ-NP-Z2-9]{6}$'),
  name       text not null default 'Friend' check (length(name) between 1 and 20),
  avatar     text not null default '🙂' check (length(avatar) between 1 and 8),
  course     text not null default 'school' check (course in ('school', 'ca')),
  streak     int  not null default 0 check (streak between 0 and 3650),
  streak_day date,
  pz         jsonb not null default '{}'::jsonb,           -- puzzle best times { key: seconds }
  synced_at  timestamptz not null default now()
);

create table if not exists studyverse.squad_stars (
  user_id uuid not null references auth.users(id) on delete cascade,
  day     date not null,
  stars   int  not null check (stars between 0 and 1500),
  primary key (user_id, day)
);
create index if not exists squad_stars_day on studyverse.squad_stars (day);

-- one row per pair, a < b; requested_by = who typed the code
create table if not exists studyverse.squad_friends (
  a            uuid not null references auth.users(id) on delete cascade,
  b            uuid not null references auth.users(id) on delete cascade,
  requested_by uuid not null,
  status       text not null default 'pending' check (status in ('pending', 'accepted')),
  created_at   timestamptz not null default now(),
  accepted_at  timestamptz,
  primary key (a, b),
  check (a < b),
  check (requested_by in (a, b))
);
create index if not exists squad_friends_b on studyverse.squad_friends (b);

create table if not exists studyverse.squad_cheers (
  id      bigint generated always as identity primary key,
  from_id uuid not null references auth.users(id) on delete cascade,
  to_id   uuid not null references auth.users(id) on delete cascade,
  kind    text not null check (kind in ('clap', 'fire', 'star', 'strong', 'wave', 'rocket')),
  at      timestamptz not null default now(),
  seen_at timestamptz
);
create index if not exists squad_cheers_to on studyverse.squad_cheers (to_id, seen_at);
create index if not exists squad_cheers_from on studyverse.squad_cheers (from_id, at);

-- rate-limit log: 'add' (friend request sent), 'badcode' (wrong code), 'newcode' (code changed)
create table if not exists studyverse.squad_events (
  user_id uuid not null references auth.users(id) on delete cascade,
  kind    text not null,
  at      timestamptz not null default now()
);
create index if not exists squad_events_u on studyverse.squad_events (user_id, kind, at);

create table if not exists studyverse.parent_challenges (
  id             uuid primary key default gen_random_uuid(),
  parent_id      uuid not null references auth.users(id) on delete cascade,
  child_id       uuid not null references auth.users(id) on delete cascade,
  src            text not null check (src ~ '^(g([1-9]|1[0-2])/[a-z0-9-]{1,30}|ca/(foundation|inter|final)/[a-z0-9-]{1,40})$'),
  title          text not null check (length(title) between 1 and 60),
  keys           jsonb not null check (jsonb_typeof(keys) = 'array' and jsonb_array_length(keys) = 5),          -- content keys 'g7-maths-01-01#3'
  questions      jsonb not null check (jsonb_typeof(questions) = 'array' and jsonb_array_length(questions) = 5), -- [{q, o:[options]}] — no answers
  parent_started timestamptz, parent_picks int[], parent_score int check (parent_score between 0 and 5), parent_ms int, parent_at timestamptz,
  child_started  timestamptz, child_picks  int[], child_score  int check (child_score between 0 and 5),  child_ms int,  child_at timestamptz,
  created_at     timestamptz not null default now(),
  expires_at     timestamptz not null default now() + interval '7 days'
);
create index if not exists parent_challenges_pc on studyverse.parent_challenges (parent_id, child_id, created_at desc);
create index if not exists parent_challenges_c on studyverse.parent_challenges (child_id, created_at desc);
-- the answer key: never readable by a client (no grants, no policies); only pc_submit uses it
create table if not exists studyverse.parent_challenge_answers (
  challenge_id uuid primary key references studyverse.parent_challenges(id) on delete cascade,
  answers      int[] not null check (array_length(answers, 1) = 5),
  explains     jsonb not null default '[]'::jsonb
);

alter table studyverse.squad_profile enable row level security;
alter table studyverse.squad_stars enable row level security;
alter table studyverse.squad_friends enable row level security;
alter table studyverse.squad_cheers enable row level security;
alter table studyverse.squad_events enable row level security;
alter table studyverse.parent_challenges enable row level security;
alter table studyverse.parent_challenge_answers enable row level security;
revoke all on studyverse.squad_profile, studyverse.squad_stars, studyverse.squad_friends, studyverse.squad_cheers,
              studyverse.squad_events, studyverse.parent_challenges, studyverse.parent_challenge_answers from anon, authenticated;
grant all on studyverse.squad_profile, studyverse.squad_stars, studyverse.squad_friends, studyverse.squad_cheers,
             studyverse.squad_events, studyverse.parent_challenges, studyverse.parent_challenge_answers to service_role;

-- ---------- helpers ----------
create or replace function studyverse._sq_today() returns date language sql stable set search_path = '' as $$
  select (now() at time zone 'Asia/Kolkata')::date $$;
create or replace function studyverse._sq_week() returns date language sql stable set search_path = '' as $$
  select date_trunc('week', (now() at time zone 'Asia/Kolkata')::date)::date $$;          -- Monday
create or replace function studyverse._sq_err(p_msg text) returns jsonb language sql immutable set search_path = '' as $$
  select jsonb_build_object('ok', false, 'msg', p_msg) $$;
create or replace function studyverse._sq_is_parent(p_uid uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select coalesce((select role = 'parent' from studyverse.profiles where user_id = p_uid), false) $$;
-- clean first name: first word only, no control or markup characters, at most 20 characters (Hindi names stay intact)
create or replace function studyverse._sq_name(p text) returns text language sql immutable set search_path = '' as $$
  select coalesce(nullif(left(regexp_replace(split_part(regexp_replace(trim(coalesce(p, '')), '\s+', ' ', 'g'), ' ', 1), '[[:cntrl:]<>&"`\\/{}@]', '', 'g'), 20), ''), 'Friend') $$;
create or replace function studyverse._sq_date(p text) returns date language plpgsql immutable set search_path = '' as $$
begin return case when p ~ '^\d{4}-\d{2}-\d{2}$' then p::date end; exception when others then return null; end $$;
create or replace function studyverse._sq_avatar(p text) returns text language sql immutable set search_path = '' as $$
  select coalesce(nullif(left(regexp_replace(coalesce(p, ''), '[\x01-\x7f]', '', 'g'), 8), ''), '🙂') $$;      -- emoji only: every ASCII character is removed
-- the caller's squad row (made on first use, with a fresh friend code)
create or replace function studyverse._sq_ensure(p_uid uuid) returns studyverse.squad_profile
language plpgsql security definer set search_path = '' as $$
declare r studyverse.squad_profile; k text; alph text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  select * into r from studyverse.squad_profile where user_id = p_uid;
  if found and r.code is not null then return r; end if;
  loop
    k := ''; for i in 1..6 loop k := k || substr(alph, 1 + floor(random() * 32)::int, 1); end loop;
    exit when not exists (select 1 from studyverse.squad_profile where code = k);
  end loop;
  insert into studyverse.squad_profile (user_id, code) values (p_uid, k)
    on conflict (user_id) do update set code = coalesce(studyverse.squad_profile.code, excluded.code)
    returning * into r;
  return r;
end $$;
create or replace function studyverse._sq_pair(x uuid, y uuid) returns studyverse.squad_friends language sql stable security definer set search_path = '' as $$
  select * from studyverse.squad_friends where a = least(x, y) and b = greatest(x, y) $$;
create or replace function studyverse._sq_week_of(p_uid uuid, p_from date) returns int language sql stable security definer set search_path = '' as $$
  select coalesce(sum(stars), 0)::int from studyverse.squad_stars where user_id = p_uid and day >= p_from and day < p_from + 7 $$;
create or replace function studyverse._sq_live_streak(r studyverse.squad_profile) returns int language sql stable set search_path = '' as $$
  select case when r.streak_day is not null and r.streak_day >= studyverse._sq_today() - 1 then r.streak else 0 end $$;
revoke all on function studyverse._sq_today(), studyverse._sq_week(), studyverse._sq_date(text), studyverse._sq_err(text), studyverse._sq_is_parent(uuid), studyverse._sq_name(text),
  studyverse._sq_avatar(text), studyverse._sq_ensure(uuid), studyverse._sq_pair(uuid, uuid), studyverse._sq_week_of(uuid, date),
  studyverse._sq_live_streak(studyverse.squad_profile) from public, anon, authenticated;

-- ---------- 1. weekly stars + public card (name, avatar, streak, puzzle bests) ----------
create or replace function studyverse.squad_sync(p_days jsonb, p_streak int default 0, p_streak_day text default null,
  p_name text default null, p_avatar text default null, p_pz jsonb default null, p_course text default 'school') returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); wk date := studyverse._sq_week(); td date := studyverse._sq_today(); sd date := studyverse._sq_date(p_streak_day); v_pz jsonb := '{}'::jsonb;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if studyverse._sq_is_parent(uid) then return studyverse._sq_err('Parent accounts are not in the squad.'); end if;
  perform studyverse._sq_ensure(uid);
  if sd > td + 1 then sd := null; end if;
  if jsonb_typeof(p_pz) = 'object' then
    select coalesce(jsonb_object_agg(key, round(value::text::numeric)::int), '{}'::jsonb) into v_pz
    from (select key, value from jsonb_each(p_pz)
          where key ~ '^[a-z0-9-]{1,24}$' and jsonb_typeof(value) = 'number' and value::text::numeric between 3 and 86400
          order by key limit 40) t;
  end if;
  update studyverse.squad_profile set
    name = studyverse._sq_name(p_name), avatar = studyverse._sq_avatar(p_avatar),
    course = case when p_course = 'ca' then 'ca' else 'school' end,
    streak = least(greatest(coalesce(p_streak, 0), 0), 3650), streak_day = sd, pz = v_pz, synced_at = now()
  where user_id = uid;
  if jsonb_typeof(p_days) = 'object' then
    insert into studyverse.squad_stars (user_id, day, stars)
    select uid, d, least(greatest(round(v)::int, 0), 1500)
    from (select studyverse._sq_date(key) as d, value::text::numeric as v from jsonb_each(p_days)
          where jsonb_typeof(value) = 'number' limit 16) t
    where d between wk - 7 and td
    on conflict (user_id, day) do update set stars = greatest(studyverse.squad_stars.stars, excluded.stars);
  end if;
  delete from studyverse.squad_stars where user_id = uid and day < wk - 14;
  return jsonb_build_object('ok', true, 'week', studyverse._sq_week_of(uid, wk), 'week_start', wk);
end $$;

-- ---------- 2.–5. everything the Squad screen shows, in one call ----------
create or replace function studyverse.squad_home() returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); me studyverse.squad_profile; wk date := studyverse._sq_week(); td date := studyverse._sq_today();
  cls record; n_same int; league jsonb := null; friends jsonb; incoming jsonb; outgoing int; cheers jsonb; chal jsonb;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if studyverse._sq_is_parent(uid) then return jsonb_build_object('ok', false, 'parent', true, 'msg', 'Parent accounts use Parent Hub.'); end if;
  me := studyverse._sq_ensure(uid);

  -- class league (newest school membership with a class)
  select m.class_id, c.institution_id, c.course, i.name as inst into cls
  from studyverse.institution_members m join studyverse.inst_classes c on c.id = m.class_id join studyverse.institutions i on i.id = c.institution_id
  where m.user_id = uid and m.role = 'student' and m.class_id is not null order by m.joined_at desc limit 1;
  if found then
    select count(*) into n_same from studyverse.inst_classes where institution_id = cls.institution_id and course = cls.course;
    with cl as (select c.id, c.name, c.grade, c.section from studyverse.inst_classes c
                where c.institution_id = cls.institution_id and (n_same < 2 or c.course = cls.course)),
    st as (select m.class_id, m.user_id,
                  coalesce(sum(s.stars) filter (where s.day >= wk), 0) as w,
                  coalesce(sum(s.stars) filter (where s.day >= wk - 7 and s.day < wk), 0) as lw
           from studyverse.institution_members m left join studyverse.squad_stars s on s.user_id = m.user_id and s.day >= wk - 7
           where m.role = 'student' and m.class_id in (select id from cl) group by m.class_id, m.user_id),
    agg as (select cl.id, cl.name, cl.grade, cl.section, count(st.user_id) as size,
                   count(st.user_id) filter (where st.w > 0 or st.lw > 0) as active, coalesce(sum(st.w), 0) as total
            from cl left join st on st.class_id = cl.id group by cl.id, cl.name, cl.grade, cl.section),
    rk as (select *, round(total::numeric / greatest(active, 1), 1) as avg from agg)
    select jsonb_build_object('kind', 'class', 'inst', cls.inst, 'my_class', cls.class_id,
             'classes', coalesce(jsonb_agg(jsonb_build_object('id', id, 'name', name, 'avg', avg, 'active', active, 'size', size, 'me', id = cls.class_id)
                                           order by avg desc, active desc, name), '[]'::jsonb))
      into league from (select * from rk order by avg desc, active desc, name limit 30) t;
  end if;

  -- accepted friends (first name, avatar, weekly stars, streak, puzzle bests)
  select coalesce(jsonb_agg(jsonb_build_object('id', p.user_id, 'name', p.name, 'avatar', p.avatar, 'course', p.course,
           'week', studyverse._sq_week_of(p.user_id, wk), 'last_week', studyverse._sq_week_of(p.user_id, wk - 7),
           'today', coalesce((select stars from studyverse.squad_stars where user_id = p.user_id and day = td), 0),
           'streak', studyverse._sq_live_streak(p), 'pz', p.pz) order by studyverse._sq_week_of(p.user_id, wk) desc, p.name), '[]'::jsonb)
    into friends
  from studyverse.squad_friends f join studyverse.squad_profile p on p.user_id = case when f.a = uid then f.b else f.a end
  where (f.a = uid or f.b = uid) and f.status = 'accepted';

  -- requests sent TO me (the sender chose to show their first name); requests I sent: only a count
  select coalesce(jsonb_agg(jsonb_build_object('id', p.user_id, 'name', p.name, 'avatar', p.avatar) order by f.created_at), '[]'::jsonb) into incoming
  from studyverse.squad_friends f join studyverse.squad_profile p on p.user_id = f.requested_by
  where (f.a = uid or f.b = uid) and f.status = 'pending' and f.requested_by <> uid;
  select count(*) into outgoing from studyverse.squad_friends where (a = uid or b = uid) and status = 'pending' and requested_by = uid;

  -- cheers received and not yet shown (only from people who are still friends)
  with c as (select ch.id, ch.kind, ch.at, p.name, p.avatar from studyverse.squad_cheers ch
             join studyverse.squad_profile p on p.user_id = ch.from_id
             join studyverse.squad_friends f on f.a = least(ch.from_id, uid) and f.b = greatest(ch.from_id, uid) and f.status = 'accepted'
             where ch.to_id = uid and ch.seen_at is null order by ch.at desc limit 10)
  select coalesce(jsonb_agg(jsonb_build_object('name', name, 'avatar', avatar, 'kind', kind, 'at', at) order by at desc), '[]'::jsonb) into cheers from c;
  update studyverse.squad_cheers set seen_at = now() where to_id = uid and seen_at is null;
  delete from studyverse.squad_cheers where to_id = uid and at < now() - interval '30 days';

  -- parent challenges for me (only from a parent I am still linked to)
  select coalesce(jsonb_agg(x order by (x ->> 'created_at') desc), '[]'::jsonb) into chal from (
    select jsonb_build_object('id', c.id, 'src', c.src, 'title', c.title, 'created_at', c.created_at, 'expires_at', c.expires_at, 'started', c.child_started is not null,
             'parent_done', c.parent_score is not null, 'child_score', c.child_score, 'child_ms', c.child_ms, 'child_at', c.child_at,
             'parent_score', case when c.child_score is not null then c.parent_score end,
             'parent_ms', case when c.child_score is not null then c.parent_ms end) as x
    from studyverse.parent_challenges c
    where c.child_id = uid and exists (select 1 from studyverse.parent_links l where l.parent_id = c.parent_id and l.child_id = uid)
      and ((c.child_score is null and c.expires_at > now()) or c.child_at > now() - interval '3 days')
    order by c.created_at desc limit 5) t;

  return jsonb_build_object('ok', true, 'week_start', wk, 'today', td,
    'me', jsonb_build_object('name', me.name, 'avatar', me.avatar, 'code', me.code, 'week', studyverse._sq_week_of(uid, wk),
                             'last_week', studyverse._sq_week_of(uid, wk - 7), 'streak', studyverse._sq_live_streak(me)),
    'league', league, 'friends', friends, 'incoming', incoming, 'outgoing', outgoing, 'cheers', cheers, 'challenges', chal);
end $$;

-- ---------- friends ----------
create or replace function studyverse.squad_add_friend(p_code text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); k text := upper(regexp_replace(coalesce(p_code, ''), '\s', '', 'g')); other uuid; f studyverse.squad_friends; n int;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if studyverse._sq_is_parent(uid) then return studyverse._sq_err('Parent accounts cannot add friends.'); end if;
  perform studyverse._sq_ensure(uid);
  if (select count(*) from studyverse.squad_events where user_id = uid and kind = 'badcode' and at > now() - interval '1 day') >= 20 then
    return studyverse._sq_err('Too many wrong codes today. Please try again tomorrow.'); end if;
  select user_id into other from studyverse.squad_profile where code = k;
  if other is null or studyverse._sq_is_parent(other) then
    insert into studyverse.squad_events (user_id, kind) values (uid, 'badcode');
    return studyverse._sq_err('No friend found with this code. Check the 6 letters and try again.');
  end if;
  if other = uid then return studyverse._sq_err('This is your own code. Share it with a friend!'); end if;
  f := studyverse._sq_pair(uid, other);
  if f.a is not null then
    if f.status = 'accepted' then return jsonb_build_object('ok', true, 'status', 'friends', 'msg', 'You are already friends.'); end if;
    if f.requested_by = uid then return jsonb_build_object('ok', true, 'status', 'pending', 'msg', 'Request already sent. Waiting for your friend to accept.'); end if;
    update studyverse.squad_friends set status = 'accepted', accepted_at = now() where a = f.a and b = f.b;      -- they asked first: accept
    return jsonb_build_object('ok', true, 'status', 'friends', 'msg', 'You are now friends!');
  end if;
  select count(*) into n from studyverse.squad_friends where a = uid or b = uid;
  if n >= 50 then return studyverse._sq_err('You can have up to 50 friends and requests.'); end if;
  if (select count(*) from studyverse.squad_events where user_id = uid and kind = 'add' and at > now() - interval '1 day') >= 10 then
    return studyverse._sq_err('You sent 10 requests today. Please try again tomorrow.'); end if;
  insert into studyverse.squad_friends (a, b, requested_by) values (least(uid, other), greatest(uid, other), uid);
  insert into studyverse.squad_events (user_id, kind) values (uid, 'add');
  return jsonb_build_object('ok', true, 'status', 'pending', 'msg', 'Request sent! Your friend will see it in their Squad.');
end $$;

create or replace function studyverse.squad_answer(p_user uuid, p_accept boolean) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); f studyverse.squad_friends;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  f := studyverse._sq_pair(uid, p_user);
  if f.a is null or f.status <> 'pending' or f.requested_by = uid then return studyverse._sq_err('This request is no longer there.'); end if;
  if coalesce(p_accept, false) then
    update studyverse.squad_friends set status = 'accepted', accepted_at = now() where a = f.a and b = f.b;
    return jsonb_build_object('ok', true, 'status', 'friends');
  end if;
  delete from studyverse.squad_friends where a = f.a and b = f.b;
  return jsonb_build_object('ok', true, 'status', 'declined');
end $$;

-- remove a friend, or take back a request I sent
create or replace function studyverse.squad_remove(p_user uuid) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  delete from studyverse.squad_friends where a = least(uid, p_user) and b = greatest(uid, p_user);
  return jsonb_build_object('ok', true);
end $$;

-- cancel every request I sent that is still waiting
create or replace function studyverse.squad_cancel_requests() returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); n int;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  delete from studyverse.squad_friends where (a = uid or b = uid) and status = 'pending' and requested_by = uid;
  get diagnostics n = row_count;
  return jsonb_build_object('ok', true, 'removed', n);
end $$;

create or replace function studyverse.squad_new_code() returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); k text; alph text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if studyverse._sq_is_parent(uid) then return studyverse._sq_err('Parent accounts cannot add friends.'); end if;
  perform studyverse._sq_ensure(uid);
  if (select count(*) from studyverse.squad_events where user_id = uid and kind = 'newcode' and at > now() - interval '1 day') >= 5 then
    return studyverse._sq_err('You changed your code 5 times today. Please try again tomorrow.'); end if;
  loop
    k := ''; for i in 1..6 loop k := k || substr(alph, 1 + floor(random() * 32)::int, 1); end loop;
    exit when not exists (select 1 from studyverse.squad_profile where code = k);
  end loop;
  update studyverse.squad_profile set code = k where user_id = uid;
  insert into studyverse.squad_events (user_id, kind) values (uid, 'newcode');
  return jsonb_build_object('ok', true, 'code', k);
end $$;

create or replace function studyverse.squad_cheer(p_to uuid, p_kind text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); f studyverse.squad_friends; day0 timestamptz := (studyverse._sq_today()::timestamp at time zone 'Asia/Kolkata');
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if p_kind is null or p_kind not in ('clap', 'fire', 'star', 'strong', 'wave', 'rocket') then return studyverse._sq_err('Pick one of the cheers.'); end if;
  f := studyverse._sq_pair(uid, p_to);
  if f.a is null or f.status <> 'accepted' then return studyverse._sq_err('You can cheer only your friends.'); end if;
  if exists (select 1 from studyverse.squad_cheers where from_id = uid and to_id = p_to and at >= day0) then
    return studyverse._sq_err('You already cheered this friend today. Try again tomorrow!'); end if;
  if (select count(*) from studyverse.squad_cheers where from_id = uid and at >= day0) >= 10 then
    return studyverse._sq_err('That''s 10 cheers today — what a great friend! More tomorrow.'); end if;
  insert into studyverse.squad_cheers (from_id, to_id, kind) values (uid, p_to, p_kind);
  return jsonb_build_object('ok', true);
end $$;

-- ---------- parent challenge (server-verified) ----------
drop function if exists studyverse.pc_submit(uuid, int, int);
create or replace function studyverse._pc_view(c studyverse.parent_challenges, p_parent boolean) returns jsonb language sql stable set search_path = '' as $$
  select jsonb_build_object('id', c.id, 'src', c.src, 'title', c.title, 'created_at', c.created_at, 'expires_at', c.expires_at,
    'started',      case when p_parent then c.parent_started else c.child_started end is not null,
    'parent_score', case when p_parent or c.child_score is not null then c.parent_score end,
    'parent_ms',    case when p_parent or c.child_score is not null then c.parent_ms end,
    'parent_done',  c.parent_score is not null,
    'child_score',  case when not p_parent or c.parent_score is not null then c.child_score end,
    'child_ms',     case when not p_parent or c.parent_score is not null then c.child_ms end,
    'child_done',   c.child_score is not null) $$;
revoke all on function studyverse._pc_view(studyverse.parent_challenges, boolean) from public, anon, authenticated;

-- p_questions: 5 × { k: 'g7-maths-01-01#3', q: text, o: [2–6 options], a: index of the right option, x: explanation (optional) }
create or replace function studyverse.pc_create(p_child uuid, p_src text, p_title text, p_questions jsonb) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); pre text; c studyverse.parent_challenges; bad int; qs jsonb; ks jsonb; ans int[]; xs jsonb;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if not exists (select 1 from studyverse.parent_links where parent_id = uid and child_id = p_child) then
    return studyverse._sq_err('You can challenge only a child linked to your Parent Hub.'); end if;
  if p_src is null or p_src !~ '^(g([1-9]|1[0-2])/[a-z0-9-]{1,30}|ca/(foundation|inter|final)/[a-z0-9-]{1,40})$' then return studyverse._sq_err('Choose a subject.'); end if;
  if jsonb_typeof(p_questions) is distinct from 'array' or jsonb_array_length(p_questions) <> 5 then return studyverse._sq_err('A challenge has 5 questions.'); end if;
  -- every question must belong to the chosen subject: school 'g7/maths' → 'g7-maths-…#3'; CA 'ca/foundation/fnd-p1' → 'fnd-p1-…#m1'
  pre := case when p_src like 'ca/%' then split_part(p_src, '/', 3) || '-' else replace(p_src, '/', '-') || '-' end;
  select count(*) into bad from jsonb_array_elements(p_questions) e
    where jsonb_typeof(e) <> 'object'
       or coalesce(e ->> 'k', '') !~ '^[a-z0-9-]{3,60}#[A-Za-z0-9_-]{1,20}$' or left(e ->> 'k', length(pre)) <> pre
       or jsonb_typeof(e -> 'q') <> 'string' or length(e ->> 'q') not between 1 and 600
       or jsonb_typeof(e -> 'o') <> 'array' or jsonb_array_length(e -> 'o') not between 2 and 6
       or exists (select 1 from jsonb_array_elements(e -> 'o') o where jsonb_typeof(o) <> 'string' or length(o #>> '{}') not between 1 and 200)
       or jsonb_typeof(e -> 'a') <> 'number' or (e ->> 'a') !~ '^\d+$' or (e ->> 'a')::int >= jsonb_array_length(e -> 'o')
       or (e ? 'x' and jsonb_typeof(e -> 'x') not in ('string', 'null'));
  if bad > 0 then return studyverse._sq_err('These questions do not fit the subject.'); end if;
  if (select count(distinct e ->> 'k') from jsonb_array_elements(p_questions) e) <> 5 then return studyverse._sq_err('The same question twice is not allowed.'); end if;
  if (select count(*) from studyverse.parent_challenges where parent_id = uid and created_at > now() - interval '1 day') >= 5 then
    return studyverse._sq_err('That''s 5 challenges today. Try again tomorrow!'); end if;
  if (select count(*) from studyverse.parent_challenges where parent_id = uid and child_id = p_child and child_score is null and expires_at > now()) >= 3 then
    return studyverse._sq_err('3 challenges are already waiting for your child. Wait until they play one.'); end if;
  select jsonb_agg(jsonb_build_object('q', e -> 'q', 'o', e -> 'o') order by n), jsonb_agg(e -> 'k' order by n),
         array_agg((e ->> 'a')::int order by n), jsonb_agg(left(coalesce(e ->> 'x', ''), 600) order by n)
    into qs, ks, ans, xs from jsonb_array_elements(p_questions) with ordinality as t(e, n);
  insert into studyverse.parent_challenges (parent_id, child_id, src, title, keys, questions)
    values (uid, p_child, p_src, left(trim(coalesce(nullif(trim(p_title), ''), 'Challenge')), 60), ks, qs) returning * into c;
  insert into studyverse.parent_challenge_answers (challenge_id, answers, explains) values (c.id, ans, xs);
  return jsonb_build_object('ok', true, 'challenge', studyverse._pc_view(c, true));
end $$;

-- open a challenge to play: returns the 5 questions WITHOUT answers; the first call starts this side's clock
create or replace function studyverse.pc_start(p_id uuid) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c studyverse.parent_challenges; par boolean;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  select * into c from studyverse.parent_challenges where id = p_id and (parent_id = uid or child_id = uid) for update;
  if not found or not exists (select 1 from studyverse.parent_links where parent_id = c.parent_id and child_id = c.child_id) then
    return studyverse._sq_err('This challenge is not available.'); end if;
  if c.expires_at < now() then return studyverse._sq_err('This challenge has ended.'); end if;
  par := c.parent_id = uid;
  if (par and c.parent_score is not null) or (not par and c.child_score is not null) then return studyverse._sq_err('You already played this challenge.'); end if;
  if par and c.parent_started is null then update studyverse.parent_challenges set parent_started = now() where id = p_id returning * into c; end if;
  if not par and c.child_started is null then update studyverse.parent_challenges set child_started = now() where id = p_id returning * into c; end if;
  return jsonb_build_object('ok', true, 'challenge', studyverse._pc_view(c, par), 'questions', c.questions,
    'started_at', case when par then c.parent_started else c.child_started end, 'now', now());
end $$;

-- p_picks: the option index picked for each of the 5 questions (-1 = not answered). The server scores it and takes
-- the time from pc_start to now; then returns the right answers (and explanations) to this side.
create or replace function studyverse.pc_submit(p_id uuid, p_picks int[]) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c studyverse.parent_challenges; k studyverse.parent_challenge_answers; par boolean; sc int; ms int; st timestamptz;
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  select * into c from studyverse.parent_challenges where id = p_id and (parent_id = uid or child_id = uid) for update;
  if not found or not exists (select 1 from studyverse.parent_links where parent_id = c.parent_id and child_id = c.child_id) then
    return studyverse._sq_err('This challenge is not available.'); end if;
  if c.expires_at < now() then return studyverse._sq_err('This challenge has ended.'); end if;
  if p_picks is null or coalesce(array_length(p_picks, 1), 0) <> 5 or array_ndims(p_picks) <> 1
     or exists (select 1 from unnest(p_picks) x where x is null or x < -1 or x > 5) then
    return studyverse._sq_err('Send one answer for each of the 5 questions.'); end if;
  par := c.parent_id = uid;
  st := case when par then c.parent_started else c.child_started end;
  if st is null then return studyverse._sq_err('Open the challenge first.'); end if;
  if (par and c.parent_score is not null) or (not par and c.child_score is not null) then return studyverse._sq_err('You already played this challenge.'); end if;
  select * into k from studyverse.parent_challenge_answers where challenge_id = c.id;
  select count(*) into sc from generate_series(1, 5) i where p_picks[i] = k.answers[i];
  ms := least(greatest((extract(epoch from now() - st) * 1000)::int, 1000), 3600000);
  if par then
    update studyverse.parent_challenges set parent_picks = p_picks, parent_score = sc, parent_ms = ms, parent_at = now() where id = p_id returning * into c;
  else
    update studyverse.parent_challenges set child_picks = p_picks, child_score = sc, child_ms = ms, child_at = now() where id = p_id returning * into c;
  end if;
  return jsonb_build_object('ok', true, 'score', sc, 'ms', ms, 'answers', to_jsonb(k.answers), 'explains', k.explains,
                            'challenge', studyverse._pc_view(c, par));
end $$;

-- the parent's challenges with one child (newest first, last 14 days)
create or replace function studyverse.pc_list(p_child uuid) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare uid uuid := auth.uid();
begin
  if uid is null then return studyverse._sq_err('Please sign in first.'); end if;
  if not exists (select 1 from studyverse.parent_links where parent_id = uid and child_id = p_child) then
    return studyverse._sq_err('This child is not linked to you.'); end if;
  return jsonb_build_object('ok', true, 'challenges', coalesce((select jsonb_agg(studyverse._pc_view(c, true) order by c.created_at desc)
    from (select * from studyverse.parent_challenges where parent_id = uid and child_id = p_child and created_at > now() - interval '14 days'
          order by created_at desc limit 8) c), '[]'::jsonb));
end $$;

do $$ declare f text; begin
  foreach f in array array['squad_sync(jsonb, int, text, text, text, jsonb, text)', 'squad_home()', 'squad_add_friend(text)', 'squad_answer(uuid, boolean)',
    'squad_remove(uuid)', 'squad_cancel_requests()', 'squad_new_code()', 'squad_cheer(uuid, text)',
    'pc_create(uuid, text, text, jsonb)', 'pc_start(uuid)', 'pc_submit(uuid, int[])', 'pc_list(uuid)'] loop
    execute format('revoke all on function studyverse.%s from public, anon', f);
    execute format('grant execute on function studyverse.%s to authenticated', f);
  end loop;
end $$;

notify pgrst, 'reload schema';
