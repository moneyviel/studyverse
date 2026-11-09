-- ============================================================================================
-- StudyVerse for Schools & Coaching (B2B) — schema studyverse.
-- Institutions (school | coaching) with admins, teachers and students; classes / sections / CA batches;
-- class-specific join codes (multi-use class codes, single-use roll-number codes, teacher codes);
-- seat orders priced per student per month, billed as 10 months per academic year (Apr–Mar):
--     Class 1–5 ₹100 · 6–8 ₹125 · 9–10 ₹175 · 11–12 ₹225 · CA Foundation coaching ₹250   (+ GST as applicable)
--     volume discount on the whole order: 100+ students 10% · 500+ 20% · 1000+ 30% · minimum 30 students.
-- Free 30-day pilot for ONE class (owner grants). Seats become course_access rows (note 'inst <id>').
-- A paid / free-forever course a student already has is NEVER shortened or overwritten; when a school seat ends
-- the student's earlier row is put back. School enrolment never touches parent_links (Parent Hub keeps working).
-- RLS: owner (studyverse.is_admin()) sees all; institution admins see their institution; teachers see only their
-- classes; students see their own rows. Every change goes through the SECURITY DEFINER functions below.
-- Functions named _inst_* / _pilot_* are for the service role only (edge functions institution-bulk,
-- institution-notify, pilot-request) and take the CALLER's id, which they check.
-- Needs (already in the project): auth.users, studyverse.profiles, course_access, progress, parent_links, admins, is_admin().
-- Idempotent: safe to run again.
-- ============================================================================================

