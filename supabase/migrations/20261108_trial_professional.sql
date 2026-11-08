-- 24-hour trial covers school AND professional courses (CA Foundation now). Applied to project moneyviel-apps.
create or replace function studyverse.start_trial() returns jsonb language plpgsql security definer set search_path = '' as $function$
declare uid uuid := auth.uid(); t timestamptz; c text;
begin
  if uid is null then return jsonb_build_object('ok', false); end if;
  select trial_at into t from studyverse.profiles where user_id = uid;
  if t is null then
    insert into studyverse.profiles(user_id, trial_at) values (uid, now())
      on conflict (user_id) do update set trial_at = coalesce(studyverse.profiles.trial_at, now());
    t := now();
  end if;
  if t > now() - interval '24 hours' then
    foreach c in array array['school-all', 'ca-foundation'] loop
      insert into studyverse.course_access(user_id, course, valid_until, note) values (uid, c, t + interval '24 hours', 'trial')
        on conflict (user_id, course) do nothing;
    end loop;
  end if;
  return jsonb_build_object('ok', true, 'started', t);
end $function$;
