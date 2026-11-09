-- ============================================================================================
-- StudyVerse "Delete my account" — scope it to StudyVerse only.
-- The Supabase project is SHARED with other MoneyViel apps (schemas salonzy, football) that use the same auth.users.
-- Deleting the auth user would cascade into those apps' data. So:
--   1. studyverse._pr_wipe_studyverse(p_user): removes every StudyVerse row that points at the user (any single-column
--      FK from schema studyverse to auth.users: ON DELETE CASCADE → delete; SET NULL / NO ACTION → set null when the column
--      allows it, else delete). Payments were already anonymised by _pr_delete_user_data.
--   2. studyverse._pr_user_elsewhere(p_user): READ-ONLY check whether ANY table in another app schema (every schema except
--      studyverse and Supabase's own) holds this user's id in any uuid column. Nothing outside studyverse is changed.
-- The Edge Function delete-account deletes the auth user ONLY when _pr_user_elsewhere is false; otherwise it keeps the
-- shared login and the person's data in the other app, and StudyVerse data is gone.
-- Service role only. Idempotent.
-- ============================================================================================

create or replace function studyverse._pr_wipe_studyverse(p_user uuid) returns jsonb
language plpgsql security definer set search_path = '' as $$
declare r record; pass int; n int; total int := 0; left_ int;
begin
  if p_user is null then return jsonb_build_object('ok', false); end if;
  if exists (select 1 from studyverse.admins where user_id = p_user) then return jsonb_build_object('ok', false, 'msg', 'owner'); end if;
  for pass in 1..4 loop
    left_ := 0;
    for r in
      select c.relname tbl, a.attname col, con.confdeltype del, a.attnotnull nn
      from pg_constraint con
      join pg_class c on c.oid = con.conrelid
      join pg_namespace ns on ns.oid = c.relnamespace
      join pg_attribute a on a.attrelid = c.oid and a.attnum = con.conkey[1]
      where con.contype = 'f' and con.confrelid = 'auth.users'::regclass and ns.nspname = 'studyverse' and array_length(con.conkey, 1) = 1
      order by (con.confdeltype = 'c') , c.relname
    loop
      begin
        if r.del = 'c' or r.nn then
          execute format('delete from studyverse.%I where %I = $1', r.tbl, r.col) using p_user;
        else
          execute format('update studyverse.%I set %I = null where %I = $1', r.tbl, r.col, r.col) using p_user;
        end if;
        get diagnostics n = row_count; total := total + n;
      exception when others then left_ := left_ + 1;      -- another row still points at it: retry next pass
      end;
    end loop;
    exit when left_ = 0;
  end loop;
  return jsonb_build_object('ok', left_ = 0, 'rows', total, 'stuck', left_);
end $$;

create or replace function studyverse._pr_user_elsewhere(p_user uuid) returns boolean
language plpgsql security definer set search_path = '' as $$
declare r record; hit boolean;
begin
  if p_user is null then return false; end if;
  for r in
    select ns.nspname sch, c.relname tbl, a.attname col
    from pg_attribute a
    join pg_class c on c.oid = a.attrelid and c.relkind = 'r'
    join pg_namespace ns on ns.oid = c.relnamespace
    where a.atttypid = 'uuid'::regtype and a.attnum > 0 and not a.attisdropped
      and ns.nspname not like 'pg\_%' and ns.nspname not in ('studyverse', 'auth', 'storage', 'extensions', 'graphql', 'graphql_public',
        'realtime', '_realtime', 'supabase_functions', 'supabase_migrations', 'vault', 'net', 'cron', 'pgbouncer', 'pgsodium',
        'pgsodium_masks', '_analytics', 'information_schema', 'public')
  loop
    execute format('select exists (select 1 from %I.%I where %I = $1)', r.sch, r.tbl, r.col) into hit using p_user;
    if hit then return true; end if;
  end loop;
  return false;
end $$;

revoke all on function studyverse._pr_wipe_studyverse(uuid) from public, anon, authenticated;
revoke all on function studyverse._pr_user_elsewhere(uuid) from public, anon, authenticated;
grant execute on function studyverse._pr_wipe_studyverse(uuid) to service_role;
grant execute on function studyverse._pr_user_elsewhere(uuid) to service_role;
notify pgrst, 'reload schema';