-- ---------- tables ----------
create table if not exists studyverse.institutions (
  id            uuid primary key default gen_random_uuid(),
  name          text not null check (length(trim(name)) between 2 and 120),
  type          text not null default 'school' check (type in ('school', 'coaching')),
  city          text, state text, board text, address text, pincode text,
  gstin         text check (gstin is null or gstin ~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'),
  contact_name  text, contact_email text, contact_phone text,
  status        text not null default 'pilot' check (status in ('pilot', 'active', 'expired')),
  pilot_until   timestamptz,
  pilot_class_id uuid,
  created_by    uuid references auth.users(id) on delete set null,
  created_at    timestamptz not null default now()
);

-- one row = one class-section (school) or one batch (coaching)
create table if not exists studyverse.inst_classes (
  id             uuid primary key default gen_random_uuid(),
  institution_id uuid not null references studyverse.institutions(id) on delete cascade,
  kind           text not null default 'class' check (kind in ('class', 'batch')),
  grade          int check (grade between 1 and 12),
  section        text not null default 'A' check (length(section) between 1 and 40),
  course         text not null check (course ~ '^school-g([1-9]|1[0-2])$' or course = 'ca-foundation'),
  name           text not null,
  created_at     timestamptz not null default now(),
  unique (institution_id, course, section)
);
create index if not exists inst_classes_inst on studyverse.inst_classes (institution_id);
do $$ begin
  if not exists (select 1 from pg_constraint where conname = 'institutions_pilot_class_fk') then
    alter table studyverse.institutions add constraint institutions_pilot_class_fk foreign key (pilot_class_id) references studyverse.inst_classes(id) on delete set null;
  end if;
end $$;

create table if not exists studyverse.institution_members (
  institution_id uuid not null references studyverse.institutions(id) on delete cascade,
  user_id        uuid not null references auth.users(id) on delete cascade,
  role           text not null check (role in ('admin', 'teacher', 'student')),
  class_id       uuid references studyverse.inst_classes(id) on delete set null,   -- students: their class / batch
  roll_no        text,
  display_name   text,
  lb_opt         boolean not null default false,                                    -- students: show my first name on the class leaderboard
  joined_at      timestamptz not null default now(),
  primary key (institution_id, user_id, role)
);
create index if not exists inst_members_user on studyverse.institution_members (user_id);
create index if not exists inst_members_class on studyverse.institution_members (class_id) where role = 'student';

create table if not exists studyverse.teacher_classes (
  class_id uuid not null references studyverse.inst_classes(id) on delete cascade,
  user_id  uuid not null references auth.users(id) on delete cascade,
  primary key (class_id, user_id)
);
create index if not exists teacher_classes_user on studyverse.teacher_classes (user_id);

create table if not exists studyverse.join_codes (
  code           text primary key check (code ~ '^[A-Z0-9]{8}$'),
  institution_id uuid not null references studyverse.institutions(id) on delete cascade,
  class_id       uuid references studyverse.inst_classes(id) on delete cascade,
  role           text not null check (role in ('student', 'teacher')),
  roll_no        text, display_name text,                -- roll-number codes (from bulk upload): one student, single use
  max_uses       int not null default 200 check (max_uses between 1 and 2000),
  used           int not null default 0,
  active         boolean not null default true,
  expires_at     timestamptz not null default now() + interval '30 days',
  created_by     uuid references auth.users(id) on delete set null,
  created_at     timestamptz not null default now(),
  check (role = 'teacher' or class_id is not null)
);
create index if not exists join_codes_inst on studyverse.join_codes (institution_id, created_at desc);

create table if not exists studyverse.inst_rates (
  band  text primary key check (band in ('1-5', '6-8', '9-10', '11-12', 'ca')),
  label text not null, rate int not null check (rate > 0), sort int not null
);
insert into studyverse.inst_rates (band, label, rate, sort) values
  ('1-5', 'Class 1–5', 100, 1), ('6-8', 'Class 6–8', 125, 2), ('9-10', 'Class 9–10', 175, 3),
  ('11-12', 'Class 11–12', 225, 4), ('ca', 'CA Foundation coaching', 250, 5)
on conflict (band) do update set label = excluded.label, rate = excluded.rate, sort = excluded.sort;

-- seller details printed on invoices; GST is charged only once the owner sets a GSTIN here
create table if not exists studyverse.billing_config (
  id             int primary key default 1 check (id = 1),
  seller_name    text not null default 'MoneyViel',
  legal_name     text not null default 'Mukesh Jhedu',
  address        text not null default 'Pune, Maharashtra, India',
  city           text not null default 'Pune',
  state          text not null default 'Maharashtra',
  gstin          text check (gstin is null or gstin ~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'),
  email          text not null default 'support@moneyviel.com',
  invoice_prefix text not null default 'SV-',
  next_no        int not null default 1,
  updated_at     timestamptz not null default now()
);
insert into studyverse.billing_config (id) values (1) on conflict do nothing;

create table if not exists studyverse.seat_orders (
  id             uuid primary key default gen_random_uuid(),
  institution_id uuid not null references studyverse.institutions(id) on delete cascade,
  lines          jsonb not null,          -- [{band, label, students, rate, months, amount}]
  students       int not null,
  months         int not null default 10 check (months = 10),
  subtotal       numeric(14,2) not null,
  discount_pct   int not null default 0,
  discount_amt   numeric(14,2) not null default 0,
  taxable        numeric(14,2) not null,
  gst            jsonb not null,          -- {mode:'none'|'intra'|'inter', cgst, sgst, igst, amount, note}
  total          numeric(14,2) not null,
  academic_year  text not null check (academic_year ~ '^20[0-9]{2}-[0-9]{2}$'),
  valid_until    timestamptz not null,
  status         text not null default 'draft' check (status in ('draft', 'invoiced', 'paid', 'cancelled')),
  invoice_no     text unique,
  seller         jsonb, buyer jsonb,      -- snapshots for the printed invoice
  payment_ref    text,
  created_by     uuid references auth.users(id) on delete set null,
  created_at     timestamptz not null default now(),
  invoiced_at    timestamptz, paid_at timestamptz, mailed_at timestamptz
);
create index if not exists seat_orders_inst on studyverse.seat_orders (institution_id, created_at desc);

-- which school seat each student holds, and what course_access row they had before (put back when the seat ends)
create table if not exists studyverse.inst_grants (
  institution_id   uuid not null references studyverse.institutions(id) on delete cascade,
  user_id          uuid not null references auth.users(id) on delete cascade,
  course           text not null,
  band             text not null,
  valid_until      timestamptz not null,
  pilot            boolean not null default false,
  had_prev         boolean not null default false,
  prev_valid_until timestamptz, prev_note text,
  granted_at       timestamptz not null default now(),
  primary key (institution_id, user_id, course)
);

create table if not exists studyverse.homework (
  id             uuid primary key default gen_random_uuid(),
  institution_id uuid not null references studyverse.institutions(id) on delete cascade,
  class_id       uuid not null references studyverse.inst_classes(id) on delete cascade,
  kind           text not null check (kind in ('chapter', 'quiz', 'mcq')),
  target         text not null check (target ~ '^([0-9]{1,2}-[a-z]+-[0-9]{1,3}|[a-z]{3}-p[0-9]+-ch[0-9]+(-u[0-9]+)?)$'),
  title          text not null check (length(title) between 1 and 160),
  subject        text,
  need           int not null default 3 check (need between 1 and 50),
  due_date       date not null,
  created_by     uuid references auth.users(id) on delete set null,
  created_at     timestamptz not null default now()
);
create index if not exists homework_class on studyverse.homework (class_id, due_date desc);
create table if not exists studyverse.hw_done (
  homework_id uuid not null references studyverse.homework(id) on delete cascade,
  user_id     uuid not null references auth.users(id) on delete cascade,
  done_at     timestamptz not null default now(),
  primary key (homework_id, user_id)
);

-- parent emails given by the school: linked when that parent signs in (proves the email) — see inst_claim()
create table if not exists studyverse.inst_parent_invites (
  id             uuid primary key default gen_random_uuid(),
  institution_id uuid not null references studyverse.institutions(id) on delete cascade,
  email          text not null,
  child_id       uuid references auth.users(id) on delete cascade,
  join_code      text,                    -- roll-number code: child_id is filled when the student uses it
  student_email  text,                    -- student invited by email: child_id is filled when the account is made
  child_name     text,
  created_at     timestamptz not null default now(),
  accepted_at    timestamptz
);
create index if not exists inst_pinv_email on studyverse.inst_parent_invites (email) where accepted_at is null;

create table if not exists studyverse.inst_bulk_log (id bigint generated always as identity primary key, institution_id uuid not null, caller uuid, rows int not null, emails int not null default 0, at timestamptz not null default now());
create table if not exists studyverse.pilot_requests (
  id bigint generated always as identity primary key, name text, school text, city text, phone text, email text, students int,
  ip_hash text, created_at timestamptz not null default now());

-- ---------- RLS ----------
alter table studyverse.institutions enable row level security;
alter table studyverse.inst_classes enable row level security;
alter table studyverse.institution_members enable row level security;
alter table studyverse.teacher_classes enable row level security;
alter table studyverse.join_codes enable row level security;
alter table studyverse.inst_rates enable row level security;
alter table studyverse.billing_config enable row level security;
alter table studyverse.seat_orders enable row level security;
alter table studyverse.inst_grants enable row level security;
alter table studyverse.homework enable row level security;
alter table studyverse.hw_done enable row level security;
alter table studyverse.inst_parent_invites enable row level security;   -- no policies: functions only
alter table studyverse.inst_bulk_log enable row level security;         -- no policies
alter table studyverse.pilot_requests enable row level security;        -- no policies

-- helpers (SECURITY DEFINER so policies do not recurse)
create or replace function studyverse._inst_owner() returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.admins where user_id = auth.uid()) $$;
create or replace function studyverse.inst_is_admin(p_inst uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select studyverse._inst_owner() or exists (select 1 from studyverse.institution_members m where m.institution_id = p_inst and m.user_id = auth.uid() and m.role = 'admin') $$;
create or replace function studyverse.inst_member(p_inst uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select studyverse._inst_owner() or exists (select 1 from studyverse.institution_members m where m.institution_id = p_inst and m.user_id = auth.uid()) $$;
create or replace function studyverse.inst_teaches(p_class uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.teacher_classes t where t.class_id = p_class and t.user_id = auth.uid())
      or exists (select 1 from studyverse.inst_classes c where c.id = p_class and studyverse.inst_is_admin(c.institution_id)) $$;
create or replace function studyverse.inst_in_class(p_class uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.institution_members m where m.class_id = p_class and m.user_id = auth.uid() and m.role = 'student') $$;
-- service-side check: may this user manage this institution? (owner or institution admin)
create or replace function studyverse._inst_can_manage(p_inst uuid, p_user uuid) returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from studyverse.admins where user_id = p_user)
      or exists (select 1 from studyverse.institution_members m where m.institution_id = p_inst and m.user_id = p_user and m.role = 'admin') $$;
revoke all on function studyverse._inst_owner(), studyverse.inst_is_admin(uuid), studyverse.inst_member(uuid), studyverse.inst_teaches(uuid), studyverse.inst_in_class(uuid) from public, anon;
grant execute on function studyverse._inst_owner(), studyverse.inst_is_admin(uuid), studyverse.inst_member(uuid), studyverse.inst_teaches(uuid), studyverse.inst_in_class(uuid) to authenticated, service_role;
revoke all on function studyverse._inst_can_manage(uuid, uuid) from public, anon, authenticated;
grant execute on function studyverse._inst_can_manage(uuid, uuid) to service_role;

drop policy if exists inst_read on studyverse.institutions;
create policy inst_read on studyverse.institutions for select to authenticated using ((select studyverse.inst_member(id)));
drop policy if exists inst_classes_read on studyverse.inst_classes;
create policy inst_classes_read on studyverse.inst_classes for select to authenticated
  using ((select studyverse.inst_is_admin(institution_id)) or (select studyverse.inst_teaches(id)) or (select studyverse.inst_in_class(id)));
drop policy if exists inst_members_read on studyverse.institution_members;
create policy inst_members_read on studyverse.institution_members for select to authenticated
  using (user_id = (select auth.uid()) or (select studyverse.inst_is_admin(institution_id)) or (role = 'student' and class_id is not null and (select studyverse.inst_teaches(class_id))));
drop policy if exists teacher_classes_read on studyverse.teacher_classes;
create policy teacher_classes_read on studyverse.teacher_classes for select to authenticated using (user_id = (select auth.uid()) or (select studyverse.inst_teaches(class_id)));
drop policy if exists join_codes_read on studyverse.join_codes;
create policy join_codes_read on studyverse.join_codes for select to authenticated
  using ((select studyverse.inst_is_admin(institution_id)) or (role = 'student' and class_id is not null and (select studyverse.inst_teaches(class_id))));
drop policy if exists inst_rates_read on studyverse.inst_rates;
create policy inst_rates_read on studyverse.inst_rates for select to anon, authenticated using (true);
drop policy if exists billing_read on studyverse.billing_config;
create policy billing_read on studyverse.billing_config for select to authenticated using (true);
drop policy if exists seat_orders_read on studyverse.seat_orders;
create policy seat_orders_read on studyverse.seat_orders for select to authenticated using ((select studyverse.inst_is_admin(institution_id)));
drop policy if exists inst_grants_read on studyverse.inst_grants;
create policy inst_grants_read on studyverse.inst_grants for select to authenticated using (user_id = (select auth.uid()) or (select studyverse.inst_is_admin(institution_id)));
drop policy if exists homework_read on studyverse.homework;
create policy homework_read on studyverse.homework for select to authenticated using ((select studyverse.inst_in_class(class_id)) or (select studyverse.inst_teaches(class_id)));
drop policy if exists hw_done_read on studyverse.hw_done;
create policy hw_done_read on studyverse.hw_done for select to authenticated
  using (user_id = (select auth.uid()) or exists (select 1 from studyverse.homework h where h.id = homework_id and (select studyverse.inst_teaches(h.class_id))));

grant select on studyverse.institutions, studyverse.inst_classes, studyverse.institution_members, studyverse.teacher_classes, studyverse.join_codes,
  studyverse.billing_config, studyverse.seat_orders, studyverse.inst_grants, studyverse.homework, studyverse.hw_done to authenticated;
grant select on studyverse.inst_rates to anon, authenticated;
grant all on studyverse.institutions, studyverse.inst_classes, studyverse.institution_members, studyverse.teacher_classes, studyverse.join_codes, studyverse.inst_rates,
  studyverse.billing_config, studyverse.seat_orders, studyverse.inst_grants, studyverse.homework, studyverse.hw_done, studyverse.inst_parent_invites,
  studyverse.inst_bulk_log, studyverse.pilot_requests to service_role;

-- ---------- pure helpers: band, academic year, price ----------
create or replace function studyverse._inst_band(p_course text) returns text language sql immutable set search_path = '' as $$
  select case when p_course = 'ca-foundation' then 'ca'
    when p_course ~ '^school-g([1-9]|1[0-2])$' then
      case when substr(p_course, 9)::int <= 5 then '1-5' when substr(p_course, 9)::int <= 8 then '6-8' when substr(p_course, 9)::int <= 10 then '9-10' else '11-12' end
    else null end $$;
-- academic year 'YYYY-YY' runs 1 April – 31 March (India); seats end 31 March 23:59:59 IST
create or replace function studyverse._inst_ay(p_at timestamptz) returns text language sql immutable set search_path = '' as $$
  select case when extract(month from (p_at at time zone 'Asia/Kolkata')) >= 4
    then extract(year from (p_at at time zone 'Asia/Kolkata'))::int::text || '-' || lpad(((extract(year from (p_at at time zone 'Asia/Kolkata'))::int + 1) % 100)::text, 2, '0')
    else (extract(year from (p_at at time zone 'Asia/Kolkata'))::int - 1)::text || '-' || lpad((extract(year from (p_at at time zone 'Asia/Kolkata'))::int % 100)::text, 2, '0') end $$;
create or replace function studyverse._inst_ay_end(p_ay text) returns timestamptz language sql immutable set search_path = '' as $$
  select (make_timestamp(substr(p_ay, 1, 4)::int + 1, 3, 31, 23, 59, 59) at time zone 'Asia/Kolkata') $$;

-- the price of an order. p_lines: [{band:'1-5'|'6-8'|'9-10'|'11-12'|'ca', students:n}, …] (same band twice is added up)
-- rate × students × 10 months per line; volume discount on the whole order; GST only when billing_config.gstin is set:
-- buyer in the seller's state → CGST 9% + SGST 9%, otherwise IGST 18%.
create or replace function studyverse._inst_price(p_lines jsonb, p_buyer_state text) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare cfg studyverse.billing_config%rowtype; items jsonb := '[]'::jsonb; r record; n int := 0; sub numeric := 0; pct int; disc numeric; tax numeric; g jsonb; half numeric;
begin
  if p_lines is null or jsonb_typeof(p_lines) <> 'array' or jsonb_array_length(p_lines) = 0 then
    return jsonb_build_object('ok', false, 'code', 'empty', 'msg', 'Add the number of students for at least one class group.'); end if;
  if exists (select 1 from jsonb_array_elements(p_lines) l where coalesce(l ->> 'band', '') not in (select band from studyverse.inst_rates)
               or coalesce(l ->> 'students', '') !~ '^[0-9]{1,6}$') then
    return jsonb_build_object('ok', false, 'code', 'bad', 'msg', 'Please check the class groups and student numbers.'); end if;
  for r in select x.band, x.label, x.rate, sum((l ->> 'students')::int)::int st
             from jsonb_array_elements(p_lines) l join studyverse.inst_rates x on x.band = l ->> 'band'
            group by x.band, x.label, x.rate, x.sort having sum((l ->> 'students')::int) > 0 order by x.sort loop
    items := items || jsonb_build_object('band', r.band, 'label', r.label, 'students', r.st, 'rate', r.rate, 'months', 10, 'amount', r.st * r.rate * 10);
    n := n + r.st; sub := sub + r.st * r.rate * 10;
  end loop;
  if n < 30 then return jsonb_build_object('ok', false, 'code', 'min', 'students', n, 'msg', 'The minimum order is 30 students (you have ' || n || ').'); end if;
  if n > 100000 then return jsonb_build_object('ok', false, 'code', 'bad', 'msg', 'Please contact us for orders above 1,00,000 students.'); end if;
  pct := case when n >= 1000 then 30 when n >= 500 then 20 when n >= 100 then 10 else 0 end;
  disc := round(sub * pct / 100.0, 2); tax := sub - disc;
  select * into cfg from studyverse.billing_config where id = 1;
  if cfg.gstin is null then
    g := jsonb_build_object('mode', 'none', 'cgst', 0, 'sgst', 0, 'igst', 0, 'amount', 0, 'note', 'GST: not charged — supplier not registered under GST');
  elsif lower(trim(coalesce(p_buyer_state, ''))) = lower(trim(cfg.state)) then
    half := round(tax * 0.09, 2);
    g := jsonb_build_object('mode', 'intra', 'cgst', half, 'sgst', half, 'igst', 0, 'amount', half * 2, 'note', 'CGST 9% + SGST 9% (place of supply: ' || cfg.state || ')');
  else
    g := jsonb_build_object('mode', 'inter', 'cgst', 0, 'sgst', 0, 'igst', round(tax * 0.18, 2), 'amount', round(tax * 0.18, 2),
      'note', 'IGST 18% (place of supply: ' || coalesce(nullif(trim(p_buyer_state), ''), 'not given') || ')');
  end if;
  return jsonb_build_object('ok', true, 'lines', items, 'students', n, 'months', 10, 'subtotal', sub, 'discount_pct', pct, 'discount_amt', disc,
    'taxable', tax, 'gst', g, 'total', tax + (g ->> 'amount')::numeric, 'per_student_month', round(tax / n / 10, 2));
end $$;
revoke all on function studyverse._inst_price(jsonb, text) from public, anon;
grant execute on function studyverse._inst_price(jsonb, text) to authenticated, service_role;

-- live quote for the order builder (and the pricing page when signed in). p_inst gives the buyer's state for GST.
create or replace function studyverse.quote_order(p_lines jsonb, p_inst uuid default null) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare st text;
begin
  if auth.uid() is null then return jsonb_build_object('ok', false, 'msg', 'Please sign in first.'); end if;
  if p_inst is not null then
    if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
    select state into st from studyverse.institutions where id = p_inst;
  end if;
  return studyverse._inst_price(p_lines, st);
end $$;
revoke all on function studyverse.quote_order(jsonb, uuid) from public, anon;
grant execute on function studyverse.quote_order(jsonb, uuid) to authenticated;

-- ---------- seats → course_access ----------
create or replace function studyverse._inst_grant(p_inst uuid, p_user uuid, p_course text, p_until timestamptz, p_pilot boolean) returns void language plpgsql security definer set search_path = '' as $$
declare prev studyverse.course_access%rowtype; had boolean; g studyverse.inst_grants%rowtype; tag text := 'inst ' || p_inst;
begin
  select * into prev from studyverse.course_access where user_id = p_user and course = p_course;
  had := found;
  select * into g from studyverse.inst_grants where institution_id = p_inst and user_id = p_user and course = p_course;
  if not found then
    insert into studyverse.inst_grants (institution_id, user_id, course, band, valid_until, pilot, had_prev, prev_valid_until, prev_note)
    values (p_inst, p_user, p_course, studyverse._inst_band(p_course), p_until, p_pilot,
            had and coalesce(prev.note, '') not like 'inst %', case when had and coalesce(prev.note, '') not like 'inst %' then prev.valid_until end,
            case when had and coalesce(prev.note, '') not like 'inst %' then prev.note end);
  else
    update studyverse.inst_grants set valid_until = p_until, pilot = p_pilot where institution_id = p_inst and user_id = p_user and course = p_course;
  end if;
  -- keep the student's own longer (or free-forever) row; a trial or another school's row is replaced by a longer seat
  if had and coalesce(prev.note, '') <> tag and coalesce(prev.note, '') <> 'trial'
     and (prev.valid_until is null or prev.valid_until >= p_until) then return; end if;
  if had and coalesce(prev.note, '') like 'inst %' and prev.note <> tag and prev.valid_until >= p_until then return; end if;
  insert into studyverse.course_access (user_id, course, valid_until, note) values (p_user, p_course, p_until, tag)
    on conflict (user_id, course) do update set valid_until = excluded.valid_until, note = excluded.note, granted_at = now();
end $$;

create or replace function studyverse._inst_revoke(p_inst uuid, p_user uuid, p_course text) returns void language plpgsql security definer set search_path = '' as $$
declare g studyverse.inst_grants%rowtype; tag text := 'inst ' || p_inst;
begin
  select * into g from studyverse.inst_grants where institution_id = p_inst and user_id = p_user and course = p_course;
  if not found then return; end if;
  if exists (select 1 from studyverse.course_access where user_id = p_user and course = p_course and note = tag) then
    if g.had_prev and coalesce(g.prev_note, '') <> 'trial' and (g.prev_valid_until is null or g.prev_valid_until > now()) then
      update studyverse.course_access set valid_until = g.prev_valid_until, note = g.prev_note where user_id = p_user and course = p_course;
    else
      delete from studyverse.course_access where user_id = p_user and course = p_course and note = tag;
    end if;
  end if;
  delete from studyverse.inst_grants where institution_id = p_inst and user_id = p_user and course = p_course;
end $$;

-- recompute seats for one institution (or one student in it). Paid seats per band go to the earliest-joined students;
-- the pilot class gets access till pilot_until without using seats. Also keeps institutions.status in step.
create or replace function studyverse._inst_sync(p_inst uuid, p_user uuid default null) returns void language plpgsql security definer set search_path = '' as $$
declare i studyverse.institutions%rowtype; r record; tot int; ou timestamptz; until timestamptz; pil boolean;
begin
  select * into i from studyverse.institutions where id = p_inst; if not found then return; end if;
  -- seats a student no longer qualifies for (left the class, changed class) are released first
  for r in select g.user_id, g.course from studyverse.inst_grants g where g.institution_id = p_inst and (p_user is null or g.user_id = p_user)
             and not exists (select 1 from studyverse.institution_members m join studyverse.inst_classes c on c.id = m.class_id
                             where m.institution_id = p_inst and m.user_id = g.user_id and m.role = 'student' and c.course = g.course) loop
    perform studyverse._inst_revoke(p_inst, r.user_id, r.course);
  end loop;
  for r in select * from (
             select m.user_id, m.class_id, c.course, studyverse._inst_band(c.course) band,
                    row_number() over (partition by studyverse._inst_band(c.course) order by m.joined_at, m.user_id) rn
               from studyverse.institution_members m join studyverse.inst_classes c on c.id = m.class_id
              where m.institution_id = p_inst and m.role = 'student') x
           where p_user is null or x.user_id = p_user loop
    until := null; pil := false;
    if i.pilot_class_id = r.class_id and i.pilot_until > now() then until := i.pilot_until; pil := true; end if;
    select coalesce(sum((l ->> 'students')::int), 0), max(o.valid_until) into tot, ou
      from studyverse.seat_orders o, jsonb_array_elements(o.lines) l
     where o.institution_id = p_inst and o.status = 'paid' and o.valid_until > now() and l ->> 'band' = r.band;
    if r.rn <= tot and (until is null or ou > until) then until := ou; pil := false; end if;
    if until is not null then perform studyverse._inst_grant(p_inst, r.user_id, r.course, until, pil);
    else perform studyverse._inst_revoke(p_inst, r.user_id, r.course); end if;
  end loop;
  update studyverse.institutions set status = case
      when exists (select 1 from studyverse.seat_orders o where o.institution_id = p_inst and o.status = 'paid' and o.valid_until > now()) then 'active'
      when pilot_until > now() then 'pilot'
      when pilot_until is null and status = 'pilot' then 'pilot'
      else 'expired' end
   where id = p_inst;
end $$;
revoke all on function studyverse._inst_grant(uuid, uuid, text, timestamptz, boolean), studyverse._inst_revoke(uuid, uuid, text), studyverse._inst_sync(uuid, uuid) from public, anon, authenticated;
grant execute on function studyverse._inst_grant(uuid, uuid, text, timestamptz, boolean), studyverse._inst_revoke(uuid, uuid, text), studyverse._inst_sync(uuid, uuid) to service_role;

-- ---------- members ----------
create or replace function studyverse._inst_clean(p text, n int) returns text language sql immutable set search_path = '' as $$
  select nullif(left(regexp_replace(trim(coalesce(p, '')), '[\s<>]+', ' ', 'g'), n), '') $$;

-- add or update a member (service role, or called by inst_join after its checks). Never touches parent_links.
create or replace function studyverse._inst_add_member(p_inst uuid, p_user uuid, p_role text, p_class uuid, p_roll text, p_name text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare em text;
begin
  if p_role not in ('admin', 'teacher', 'student') then return jsonb_build_object('ok', false, 'msg', 'Unknown role.'); end if;
  if p_class is not null and not exists (select 1 from studyverse.inst_classes where id = p_class and institution_id = p_inst) then
    return jsonb_build_object('ok', false, 'msg', 'This class is not in this institution.'); end if;
  if p_role = 'student' and p_class is null then return jsonb_build_object('ok', false, 'msg', 'Choose the class.'); end if;
  insert into studyverse.institution_members (institution_id, user_id, role, class_id, roll_no, display_name)
  values (p_inst, p_user, p_role, case when p_role = 'student' then p_class end, studyverse._inst_clean(p_roll, 20), studyverse._inst_clean(p_name, 60))
  on conflict (institution_id, user_id, role) do update set
    class_id = case when excluded.role = 'student' then excluded.class_id else studyverse.institution_members.class_id end,
    roll_no = coalesce(excluded.roll_no, studyverse.institution_members.roll_no),
    display_name = coalesce(excluded.display_name, studyverse.institution_members.display_name);
  if p_role = 'teacher' and p_class is not null then
    insert into studyverse.teacher_classes (class_id, user_id) values (p_class, p_user) on conflict do nothing;
  end if;
  if p_role = 'student' then
    select lower(email) into em from auth.users where id = p_user;
    update studyverse.inst_parent_invites set child_id = p_user where institution_id = p_inst and child_id is null and student_email = em;
    perform studyverse._inst_sync(p_inst, p_user);
  end if;
  return jsonb_build_object('ok', true);
end $$;
revoke all on function studyverse._inst_add_member(uuid, uuid, text, uuid, text, text) from public, anon, authenticated;
grant execute on function studyverse._inst_add_member(uuid, uuid, text, uuid, text, text) to service_role;

-- what am I in? (role routing, student badge, teacher class list)
create or replace function studyverse.inst_me() returns jsonb language sql stable security definer set search_path = '' as $$
  select jsonb_build_object('owner', studyverse._inst_owner(), 'memberships', coalesce(jsonb_agg(jsonb_build_object(
      'institution_id', i.id, 'name', i.name, 'type', i.type, 'status', i.status, 'role', m.role,
      'class_id', m.class_id, 'class_name', c.name, 'grade', c.grade, 'course', c.course, 'lb_opt', m.lb_opt,
      'classes', case when m.role = 'teacher' then (select coalesce(jsonb_agg(jsonb_build_object('id', c2.id, 'name', c2.name, 'grade', c2.grade, 'course', c2.course) order by c2.course, c2.section), '[]'::jsonb)
                                                      from studyverse.teacher_classes t join studyverse.inst_classes c2 on c2.id = t.class_id where t.user_id = m.user_id and c2.institution_id = i.id)
                      when m.role = 'admin' then (select coalesce(jsonb_agg(jsonb_build_object('id', c2.id, 'name', c2.name, 'grade', c2.grade, 'course', c2.course) order by c2.course, c2.section), '[]'::jsonb)
                                                      from studyverse.inst_classes c2 where c2.institution_id = i.id) end)
      order by i.name, m.role), '[]'::jsonb))
  from studyverse.institution_members m join studyverse.institutions i on i.id = m.institution_id
  left join studyverse.inst_classes c on c.id = m.class_id
  where m.user_id = auth.uid() $$;
revoke all on function studyverse.inst_me() from public, anon;
grant execute on function studyverse.inst_me() to authenticated;

-- join with a code (students: class code or roll-number code; teachers: teacher code)
create or replace function studyverse.inst_join(p_code text, p_name text default null, p_roll text default null) returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); j studyverse.join_codes%rowtype; i studyverse.institutions%rowtype; c studyverse.inst_classes%rowtype; res jsonb;
begin
  if uid is null then return jsonb_build_object('ok', false, 'msg', 'Please sign in first.'); end if;
  select * into j from studyverse.join_codes where code = upper(regexp_replace(coalesce(p_code, ''), '[\s-]', '', 'g')) for update;
  if not found or not j.active or j.expires_at < now() or j.used >= j.max_uses then
    return jsonb_build_object('ok', false, 'msg', 'This code is not valid or has expired. Please ask your school for a new one.'); end if;
  select * into i from studyverse.institutions where id = j.institution_id;
  select * into c from studyverse.inst_classes where id = j.class_id;
  if j.role = 'student' then
    if (select role from studyverse.profiles where user_id = uid) = 'parent' then
      return jsonb_build_object('ok', false, 'msg', 'This is a parent account. Please sign in with the student''s own account to join the class.'); end if;
    if exists (select 1 from studyverse.institution_members m where m.institution_id = j.institution_id and m.user_id = uid and m.role = 'student' and m.class_id = j.class_id) then
      return jsonb_build_object('ok', true, 'already', true, 'institution', i.name, 'class', c.name, 'role', 'student'); end if;
    res := studyverse._inst_add_member(j.institution_id, uid, 'student', j.class_id, coalesce(j.roll_no, p_roll), coalesce(j.display_name, p_name));
    update studyverse.inst_parent_invites set child_id = uid where join_code = j.code and child_id is null;
    insert into studyverse.profiles (user_id, role) values (uid, 'student') on conflict (user_id) do update set role = coalesce(studyverse.profiles.role, 'student');
  else
    res := studyverse._inst_add_member(j.institution_id, uid, 'teacher', j.class_id, null, p_name);
  end if;
  if not (res ->> 'ok')::boolean then return res; end if;
  update studyverse.join_codes set used = used + 1 where code = j.code;
  return jsonb_build_object('ok', true, 'institution', i.name, 'class', c.name, 'role', j.role);
end $$;
revoke all on function studyverse.inst_join(text, text, text) from public, anon;
grant execute on function studyverse.inst_join(text, text, text) to authenticated;

-- a parent signs in: school-given parent emails for this (confirmed) email become Parent Hub links
create or replace function studyverse.inst_claim() returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); e text; n int := 0; r record;
begin
  if uid is null then return jsonb_build_object('ok', false); end if;
  select lower(email) into e from auth.users where id = uid and email_confirmed_at is not null;
  if e is null then return jsonb_build_object('ok', true, 'linked', 0); end if;
  if (select role from studyverse.profiles where user_id = uid) = 'student' then return jsonb_build_object('ok', true, 'linked', 0); end if;
  for r in select * from studyverse.inst_parent_invites where email = e and accepted_at is null and child_id is not null and child_id <> uid loop
    if (select count(*) from studyverse.parent_links where parent_id = uid) < 6 then
      insert into studyverse.parent_links (parent_id, child_id, child_name) values (uid, r.child_id, r.child_name) on conflict (parent_id, child_id) do nothing;
      n := n + 1;
    end if;
    update studyverse.inst_parent_invites set accepted_at = now() where id = r.id;
  end loop;
  if n > 0 then insert into studyverse.profiles (user_id, role) values (uid, 'parent') on conflict (user_id) do update set role = coalesce(studyverse.profiles.role, 'parent'); end if;
  return jsonb_build_object('ok', true, 'linked', n);
end $$;
revoke all on function studyverse.inst_claim() from public, anon;
grant execute on function studyverse.inst_claim() to authenticated;

create or replace function studyverse.inst_set_leaderboard(p_on boolean) returns jsonb language sql security definer set search_path = '' as $$
  with u as (update studyverse.institution_members set lb_opt = coalesce(p_on, false) where user_id = auth.uid() and role = 'student' returning 1)
  select jsonb_build_object('ok', true, 'n', (select count(*) from u)) $$;
revoke all on function studyverse.inst_set_leaderboard(boolean) from public, anon;
grant execute on function studyverse.inst_set_leaderboard(boolean) to authenticated;

-- ---------- admin: institution, classes, teachers, codes ----------
create or replace function studyverse._inst_details_ok(p jsonb) returns text language plpgsql immutable set search_path = '' as $$
begin
  if p ? 'name' and length(trim(coalesce(p ->> 'name', ''))) < 2 then return 'Enter the institution name.'; end if;
  if coalesce(p ->> 'type', 'school') not in ('school', 'coaching') then return 'Type must be school or coaching.'; end if;
  if nullif(trim(p ->> 'gstin'), '') is not null and upper(trim(p ->> 'gstin')) !~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$' then return 'The GSTIN does not look right (15 characters, e.g. 27ABCDE1234F1Z5).'; end if;
  if nullif(trim(p ->> 'contact_email'), '') is not null and trim(p ->> 'contact_email') !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' then return 'Please check the contact email.'; end if;
  return null;
end $$;

create or replace function studyverse.inst_update_details(p_inst uuid, p jsonb) returns jsonb language plpgsql security definer set search_path = '' as $$
declare e text := studyverse._inst_details_ok(p);
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if e is not null then return jsonb_build_object('ok', false, 'msg', e); end if;
  update studyverse.institutions set
    name = coalesce(studyverse._inst_clean(p ->> 'name', 120), name), city = studyverse._inst_clean(p ->> 'city', 60), state = studyverse._inst_clean(p ->> 'state', 60),
    board = studyverse._inst_clean(p ->> 'board', 40), address = studyverse._inst_clean(p ->> 'address', 300), pincode = studyverse._inst_clean(p ->> 'pincode', 10),
    gstin = upper(studyverse._inst_clean(p ->> 'gstin', 15)), contact_name = studyverse._inst_clean(p ->> 'contact_name', 80),
    contact_email = lower(studyverse._inst_clean(p ->> 'contact_email', 120)), contact_phone = studyverse._inst_clean(p ->> 'contact_phone', 20)
  where id = p_inst;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.inst_save_class(p_inst uuid, p_id uuid, p_kind text, p_grade int, p_section text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare sec text := studyverse._inst_clean(p_section, 40); crs text; nm text; nid uuid;
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if p_kind = 'batch' then
    if sec is null then return jsonb_build_object('ok', false, 'msg', 'Enter the batch name.'); end if;
    crs := 'ca-foundation'; nm := 'CA Foundation · ' || sec; p_grade := null;
  else
    if p_grade is null or p_grade not between 1 and 12 then return jsonb_build_object('ok', false, 'msg', 'Choose a class from 1 to 12.'); end if;
    sec := upper(coalesce(sec, 'A')); crs := 'school-g' || p_grade; nm := p_grade || '-' || sec; p_kind := 'class';
  end if;
  if (select count(*) from studyverse.inst_classes where institution_id = p_inst) >= 300 and p_id is null then return jsonb_build_object('ok', false, 'msg', 'You can have up to 300 classes.'); end if;
  if exists (select 1 from studyverse.inst_classes where institution_id = p_inst and course = crs and section = sec and id is distinct from p_id) then
    return jsonb_build_object('ok', false, 'msg', nm || ' already exists.'); end if;
  if p_id is null then
    insert into studyverse.inst_classes (institution_id, kind, grade, section, course, name) values (p_inst, p_kind, p_grade, sec, crs, nm) returning id into nid;
  else
    update studyverse.inst_classes set kind = p_kind, grade = p_grade, section = sec, course = crs, name = nm where id = p_id and institution_id = p_inst returning id into nid;
    if nid is null then return jsonb_build_object('ok', false, 'msg', 'Class not found.'); end if;
    perform studyverse._inst_sync(p_inst);   -- a changed grade moves students to another course
  end if;
  return jsonb_build_object('ok', true, 'id', nid, 'name', nm);
end $$;

create or replace function studyverse.inst_delete_class(p_id uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
declare c studyverse.inst_classes%rowtype;
begin
  select * into c from studyverse.inst_classes where id = p_id;
  if not found or not studyverse.inst_is_admin(c.institution_id) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if exists (select 1 from studyverse.institution_members where class_id = p_id and role = 'student') then
    return jsonb_build_object('ok', false, 'msg', 'Move or remove the students in ' || c.name || ' first.'); end if;
  delete from studyverse.inst_classes where id = p_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse.inst_assign_teacher(p_class uuid, p_user uuid, p_on boolean) returns jsonb language plpgsql security definer set search_path = '' as $$
declare c studyverse.inst_classes%rowtype;
begin
  select * into c from studyverse.inst_classes where id = p_class;
  if not found or not studyverse.inst_is_admin(c.institution_id) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if not exists (select 1 from studyverse.institution_members where institution_id = c.institution_id and user_id = p_user and role in ('teacher', 'admin')) then
    return jsonb_build_object('ok', false, 'msg', 'This person is not a teacher here.'); end if;
  if p_on then
    insert into studyverse.institution_members (institution_id, user_id, role) values (c.institution_id, p_user, 'teacher') on conflict do nothing;
    insert into studyverse.teacher_classes (class_id, user_id) values (p_class, p_user) on conflict do nothing;
  else delete from studyverse.teacher_classes where class_id = p_class and user_id = p_user; end if;
  return jsonb_build_object('ok', true);
end $$;

-- move a student to another class (same institution) or remove a member. Removing never touches parent links.
create or replace function studyverse.inst_move_student(p_inst uuid, p_user uuid, p_class uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if not exists (select 1 from studyverse.inst_classes where id = p_class and institution_id = p_inst) then return jsonb_build_object('ok', false, 'msg', 'Class not found.'); end if;
  update studyverse.institution_members set class_id = p_class where institution_id = p_inst and user_id = p_user and role = 'student';
  if not found then return jsonb_build_object('ok', false, 'msg', 'Student not found.'); end if;
  perform studyverse._inst_sync(p_inst, p_user);
  return jsonb_build_object('ok', true);
end $$;
create or replace function studyverse.inst_remove_member(p_inst uuid, p_user uuid, p_role text) returns jsonb language plpgsql security definer set search_path = '' as $$
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if p_role = 'admin' and p_user = auth.uid() and not studyverse._inst_owner()
     and (select count(*) from studyverse.institution_members where institution_id = p_inst and role = 'admin') <= 1 then
    return jsonb_build_object('ok', false, 'msg', 'You are the only admin. Add another admin first.'); end if;
  delete from studyverse.institution_members where institution_id = p_inst and user_id = p_user and role = p_role;
  if p_role = 'teacher' then delete from studyverse.teacher_classes t using studyverse.inst_classes c where t.class_id = c.id and c.institution_id = p_inst and t.user_id = p_user; end if;
  if p_role = 'student' then perform studyverse._inst_sync(p_inst, p_user); end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function studyverse._inst_new_code() returns text language plpgsql volatile set search_path = '' as $$
declare k text; alph text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; i int;
begin
  loop
    k := ''; for i in 1..8 loop k := k || substr(alph, 1 + floor(random() * length(alph))::int, 1); end loop;
    exit when not exists (select 1 from studyverse.join_codes where code = k);
  end loop;
  return k;
end $$;
revoke all on function studyverse._inst_new_code() from public, anon, authenticated;

create or replace function studyverse.inst_create_code(p_inst uuid, p_class uuid, p_role text, p_days int default 30, p_max int default 200) returns jsonb language plpgsql security definer set search_path = '' as $$
declare k text;
begin
  if p_role = 'teacher' then
    if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can make teacher codes.'); end if;
  elsif p_role = 'student' then
    if p_class is null or not exists (select 1 from studyverse.inst_classes where id = p_class and institution_id = p_inst) then return jsonb_build_object('ok', false, 'msg', 'Choose the class.'); end if;
    if not studyverse.inst_teaches(p_class) then return jsonb_build_object('ok', false, 'msg', 'Only the admin or this class''s teacher can do this.'); end if;
  else return jsonb_build_object('ok', false, 'msg', 'Unknown role.'); end if;
  if p_class is not null and not exists (select 1 from studyverse.inst_classes where id = p_class and institution_id = p_inst) then return jsonb_build_object('ok', false, 'msg', 'Class not found.'); end if;
  if (select count(*) from studyverse.join_codes where institution_id = p_inst and roll_no is null and created_at > now() - interval '1 day') >= 100 then
    return jsonb_build_object('ok', false, 'msg', 'Too many codes made today. Please try again tomorrow.'); end if;
  k := studyverse._inst_new_code();
  insert into studyverse.join_codes (code, institution_id, class_id, role, max_uses, expires_at, created_by)
  values (k, p_inst, p_class, p_role, greatest(1, least(coalesce(p_max, 200), 2000)), now() + make_interval(days => greatest(1, least(coalesce(p_days, 30), 365))), auth.uid());
  return jsonb_build_object('ok', true, 'code', k);
end $$;

create or replace function studyverse.inst_revoke_code(p_code text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare j studyverse.join_codes%rowtype;
begin
  select * into j from studyverse.join_codes where code = p_code;
  if not found or not (studyverse.inst_is_admin(j.institution_id) or (j.role = 'student' and studyverse.inst_teaches(j.class_id))) then
    return jsonb_build_object('ok', false, 'msg', 'Not allowed.'); end if;
  update studyverse.join_codes set active = false where code = p_code;
  return jsonb_build_object('ok', true);
end $$;

-- seats by band, students, teachers, activity (admin console overview)
create or replace function studyverse.inst_overview(p_inst uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare i studyverse.institutions%rowtype; seats jsonb;
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  select * into i from studyverse.institutions where id = p_inst;
  select coalesce(jsonb_agg(jsonb_build_object('band', x.band, 'label', x.label, 'rate', x.rate,
      'total', coalesce((select sum((l ->> 'students')::int) from studyverse.seat_orders o, jsonb_array_elements(o.lines) l
                          where o.institution_id = p_inst and o.status = 'paid' and o.valid_until > now() and l ->> 'band' = x.band), 0),
      'used', (select count(*) from studyverse.inst_grants g where g.institution_id = p_inst and g.band = x.band and not g.pilot),
      'pilot', (select count(*) from studyverse.inst_grants g where g.institution_id = p_inst and g.band = x.band and g.pilot),
      'students', (select count(*) from studyverse.institution_members m join studyverse.inst_classes c on c.id = m.class_id
                    where m.institution_id = p_inst and m.role = 'student' and studyverse._inst_band(c.course) = x.band)) order by x.sort), '[]'::jsonb)
    into seats from studyverse.inst_rates x;
  return jsonb_build_object('ok', true, 'institution', to_jsonb(i), 'seats', seats,
    'pilot_class', (select name from studyverse.inst_classes where id = i.pilot_class_id),
    'students', (select count(*) from studyverse.institution_members where institution_id = p_inst and role = 'student'),
    'teachers', (select count(distinct user_id) from studyverse.institution_members where institution_id = p_inst and role = 'teacher'),
    'classes', (select count(*) from studyverse.inst_classes where institution_id = p_inst),
    'active7', (select count(*) from studyverse.institution_members m join studyverse.progress p on p.user_id = m.user_id
                 where m.institution_id = p_inst and m.role = 'student' and p.updated_at > now() - interval '7 days'),
    'paid_until', (select max(valid_until) from studyverse.seat_orders where institution_id = p_inst and status = 'paid'));
end $$;

-- people list for the admin console
create or replace function studyverse.inst_roster(p_inst uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  return jsonb_build_object('ok', true,
    'students', (select coalesce(jsonb_agg(jsonb_build_object('user_id', m.user_id, 'name', coalesce(m.display_name, p.state -> 'st' -> 'profile' ->> 'name', split_part(u.email, '@', 1)),
        'email', u.email, 'roll_no', m.roll_no, 'class_id', m.class_id, 'class_name', c.name,
        'seat', (select case when g.pilot then 'pilot' else 'paid' end from studyverse.inst_grants g where g.institution_id = p_inst and g.user_id = m.user_id limit 1),
        'parents', (select count(*) from studyverse.parent_links l where l.child_id = m.user_id), 'last_active', p.updated_at)
        order by c.course, c.section, m.roll_no nulls last, m.display_name), '[]'::jsonb)
      from studyverse.institution_members m join auth.users u on u.id = m.user_id left join studyverse.inst_classes c on c.id = m.class_id
      left join studyverse.progress p on p.user_id = m.user_id where m.institution_id = p_inst and m.role = 'student'),
    'staff', (select coalesce(jsonb_agg(jsonb_build_object('user_id', m.user_id, 'email', u.email, 'name', m.display_name, 'role', m.role,
        'classes', (select coalesce(jsonb_agg(t.class_id), '[]'::jsonb) from studyverse.teacher_classes t join studyverse.inst_classes c on c.id = t.class_id where t.user_id = m.user_id and c.institution_id = p_inst))
        order by m.role, u.email), '[]'::jsonb)
      from studyverse.institution_members m join auth.users u on u.id = m.user_id where m.institution_id = p_inst and m.role in ('admin', 'teacher')),
    'pending', (select coalesce(jsonb_agg(jsonb_build_object('code', j.code, 'roll_no', j.roll_no, 'name', j.display_name, 'class_id', j.class_id) order by j.roll_no), '[]'::jsonb)
      from studyverse.join_codes j where j.institution_id = p_inst and j.roll_no is not null and j.used = 0 and j.active and j.expires_at > now()));
end $$;

-- ---------- orders & invoices ----------
create or replace function studyverse.create_order(p_inst uuid, p_lines jsonb, p_ay text default null, p_submit boolean default true) returns jsonb language plpgsql security definer set search_path = '' as $$
declare i studyverse.institutions%rowtype; q jsonb; ay text := coalesce(nullif(trim(p_ay), ''), studyverse._inst_ay(now())); cur text := studyverse._inst_ay(now());
  cfg studyverse.billing_config%rowtype; inv text; oid uuid;
begin
  if not studyverse.inst_is_admin(p_inst) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if ay !~ '^20[0-9]{2}-[0-9]{2}$' or (substr(ay, 1, 4)::int + 1) % 100 <> substr(ay, 6, 2)::int
     or substr(ay, 1, 4)::int not between substr(cur, 1, 4)::int and substr(cur, 1, 4)::int + 1 then
    return jsonb_build_object('ok', false, 'msg', 'Choose this academic year or the next one.'); end if;
  if (select count(*) from studyverse.seat_orders where institution_id = p_inst and created_at > now() - interval '1 day') >= 20 then
    return jsonb_build_object('ok', false, 'msg', 'Too many orders today. Please write to support@moneyviel.com.'); end if;
  select * into i from studyverse.institutions where id = p_inst;
  q := studyverse._inst_price(p_lines, i.state);
  if not (q ->> 'ok')::boolean then return q; end if;
  if p_submit then
    update studyverse.billing_config set next_no = next_no + 1, updated_at = now() where id = 1 returning * into cfg;
    inv := cfg.invoice_prefix || ay || '-' || lpad((cfg.next_no - 1)::text, 4, '0');
  else select * into cfg from studyverse.billing_config where id = 1; end if;
  insert into studyverse.seat_orders (institution_id, lines, students, subtotal, discount_pct, discount_amt, taxable, gst, total, academic_year, valid_until, status,
      invoice_no, seller, buyer, created_by, invoiced_at)
  values (p_inst, q -> 'lines', (q ->> 'students')::int, (q ->> 'subtotal')::numeric, (q ->> 'discount_pct')::int, (q ->> 'discount_amt')::numeric,
      (q ->> 'taxable')::numeric, q -> 'gst', (q ->> 'total')::numeric, ay, studyverse._inst_ay_end(ay), case when p_submit then 'invoiced' else 'draft' end,
      inv, jsonb_build_object('name', cfg.seller_name, 'legal_name', cfg.legal_name, 'address', cfg.address, 'city', cfg.city, 'state', cfg.state, 'gstin', cfg.gstin, 'email', cfg.email),
      jsonb_build_object('name', i.name, 'address', i.address, 'city', i.city, 'state', i.state, 'pincode', i.pincode, 'gstin', i.gstin,
        'contact_name', i.contact_name, 'contact_email', i.contact_email, 'contact_phone', i.contact_phone),
      auth.uid(), case when p_submit then now() end)
  returning id into oid;
  return q || jsonb_build_object('order_id', oid, 'invoice_no', inv, 'status', case when p_submit then 'invoiced' else 'draft' end, 'academic_year', ay);
end $$;

-- a draft becomes "invoiced" (gets its number); admin may cancel an unpaid order
create or replace function studyverse.submit_order(p_order uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
declare o studyverse.seat_orders%rowtype; cfg studyverse.billing_config%rowtype;
begin
  select * into o from studyverse.seat_orders where id = p_order for update;
  if not found or not studyverse.inst_is_admin(o.institution_id) then return jsonb_build_object('ok', false, 'msg', 'Order not found.'); end if;
  if o.status <> 'draft' then return jsonb_build_object('ok', true, 'invoice_no', o.invoice_no, 'status', o.status); end if;
  update studyverse.billing_config set next_no = next_no + 1, updated_at = now() where id = 1 returning * into cfg;
  update studyverse.seat_orders set status = 'invoiced', invoiced_at = now(), invoice_no = cfg.invoice_prefix || o.academic_year || '-' || lpad((cfg.next_no - 1)::text, 4, '0')
   where id = p_order returning * into o;
  return jsonb_build_object('ok', true, 'invoice_no', o.invoice_no, 'status', o.status);
end $$;
create or replace function studyverse.cancel_order(p_order uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
declare o studyverse.seat_orders%rowtype;
begin
  select * into o from studyverse.seat_orders where id = p_order for update;
  if not found or not studyverse.inst_is_admin(o.institution_id) then return jsonb_build_object('ok', false, 'msg', 'Order not found.'); end if;
  if o.status = 'paid' then return jsonb_build_object('ok', false, 'msg', 'A paid order cannot be cancelled here. Please write to support@moneyviel.com.'); end if;
  update studyverse.seat_orders set status = 'cancelled' where id = p_order;
  return jsonb_build_object('ok', true);
end $$;

-- service: details for the "invoice requested" email (only for someone who manages the institution; once per 10 minutes)
create or replace function studyverse._inst_order_mail(p_order uuid, p_caller uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
declare o studyverse.seat_orders%rowtype; u text;
begin
  select * into o from studyverse.seat_orders where id = p_order for update;
  if not found or not studyverse._inst_can_manage(o.institution_id, p_caller) then return jsonb_build_object('ok', false, 'msg', 'Order not found.'); end if;
  if o.status not in ('invoiced', 'paid') then return jsonb_build_object('ok', false, 'msg', 'Request the invoice first.'); end if;
  if o.mailed_at > now() - interval '10 minutes' then return jsonb_build_object('ok', false, 'msg', 'We already have this request. We will reply soon.'); end if;
  update studyverse.seat_orders set mailed_at = now() where id = p_order;
  select email into u from auth.users where id = p_caller;
  return jsonb_build_object('ok', true, 'order', to_jsonb(o), 'by', u);
end $$;
revoke all on function studyverse._inst_order_mail(uuid, uuid) from public, anon, authenticated;
grant execute on function studyverse._inst_order_mail(uuid, uuid) to service_role;

-- ---------- owner (studyverse.admins) ----------
create or replace function studyverse.owner_create_institution(p jsonb) returns jsonb language plpgsql security definer set search_path = '' as $$
declare e text := studyverse._inst_details_ok(p || jsonb_build_object('name', coalesce(p ->> 'name', ''))); nid uuid;
begin
  if not studyverse._inst_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  if e is not null then return jsonb_build_object('ok', false, 'msg', e); end if;
  insert into studyverse.institutions (name, type, city, state, board, address, pincode, gstin, contact_name, contact_email, contact_phone, status, created_by)
  values (studyverse._inst_clean(p ->> 'name', 120), coalesce(p ->> 'type', 'school'), studyverse._inst_clean(p ->> 'city', 60), studyverse._inst_clean(p ->> 'state', 60),
    studyverse._inst_clean(p ->> 'board', 40), studyverse._inst_clean(p ->> 'address', 300), studyverse._inst_clean(p ->> 'pincode', 10), upper(studyverse._inst_clean(p ->> 'gstin', 15)),
    studyverse._inst_clean(p ->> 'contact_name', 80), lower(studyverse._inst_clean(p ->> 'contact_email', 120)), studyverse._inst_clean(p ->> 'contact_phone', 20), 'pilot', auth.uid())
  returning id into nid;
  return jsonb_build_object('ok', true, 'id', nid);
end $$;

create or replace function studyverse.owner_list_institutions() returns jsonb language sql stable security definer set search_path = '' as $$
  select case when not studyverse._inst_owner() then '[]'::jsonb else coalesce((select jsonb_agg(to_jsonb(i) || jsonb_build_object(
      'students', (select count(*) from studyverse.institution_members m where m.institution_id = i.id and m.role = 'student'),
      'admins', (select coalesce(jsonb_agg(u.email), '[]'::jsonb) from studyverse.institution_members m join auth.users u on u.id = m.user_id where m.institution_id = i.id and m.role = 'admin'),
      'classes', (select coalesce(jsonb_agg(jsonb_build_object('id', c.id, 'name', c.name) order by c.course, c.section), '[]'::jsonb) from studyverse.inst_classes c where c.institution_id = i.id),
      'pilot_class', (select name from studyverse.inst_classes c where c.id = i.pilot_class_id),
      'orders', (select count(*) from studyverse.seat_orders o where o.institution_id = i.id and o.status in ('invoiced', 'paid'))) order by i.created_at desc)
    from studyverse.institutions i), '[]'::jsonb) end $$;

create or replace function studyverse.owner_list_orders() returns jsonb language sql stable security definer set search_path = '' as $$
  select case when not studyverse._inst_owner() then '[]'::jsonb else coalesce((select jsonb_agg(to_jsonb(o) || jsonb_build_object('institution', i.name) order by o.created_at desc)
    from studyverse.seat_orders o join studyverse.institutions i on i.id = o.institution_id where o.status <> 'draft'), '[]'::jsonb) end $$;

-- free pilot: one class, up to 30 days
create or replace function studyverse.owner_grant_pilot(p_inst uuid, p_class uuid, p_days int default 30) returns jsonb language plpgsql security definer set search_path = '' as $$
declare until timestamptz;
begin
  if not studyverse._inst_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  if coalesce(p_days, 0) not between 1 and 30 then return jsonb_build_object('ok', false, 'msg', 'A pilot is 1 to 30 days.'); end if;
  if not exists (select 1 from studyverse.inst_classes where id = p_class and institution_id = p_inst) then return jsonb_build_object('ok', false, 'msg', 'Choose one class of this institution.'); end if;
  until := now() + make_interval(days => p_days);
  update studyverse.institutions set pilot_class_id = p_class, pilot_until = until where id = p_inst;
  perform studyverse._inst_sync(p_inst);
  return jsonb_build_object('ok', true, 'pilot_until', until);
end $$;

create or replace function studyverse.owner_end_pilot(p_inst uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
begin
  if not studyverse._inst_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  update studyverse.institutions set pilot_until = now() - interval '1 second' where id = p_inst;
  perform studyverse._inst_sync(p_inst);
  return jsonb_build_object('ok', true);
end $$;

-- owner confirms payment received → seats switch on for the academic year
create or replace function studyverse.owner_mark_paid(p_order uuid, p_ref text default null) returns jsonb language plpgsql security definer set search_path = '' as $$
declare o studyverse.seat_orders%rowtype; cfg studyverse.billing_config%rowtype;
begin
  if not studyverse._inst_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  select * into o from studyverse.seat_orders where id = p_order for update;
  if not found then return jsonb_build_object('ok', false, 'msg', 'Order not found.'); end if;
  if o.status = 'cancelled' then return jsonb_build_object('ok', false, 'msg', 'This order was cancelled.'); end if;
  if o.status <> 'paid' then
    if o.invoice_no is null then
      update studyverse.billing_config set next_no = next_no + 1, updated_at = now() where id = 1 returning * into cfg;
      o.invoice_no := cfg.invoice_prefix || o.academic_year || '-' || lpad((cfg.next_no - 1)::text, 4, '0');
    end if;
    update studyverse.seat_orders set status = 'paid', paid_at = now(), payment_ref = studyverse._inst_clean(p_ref, 80), invoice_no = o.invoice_no,
      invoiced_at = coalesce(invoiced_at, now()) where id = p_order;
  end if;
  perform studyverse._inst_sync(o.institution_id);
  return jsonb_build_object('ok', true, 'invoice_no', o.invoice_no, 'valid_until', o.valid_until);
end $$;

create or replace function studyverse.owner_set_billing(p jsonb) returns jsonb language plpgsql security definer set search_path = '' as $$
declare g text := upper(nullif(trim(coalesce(p ->> 'gstin', '')), ''));
begin
  if not studyverse._inst_owner() then return jsonb_build_object('ok', false, 'msg', 'Owner only.'); end if;
  if g is not null and g !~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$' then return jsonb_build_object('ok', false, 'msg', 'The GSTIN does not look right (15 characters, e.g. 27ABCDE1234F1Z5).'); end if;
  if nullif(trim(coalesce(p ->> 'state', '')), '') is null then return jsonb_build_object('ok', false, 'msg', 'Choose the seller''s state.'); end if;
  update studyverse.billing_config set gstin = g, state = studyverse._inst_clean(p ->> 'state', 60),
    address = coalesce(studyverse._inst_clean(p ->> 'address', 300), address), city = coalesce(studyverse._inst_clean(p ->> 'city', 60), city), updated_at = now() where id = 1;
  return jsonb_build_object('ok', true);
end $$;

-- ---------- homework ----------
create or replace function studyverse.inst_set_homework(p_class uuid, p_kind text, p_target text, p_title text, p_subject text, p_due date, p_need int default null) returns jsonb language plpgsql security definer set search_path = '' as $$
declare c studyverse.inst_classes%rowtype; hid uuid;
begin
  select * into c from studyverse.inst_classes where id = p_class;
  if not found or not studyverse.inst_teaches(p_class) then return jsonb_build_object('ok', false, 'msg', 'Only this class''s teacher can set homework.'); end if;
  if p_kind not in ('chapter', 'quiz', 'mcq') then return jsonb_build_object('ok', false, 'msg', 'Choose the homework type.'); end if;
  if coalesce(p_target, '') !~ '^([0-9]{1,2}-[a-z]+-[0-9]{1,3}|[a-z]{3}-p[0-9]+-ch[0-9]+(-u[0-9]+)?)$' then return jsonb_build_object('ok', false, 'msg', 'Choose a chapter or unit.'); end if;
  if p_due is null or p_due < (now() at time zone 'Asia/Kolkata')::date or p_due > (now() at time zone 'Asia/Kolkata')::date + 60 then
    return jsonb_build_object('ok', false, 'msg', 'Choose a due date from today up to 60 days ahead.'); end if;
  if studyverse._inst_clean(p_title, 160) is null then return jsonb_build_object('ok', false, 'msg', 'Enter a title.'); end if;
  if (select count(*) from studyverse.homework where class_id = p_class and created_at > now() - interval '1 day') >= 30 then
    return jsonb_build_object('ok', false, 'msg', 'Too much homework set today for this class.'); end if;
  insert into studyverse.homework (institution_id, class_id, kind, target, title, subject, need, due_date, created_by)
  values (c.institution_id, p_class, p_kind, p_target, studyverse._inst_clean(p_title, 160), studyverse._inst_clean(p_subject, 80),
          greatest(1, least(coalesce(p_need, case when p_kind = 'chapter' then 3 else 5 end), 50)), p_due, auth.uid())
  returning id into hid;
  return jsonb_build_object('ok', true, 'id', hid);
end $$;
create or replace function studyverse.inst_delete_homework(p_id uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
declare h studyverse.homework%rowtype;
begin
  select * into h from studyverse.homework where id = p_id;
  if not found or not studyverse.inst_teaches(h.class_id) then return jsonb_build_object('ok', false, 'msg', 'Not allowed.'); end if;
  delete from studyverse.homework where id = p_id;
  return jsonb_build_object('ok', true);
end $$;
-- student: my homework (due in the last 7 days or later), with done flags
create or replace function studyverse.my_homework() returns jsonb language sql stable security definer set search_path = '' as $$
  select coalesce(jsonb_agg(jsonb_build_object('id', h.id, 'kind', h.kind, 'target', h.target, 'title', h.title, 'subject', h.subject, 'need', h.need,
      'due_date', h.due_date, 'set_at', h.created_at, 'class_name', c.name,
      'done_at', (select d.done_at from studyverse.hw_done d where d.homework_id = h.id and d.user_id = auth.uid())) order by h.due_date, h.created_at), '[]'::jsonb)
  from studyverse.homework h join studyverse.inst_classes c on c.id = h.class_id
  join studyverse.institution_members m on m.class_id = h.class_id and m.user_id = auth.uid() and m.role = 'student'
  where h.due_date >= (now() at time zone 'Asia/Kolkata')::date - 7 $$;
create or replace function studyverse.homework_done(p_id uuid) returns jsonb language plpgsql security definer set search_path = '' as $$
begin
  if not exists (select 1 from studyverse.homework h join studyverse.institution_members m on m.class_id = h.class_id and m.role = 'student'
                  where h.id = p_id and m.user_id = auth.uid()) then return jsonb_build_object('ok', false, 'msg', 'Homework not found.'); end if;
  insert into studyverse.hw_done (homework_id, user_id) values (p_id, auth.uid()) on conflict do nothing;
  return jsonb_build_object('ok', true);
end $$;

-- ---------- teacher data ----------
-- the synced progress of every student in a class (teachers of the class, admins, owner)
create or replace function studyverse.class_progress(p_class uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare c studyverse.inst_classes%rowtype;
begin
  select * into c from studyverse.inst_classes where id = p_class;
  if not found or not studyverse.inst_teaches(p_class) then return jsonb_build_object('ok', false, 'msg', 'Only this class''s teacher can see it.'); end if;
  return jsonb_build_object('ok', true, 'class', to_jsonb(c),
    'institution', (select jsonb_build_object('id', i.id, 'name', i.name, 'type', i.type) from studyverse.institutions i where i.id = c.institution_id),
    'students', (select coalesce(jsonb_agg(jsonb_build_object('user_id', m.user_id, 'name', coalesce(m.display_name, p.state -> 'st' -> 'profile' ->> 'name', 'Student'),
        'roll_no', m.roll_no, 'lb_opt', m.lb_opt, 'joined_at', m.joined_at, 'state', p.state -> 'st', 'updated_at', p.updated_at,
        'parents', (select count(*) from studyverse.parent_links l where l.child_id = m.user_id),
        'hw', (select coalesce(jsonb_object_agg(d.homework_id, d.done_at), '{}'::jsonb) from studyverse.hw_done d join studyverse.homework h on h.id = d.homework_id
                where d.user_id = m.user_id and h.class_id = p_class)) order by m.roll_no nulls last, m.display_name), '[]'::jsonb)
      from studyverse.institution_members m left join studyverse.progress p on p.user_id = m.user_id where m.class_id = p_class and m.role = 'student'),
    'homework', (select coalesce(jsonb_agg(to_jsonb(h) order by h.due_date desc, h.created_at desc), '[]'::jsonb) from studyverse.homework h where h.class_id = p_class));
end $$;

-- opt-in leaderboard: first names and correct answers in the last 7 days (students of the class and its teachers)
create or replace function studyverse.class_leaderboard(p_class uuid) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare since text := to_char((now() at time zone 'Asia/Kolkata')::date - 6, 'YYYY-MM-DD'); since_min bigint := floor(extract(epoch from now() - interval '7 days') / 60);
begin
  if not (studyverse.inst_in_class(p_class) or studyverse.inst_teaches(p_class)) then return jsonb_build_object('ok', false, 'msg', 'Not allowed.'); end if;
  return jsonb_build_object('ok', true, 'rows', (select coalesce(jsonb_agg(x order by (x ->> 'score')::int desc, x ->> 'name'), '[]'::jsonb) from (
    select jsonb_build_object('name', split_part(coalesce(m.display_name, p.state -> 'st' -> 'profile' ->> 'name', 'Student'), ' ', 1), 'me', m.user_id = auth.uid(),
      'score', coalesce((select sum(coalesce((d.value ->> 'r')::int, 0)) from jsonb_each(case when jsonb_typeof(p.state -> 'st' -> 'ins' -> 'day') = 'object' then p.state -> 'st' -> 'ins' -> 'day' else '{}'::jsonb end) d where d.key >= since), 0)
             + coalesce((select count(*) from jsonb_array_elements(case when jsonb_typeof(p.state -> 'st' -> 'ca' -> 'mlog') = 'array' then p.state -> 'st' -> 'ca' -> 'mlog' else '[]'::jsonb end) e
                          where jsonb_typeof(e) = 'array' and (e ->> 0) ~ '^[0-9]+$' and (e ->> 0)::bigint >= since_min and coalesce(e ->> 2, '0') in ('1', 'true')), 0)) x
    from studyverse.institution_members m left join studyverse.progress p on p.user_id = m.user_id
    where m.class_id = p_class and m.role = 'student' and m.lb_opt) s));
end $$;

-- ---------- service: bulk upload + pilot requests ----------
-- rows: [{name, class:'7'|'CA', section, roll, email?, parent_email?}] → classes found / made, roll-number codes for rows without an
-- email, a list of students to invite by email; parent emails saved (linked when the parent signs in).
create or replace function studyverse._inst_bulk_prepare(p_caller uuid, p_inst uuid, p_rows jsonb) returns jsonb language plpgsql security definer set search_path = '' as $$
declare r jsonb; idx int := 0; cls text; sec text; g int; crs text; nm text; cid uuid; k text; em text; pem text; roll text; sname text;
  codes jsonb := '[]'::jsonb; inv jsonb := '[]'::jsonb; errs jsonb := '[]'::jsonb; made int := 0; mails int := 0; today int; ex studyverse.join_codes%rowtype;
begin
  if not studyverse._inst_can_manage(p_inst, p_caller) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if jsonb_typeof(p_rows) <> 'array' or jsonb_array_length(p_rows) = 0 then return jsonb_build_object('ok', false, 'msg', 'No rows found.'); end if;
  if jsonb_array_length(p_rows) > 500 then return jsonb_build_object('ok', false, 'msg', 'Up to 500 students per upload. Please split the list.'); end if;
  if (select count(*) from studyverse.inst_bulk_log where institution_id = p_inst and at > now() - interval '1 hour') >= 10 then
    return jsonb_build_object('ok', false, 'msg', 'Too many uploads in the last hour. Please wait a little.'); end if;
  select (count(distinct lower(trim(e ->> 'email'))) filter (where coalesce(trim(e ->> 'email'), '') <> '') + count(distinct lower(trim(e ->> 'parent_email'))) filter (where coalesce(trim(e ->> 'parent_email'), '') <> ''))::int
    into mails from jsonb_array_elements(p_rows) e;
  select coalesce(sum(emails), 0) into today from studyverse.inst_bulk_log where institution_id = p_inst and at > now() - interval '1 day';
  if today + mails > 250 then return jsonb_build_object('ok', false, 'msg', 'This upload would send ' || mails || ' emails; the daily limit is 250 (' || greatest(0, 250 - today) || ' left today). Remove some emails or upload the rest tomorrow.'); end if;
  for r in select * from jsonb_array_elements(p_rows) loop
    idx := idx + 1;
    sname := studyverse._inst_clean(r ->> 'name', 60); cls := upper(trim(coalesce(r ->> 'class', ''))); sec := studyverse._inst_clean(r ->> 'section', 40);
    roll := studyverse._inst_clean(r ->> 'roll', 20); em := lower(nullif(trim(coalesce(r ->> 'email', '')), '')); pem := lower(nullif(trim(coalesce(r ->> 'parent_email', '')), ''));
    if sname is null then errs := errs || jsonb_build_object('row', idx, 'msg', 'Name is missing.'); continue; end if;
    if em is not null and em !~ '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$' then errs := errs || jsonb_build_object('row', idx, 'msg', 'Student email does not look right.'); continue; end if;
    if pem is not null and pem !~ '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$' then errs := errs || jsonb_build_object('row', idx, 'msg', 'Parent email does not look right.'); continue; end if;
    if pem is not null and pem = em then errs := errs || jsonb_build_object('row', idx, 'msg', 'Parent email is the same as the student email.'); continue; end if;
    if cls ~ '^CA' then crs := 'ca-foundation'; g := null; sec := coalesce(sec, 'Batch 1'); nm := 'CA Foundation · ' || sec;
    elsif cls ~ '^(CLASS\s*)?([1-9]|1[0-2])$' then g := regexp_replace(cls, '[^0-9]', '', 'g')::int; crs := 'school-g' || g; sec := upper(coalesce(sec, 'A')); nm := g || '-' || sec;
    else errs := errs || jsonb_build_object('row', idx, 'msg', 'Class must be 1 to 12 or CA.'); continue; end if;
    select id into cid from studyverse.inst_classes where institution_id = p_inst and course = crs and section = sec;
    if cid is null then
      insert into studyverse.inst_classes (institution_id, kind, grade, section, course, name) values (p_inst, case when g is null then 'batch' else 'class' end, g, sec, crs, nm) returning id into cid;
      made := made + 1;
    end if;
    if em is not null then
      inv := inv || jsonb_build_object('row', idx, 'email', em, 'name', sname, 'roll', roll, 'class_id', cid, 'class_name', nm, 'parent_email', pem);
      if pem is not null then insert into studyverse.inst_parent_invites (institution_id, email, student_email, child_name) values (p_inst, pem, em, sname); end if;
    else
      select * into ex from studyverse.join_codes where institution_id = p_inst and class_id = cid and roll_no is not distinct from roll and display_name = sname and used = 0 and active and expires_at > now() limit 1;
      if found then k := ex.code;
      else
        k := studyverse._inst_new_code();
        insert into studyverse.join_codes (code, institution_id, class_id, role, roll_no, display_name, max_uses, expires_at, created_by)
        values (k, p_inst, cid, 'student', roll, sname, 1, now() + interval '60 days', p_caller);
      end if;
      codes := codes || jsonb_build_object('row', idx, 'name', sname, 'roll', roll, 'class_name', nm, 'code', k, 'parent_email', pem);
      if pem is not null then insert into studyverse.inst_parent_invites (institution_id, email, join_code, child_name) values (p_inst, pem, k, sname); end if;
    end if;
  end loop;
  insert into studyverse.inst_bulk_log (institution_id, caller, rows, emails) values (p_inst, p_caller, idx, mails);
  return jsonb_build_object('ok', true, 'classes_created', made, 'codes', codes, 'invites', inv, 'errors', errs,
    'institution', (select name from studyverse.institutions where id = p_inst));
end $$;
revoke all on function studyverse._inst_bulk_prepare(uuid, uuid, jsonb) from public, anon, authenticated;
grant execute on function studyverse._inst_bulk_prepare(uuid, uuid, jsonb) to service_role;

-- staff invite (owner → first admin; admin → teachers / admins): checked here, account made by the edge function
create or replace function studyverse._inst_staff_ok(p_caller uuid, p_inst uuid, p_role text) returns jsonb language plpgsql security definer set search_path = '' as $$
begin
  if p_role not in ('admin', 'teacher') then return jsonb_build_object('ok', false, 'msg', 'Unknown role.'); end if;
  if not studyverse._inst_can_manage(p_inst, p_caller) then return jsonb_build_object('ok', false, 'msg', 'Only the institution admin can do this.'); end if;
  if (select coalesce(sum(emails), 0) from studyverse.inst_bulk_log where institution_id = p_inst and at > now() - interval '1 day') >= 250 then
    return jsonb_build_object('ok', false, 'msg', 'Daily email limit reached. Please try tomorrow.'); end if;
  insert into studyverse.inst_bulk_log (institution_id, caller, rows, emails) values (p_inst, p_caller, 1, 1);
  return jsonb_build_object('ok', true, 'institution', (select name from studyverse.institutions where id = p_inst));
end $$;
revoke all on function studyverse._inst_staff_ok(uuid, uuid, text) from public, anon, authenticated;
grant execute on function studyverse._inst_staff_ok(uuid, uuid, text) to service_role;

-- public "Request a free pilot" form (pricing page) — rate-limited per IP (hashed) and per day
create or replace function studyverse._pilot_request(p jsonb, p_ip text) returns jsonb language plpgsql security definer set search_path = '' as $$
begin
  if (select count(*) from studyverse.pilot_requests where ip_hash = p_ip and created_at > now() - interval '1 hour') >= 3 then
    return jsonb_build_object('ok', false, 'code', 'limit', 'msg', 'We already have your request. We will call you soon.'); end if;
  if (select count(*) from studyverse.pilot_requests where created_at > now() - interval '1 day') >= 100 then
    return jsonb_build_object('ok', false, 'code', 'limit', 'msg', 'Please email support@moneyviel.com instead.'); end if;
  insert into studyverse.pilot_requests (name, school, city, phone, email, students, ip_hash)
  values (studyverse._inst_clean(p ->> 'name', 80), studyverse._inst_clean(p ->> 'school', 120), studyverse._inst_clean(p ->> 'city', 60),
          studyverse._inst_clean(p ->> 'phone', 20), lower(studyverse._inst_clean(p ->> 'email', 120)), least(greatest(coalesce((p ->> 'students')::int, 0), 0), 1000000), p_ip);
  return jsonb_build_object('ok', true);
end $$;
revoke all on function studyverse._pilot_request(jsonb, text) from public, anon, authenticated;
grant execute on function studyverse._pilot_request(jsonb, text) to service_role;

-- ---------- grants for the signed-in API ----------
do $$ declare f text; begin
  foreach f in array array[
    'studyverse.inst_update_details(uuid, jsonb)', 'studyverse.inst_save_class(uuid, uuid, text, int, text)', 'studyverse.inst_delete_class(uuid)',
    'studyverse.inst_assign_teacher(uuid, uuid, boolean)', 'studyverse.inst_move_student(uuid, uuid, uuid)', 'studyverse.inst_remove_member(uuid, uuid, text)',
    'studyverse.inst_create_code(uuid, uuid, text, int, int)', 'studyverse.inst_revoke_code(text)', 'studyverse.inst_overview(uuid)', 'studyverse.inst_roster(uuid)',
    'studyverse.create_order(uuid, jsonb, text, boolean)', 'studyverse.submit_order(uuid)', 'studyverse.cancel_order(uuid)',
    'studyverse.owner_create_institution(jsonb)', 'studyverse.owner_list_institutions()', 'studyverse.owner_list_orders()', 'studyverse.owner_grant_pilot(uuid, uuid, int)',
    'studyverse.owner_end_pilot(uuid)', 'studyverse.owner_mark_paid(uuid, text)', 'studyverse.owner_set_billing(jsonb)',
    'studyverse.inst_set_homework(uuid, text, text, text, text, date, int)', 'studyverse.inst_delete_homework(uuid)', 'studyverse.my_homework()', 'studyverse.homework_done(uuid)',
    'studyverse.class_progress(uuid)', 'studyverse.class_leaderboard(uuid)'] loop
    execute 'revoke all on function ' || f || ' from public, anon';
    execute 'grant execute on function ' || f || ' to authenticated';
  end loop;
end $$;
revoke all on function studyverse._inst_details_ok(jsonb), studyverse._inst_clean(text, int), studyverse._inst_band(text), studyverse._inst_ay(timestamptz), studyverse._inst_ay_end(text) from public, anon;
grant execute on function studyverse._inst_details_ok(jsonb), studyverse._inst_clean(text, int), studyverse._inst_band(text), studyverse._inst_ay(timestamptz), studyverse._inst_ay_end(text) to authenticated, service_role;
