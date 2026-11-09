-- Knowtopia Pulse: leave out logins that belong only to the owner's other apps (Salonzy, Football Club).
-- The Supabase project is shared, so auth.users also holds people who never used Knowtopia. A login counts as
-- "other app only" when studyverse._pr_user_elsewhere() finds it in another app's schema AND it has no Knowtopia
-- footprint at all (profile, saved progress, course access, consents, parent links). Such logins are hidden from
-- every Pulse view, even with "Show test accounts" on. Read-only for user data; idempotent.
begin;

create or replace function studyverse._od_other_app(u uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select studyverse._pr_user_elsewhere(u)
     and not exists (select 1 from studyverse.profiles x where x.user_id = u)
     and not exists (select 1 from studyverse.progress x where x.user_id = u)
     and not exists (select 1 from studyverse.course_access x where x.user_id = u)
     and not exists (select 1 from studyverse.consents x where x.subject_id = u or x.actor_id = u)
     and not exists (select 1 from studyverse.parent_links x where x.parent_id = u or x.child_id = u) $$;
revoke all on function studyverse._od_other_app(uuid) from public, anon, authenticated;

create or replace function studyverse._od_test_user(u uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from auth.users x where x.id = u and (studyverse._od_test_email(x.email) or coalesce(x.raw_user_meta_data ->> 'demo', '') in ('true', '1')))
      or exists (select 1 from studyverse.progress pr where pr.user_id = u and pr.state #>> '{st,profile,name}' = 'Demo Student')
      or studyverse._od_other_app(u) $$;

-- patch the live student list (_od_users) in place: add the filter right before the test-account filter
do $p$
declare d text; marker text := '-- test / demo accounts are hidden unless p.test is true';
begin
  select pg_get_functiondef('studyverse._od_users(jsonb)'::regprocedure) into d;
  if position('_od_other_app' in d) > 0 then return; end if;
  if (length(d) - length(replace(d, marker, ''))) / length(marker) <> 1 then raise exception 'marker not found exactly once'; end if;
  d := replace(d, marker, '-- logins used only by other MoneyViel apps are never Knowtopia users
      and not studyverse._od_other_app(u.id)
      ' || marker);
  execute d;
end $p$;

commit;
