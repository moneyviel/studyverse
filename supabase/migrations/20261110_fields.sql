-- ============================================================================================
-- StudyVerse — strict contact fields on the server (pairs with js/fields.js).  Schema studyverse.
-- So bad data cannot get in, whatever the client sends:
--   PIN code : Indian PIN, ^[1-9][0-9]{5}$ (table check on institutions and pilot_requests)
--   phone    : stored as E.164 ^\+[1-9][0-9]{6,14}$; +91 numbers must be mobiles +91[6-9][0-9]{9}.
--              Friendly input is normalised first: "98765 43210", "098765-43210", "91 9876543210", "0091…" → +919876543210;
--              a number without + / 00 is taken as Indian (so 5876543210 is refused, not read as a foreign number).
--   email    : trimmed, lower case, a sensible name@domain.tld shape.
--   board    : CBSE / ICSE/ISC / "State board: <state>" / IB / Cambridge/IGCSE / NIOS / Other (free text up to 60 safe characters
--              is still accepted so older values keep working).
-- Changes (signatures unchanged, so the app and edge functions keep working):
--   _inst_details_ok(jsonb)  → also checks pincode, board, contact_phone, contact_email
--   inst_update_details, owner_create_institution → store the normalised phone / PIN / email
--   _pilot_request(jsonb, text) → checks + stores pincode and board (new nullable columns on pilot_requests)
-- Existing institution rows: a PIN code that is not 6 digits after removing spaces is cleared (the check needs it).
-- Idempotent: safe to run again. Run after 20261109_institutions.sql.
-- ============================================================================================

-- ---------- pure helpers ----------
create or replace function studyverse._fld_email_ok(p text) returns boolean language sql immutable set search_path = '' as $$
  select p is not null and length(p) <= 254
     and p ~ '^[a-z0-9._%+''-]+@[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*\.[a-z]{2,}$'
     and p !~ '(\.\.|^\.|\.@)' $$;

create or replace function studyverse._fld_pin_ok(p text) returns boolean language sql immutable set search_path = '' as $$
  select p is not null and p ~ '^[1-9][0-9]{5}$' $$;

-- friendly phone → E.164 candidate (may still be invalid: check with _fld_phone_ok). null for empty.
create or replace function studyverse._fld_phone_norm(p text) returns text language sql immutable set search_path = '' as $$
  select case
    when d is null then null
    when s ~ '^\+' then '+' || d
    when s ~ '^00' then '+' || substr(d, 3)
    when d ~ '^91[0-9]{10}$' then '+' || d                           -- 91 98765 43210
    else '+91' || regexp_replace(d, '^0+', '') end                     -- no country code = India (098765 43210 → +919876543210)
  from (select nullif(trim(coalesce(p, '')), '') s, nullif(regexp_replace(coalesce(p, ''), '[^0-9]', '', 'g'), '') d) x $$;

create or replace function studyverse._fld_phone_ok(p text) returns boolean language sql immutable set search_path = '' as $$
  select p is not null and p ~ '^\+[1-9][0-9]{6,14}$' and (p !~ '^\+91' or p ~ '^\+91[6-9][0-9]{9}$') $$;

create or replace function studyverse._fld_board_ok(p text) returns boolean language sql immutable set search_path = '' as $$
  select p is null or (length(p) between 2 and 60 and p ~ '^[A-Za-z0-9 &/().,:''-]+$') $$;

revoke all on function studyverse._fld_email_ok(text), studyverse._fld_pin_ok(text), studyverse._fld_phone_norm(text), studyverse._fld_phone_ok(text),
  studyverse._fld_board_ok(text) from public, anon;
grant execute on function studyverse._fld_email_ok(text), studyverse._fld_pin_ok(text), studyverse._fld_phone_norm(text), studyverse._fld_phone_ok(text),
  studyverse._fld_board_ok(text) to authenticated, service_role;

