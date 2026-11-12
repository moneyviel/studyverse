-- Owner gives / takes back a course for one student from Pulse → Students → (student) → 🔑 Access.
-- Courses: jee · ca-foundation · ca-inter · ca-final · school-g1 … school-g12. Days 1–3650 or no end date.
-- A gift extends from the later of now and the current end date; a paid row keeps its "paid" note.
-- Take-back removes only rows the owner gave (note = 'gift'); paid plans and school seats are never touched here.
create or replace function studyverse.owner_give_course(p_user uuid, p_course text, p_days int default null) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare cur studyverse.course_access%rowtype; base timestamptz; until timestamptz;
begin
  if not studyverse._od_is_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  if p_course is null or p_course !~ '^(jee|ca-(foundation|inter|final)|school-g([1-9]|1[0-2]))$' then return jsonb_build_object('ok', false, 'msg', 'Unknown course.'); end if;
  if p_days is not null and (p_days < 1 or p_days > 3650) then return jsonb_build_object('ok', false, 'msg', 'Days must be 1 to 3650.'); end if;
  if not exists (select 1 from auth.users where id = p_user) then return jsonb_build_object('ok', false, 'msg', 'Student not found.'); end if;
  select * into cur from studyverse.course_access where user_id = p_user and course = p_course;
  if found and cur.valid_until is null then return jsonb_build_object('ok', true, 'valid_until', null, 'msg', 'Already has this course with no end date.'); end if;
  base := greatest(now(), coalesce(cur.valid_until, now()));
  until := case when p_days is null then null else base + make_interval(days => p_days) end;
  insert into studyverse.course_access(user_id, course, valid_until, note) values (p_user, p_course, until, 'gift')
  on conflict (user_id, course) do update set valid_until = excluded.valid_until,
    note = case when studyverse.course_access.note like 'paid%' then studyverse.course_access.note else 'gift' end, granted_at = now();
  return jsonb_build_object('ok', true, 'valid_until', until);
end $$;

create or replace function studyverse.owner_take_course(p_user uuid, p_course text) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if not studyverse._od_is_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  delete from studyverse.course_access where user_id = p_user and course = p_course and note = 'gift';
  get diagnostics n = row_count;
  return jsonb_build_object('ok', n > 0, 'msg', case when n > 0 then 'Removed.' else 'Only courses you gave can be removed here (paid plans and school seats stay).' end);
end $$;

revoke all on function studyverse.owner_give_course(uuid, text, int) from public, anon;
revoke all on function studyverse.owner_take_course(uuid, text) from public, anon;
grant execute on function studyverse.owner_give_course(uuid, text, int) to authenticated;
grant execute on function studyverse.owner_take_course(uuid, text) to authenticated;