-- ---------- tables ----------
alter table studyverse.institutions add column if not exists pincode text;
alter table studyverse.institutions add column if not exists board text;
update studyverse.institutions set pincode = nullif(regexp_replace(pincode, '\s', '', 'g'), '') where pincode is not null and pincode <> regexp_replace(pincode, '\s', '', 'g');
update studyverse.institutions set pincode = null where pincode is not null and pincode !~ '^[1-9][0-9]{5}$';
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'institutions_pincode_chk') then
    alter table studyverse.institutions add constraint institutions_pincode_chk check (pincode is null or pincode ~ '^[1-9][0-9]{5}$');
  end if;
end $$;

alter table studyverse.pilot_requests add column if not exists pincode text;
alter table studyverse.pilot_requests add column if not exists board text;
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'pilot_requests_pincode_chk') then
    alter table studyverse.pilot_requests add constraint pilot_requests_pincode_chk check (pincode is null or pincode ~ '^[1-9][0-9]{5}$');
  end if;
  if not exists (select 1 from pg_constraint where conname = 'pilot_requests_board_chk') then
    alter table studyverse.pilot_requests add constraint pilot_requests_board_chk check (board is null or length(board) <= 60);
  end if;
end $$;

-- ---------- institution details (owner create + admin edit share this check) ----------
create or replace function studyverse._inst_details_ok(p jsonb) returns text language plpgsql immutable set search_path = '' as $$
declare ph text := studyverse._fld_phone_norm(p ->> 'contact_phone'); em text := lower(nullif(trim(p ->> 'contact_email'), ''));
  pin text := nullif(regexp_replace(coalesce(p ->> 'pincode', ''), '\s', '', 'g'), ''); bd text := nullif(trim(p ->> 'board'), '');
begin
  if p ? 'name' and length(trim(coalesce(p ->> 'name', ''))) < 2 then return 'Enter the institution name.'; end if;
  if coalesce(p ->> 'type', 'school') not in ('school', 'coaching') then return 'Type must be school or coaching.'; end if;
  if nullif(trim(p ->> 'gstin'), '') is not null and upper(trim(p ->> 'gstin')) !~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$' then return 'The GSTIN does not look right (15 characters, e.g. 27ABCDE1234F1Z5).'; end if;
  if em is not null and not studyverse._fld_email_ok(em) then return 'Please check the contact email (like name@school.com).'; end if;
  if ph is not null and not studyverse._fld_phone_ok(ph) then
    return case when ph ~ '^\+91' then 'Please check the mobile number: 10 digits starting with 6, 7, 8 or 9.' else 'Please check the phone number (with its country code).' end; end if;
  if pin is not null and not studyverse._fld_pin_ok(pin) then return 'The PIN code must be 6 digits and cannot start with 0.'; end if;
  if not studyverse._fld_board_ok(bd) then return 'Please choose the board from the list.'; end if;
  return null;
end $$;

create or replace function studyverse.inst_update_details(p_inst uuid, p jsonb) returns jsonb language plpgsql security definer set search_path = '' as $$
declare e text := studyverse._inst_details_ok(p);
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if e is not null then return jsonb_build_object('ok', false, 'msg', e); end if;
  update studyverse.institutions set
    name = coalesce(studyverse._inst_clean(p ->> 'name', 120), name), city = studyverse._inst_clean(p ->> 'city', 60), state = studyverse._inst_clean(p ->> 'state', 60),
    board = studyverse._inst_clean(p ->> 'board', 60), address = studyverse._inst_clean(p ->> 'address', 300),
    pincode = nullif(regexp_replace(coalesce(p ->> 'pincode', ''), '\s', '', 'g'), ''),
    gstin = upper(studyverse._inst_clean(p ->> 'gstin', 15)), contact_name = studyverse._inst_clean(p ->> 'contact_name', 80),
    contact_email = lower(studyverse._inst_clean(p ->> 'contact_email', 120)), contact_phone = studyverse._fld_phone_norm(p ->> 'contact_phone')
  where id = p_inst;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.owner_create_institution(p jsonb) returns jsonb language plpgsql security definer set search_path = '' as $$
declare e text := studyverse._inst_details_ok(p || jsonb_build_object('name', coalesce(p ->> 'name', ''))); nid uuid;
begin
  if not studyverse._inst_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  if e is not null then return jsonb_build_object('ok', false, 'msg', e); end if;
  insert into studyverse.institutions (name, type, city, state, board, address, pincode, gstin, contact_name, contact_email, contact_phone, status, created_by)
  values (studyverse._inst_clean(p ->> 'name', 120), coalesce(p ->> 'type', 'school'), studyverse._inst_clean(p ->> 'city', 60), studyverse._inst_clean(p ->> 'state', 60),
    studyverse._inst_clean(p ->> 'board', 60), studyverse._inst_clean(p ->> 'address', 300), nullif(regexp_replace(coalesce(p ->> 'pincode', ''), '\s', '', 'g'), ''),
    upper(studyverse._inst_clean(p ->> 'gstin', 15)), studyverse._inst_clean(p ->> 'contact_name', 80), lower(studyverse._inst_clean(p ->> 'contact_email', 120)),
    studyverse._fld_phone_norm(p ->> 'contact_phone'), 'pilot', auth.uid())
  returning id into nid;
  return jsonb_build_object('ok', true, 'id', nid);
end $$;

-- ---------- public "Request a free pilot" form (via edge function pilot-request) ----------
-- Fields are checked when given (the edge function makes name / phone / email / students / PIN / board required).
create or replace function studyverse._pilot_request(p jsonb, p_ip text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare ph text := studyverse._fld_phone_norm(p ->> 'phone'); em text := lower(nullif(trim(p ->> 'email'), ''));
  pin text := nullif(regexp_replace(coalesce(p ->> 'pincode', ''), '\s', '', 'g'), ''); bd text := nullif(trim(p ->> 'board'), '');
  st text := nullif(trim(coalesce(p ->> 'students', '')), '');
begin
  if (select count(*) from studyverse.pilot_requests where ip_hash = p_ip and created_at > now() - interval '1 hour') >= 3 then
    return jsonb_build_object('ok', false, 'code', 'limit', 'msg', 'We already have your request. We will call you soon.'); end if;
  if (select count(*) from studyverse.pilot_requests where created_at > now() - interval '1 day') >= 100 then
    return jsonb_build_object('ok', false, 'code', 'limit', 'msg', 'Please email support@moneyviel.com instead.'); end if;
  if ph is not null and not studyverse._fld_phone_ok(ph) then return jsonb_build_object('ok', false, 'code', 'bad', 'field', 'phone', 'msg', 'Please enter a valid mobile number.'); end if;
  if em is not null and not studyverse._fld_email_ok(em) then return jsonb_build_object('ok', false, 'code', 'bad', 'field', 'email', 'msg', 'Please enter a valid email, like name@school.com'); end if;
  if pin is not null and not studyverse._fld_pin_ok(pin) then return jsonb_build_object('ok', false, 'code', 'bad', 'field', 'pincode', 'msg', 'Please enter the 6-digit PIN code.'); end if;
  if not studyverse._fld_board_ok(bd) then return jsonb_build_object('ok', false, 'code', 'bad', 'field', 'board', 'msg', 'Please choose the board.'); end if;
  if st is not null and st !~ '^[0-9]{1,7}$' then return jsonb_build_object('ok', false, 'code', 'bad', 'field', 'students', 'msg', 'Please enter the number of students.'); end if;
  insert into studyverse.pilot_requests (name, school, city, phone, email, students, pincode, board, ip_hash)
  values (studyverse._inst_clean(p ->> 'name', 80), studyverse._inst_clean(p ->> 'school', 120), studyverse._inst_clean(p ->> 'city', 60),
          ph, em, least(greatest(coalesce(st::int, 0), 0), 1000000), pin, studyverse._inst_clean(bd, 60), p_ip);
  return jsonb_build_object('ok', true);
end $$;
revoke all on function studyverse._pilot_request(jsonb, text) from public, anon, authenticated;
grant execute on function studyverse._pilot_request(jsonb, text) to service_role;
