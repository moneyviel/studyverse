-- StudyVerse: plans, 24-hour trial, payments (Razorpay) — schema studyverse in project moneyviel-apps
create table if not exists studyverse.plans (
  id text primary key check (id ~ '^[a-z0-9-]{2,40}$'),
  course text not null check (course ~ '^[a-z0-9-]{2,40}$'),
  label text not null,
  months int not null check (months between 1 and 36),
  price_inr int not null check (price_inr > 0),
  active boolean not null default true,
  sort int not null default 0
);
insert into studyverse.plans (id, course, label, months, price_inr, sort) values
  ('school-month', 'school-all', 'School · 1 month', 1, 149, 1),
  ('school-year', 'school-all', 'School · 12 months', 12, 999, 2),
  ('ca-month', 'ca-foundation', 'CA Foundation · 1 month', 1, 299, 3),
  ('ca-year', 'ca-foundation', 'CA Foundation · 12 months', 12, 1999, 4)
on conflict (id) do nothing;

alter table studyverse.profiles add column if not exists trial_at timestamptz;

create table if not exists studyverse.payments (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  plan_id text not null references studyverse.plans(id),
  amount_paise int not null check (amount_paise >= 0),
  discount_code text,
  percent smallint,
  order_id text unique not null,
  payment_id text,
  status text not null default 'created' check (status in ('created','paid','failed')),
  created_at timestamptz not null default now(),
  paid_at timestamptz,
  valid_until timestamptz
);
create index if not exists payments_user on studyverse.payments(user_id, created_at desc);

alter table studyverse.plans enable row level security;
alter table studyverse.payments enable row level security;
create policy plans_read on studyverse.plans for select to authenticated using (active or (select studyverse.is_admin()));
create policy plans_admin on studyverse.plans for all to authenticated using ((select studyverse.is_admin())) with check ((select studyverse.is_admin()));
create policy payments_read on studyverse.payments for select to authenticated using (user_id = (select auth.uid()) or (select studyverse.is_admin()));
grant select on studyverse.plans to authenticated;
grant insert, update, delete on studyverse.plans to authenticated;
grant select on studyverse.payments to authenticated;
grant all on studyverse.plans, studyverse.payments to service_role;

-- 24 hours of all school grades, once per account (first call starts it)
create or replace function studyverse.start_trial() returns jsonb language plpgsql security definer set search_path = '' as $$
declare uid uuid := auth.uid(); t timestamptz;
begin
  if uid is null then return jsonb_build_object('ok', false); end if;
  select trial_at into t from studyverse.profiles where user_id = uid;
  if t is not null then return jsonb_build_object('ok', true, 'started', t); end if;
  insert into studyverse.profiles(user_id, trial_at) values (uid, now())
    on conflict (user_id) do update set trial_at = coalesce(studyverse.profiles.trial_at, now());
  insert into studyverse.course_access(user_id, course, valid_until, note) values (uid, 'school-all', now() + interval '24 hours', 'trial')
    on conflict (user_id, course) do nothing;
  return jsonb_build_object('ok', true, 'started', now());
end $$;
revoke all on function studyverse.start_trial() from public, anon;
grant execute on function studyverse.start_trial() to authenticated;

-- is this discount code usable by the signed-in student? (the server applies it again at payment)
create or replace function studyverse.quote(p_code text) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare uid uuid := auth.uid(); c studyverse.codes%rowtype; k text := upper(trim(coalesce(p_code, '')));
begin
  if uid is null then return jsonb_build_object('ok', false, 'msg', 'Please sign in first.'); end if;
  select * into c from studyverse.codes where code = k;
  if not found or not c.active or c.kind <> 'discount' then return jsonb_build_object('ok', false, 'msg', 'This discount code is not valid.'); end if;
  if c.valid_until is not null and c.valid_until < now() then return jsonb_build_object('ok', false, 'msg', 'This code has expired.'); end if;
  if c.max_uses is not null and c.used >= c.max_uses then return jsonb_build_object('ok', false, 'msg', 'This code has been fully used.'); end if;
  if exists (select 1 from studyverse.code_uses u where u.code = k and u.user_id = uid) then return jsonb_build_object('ok', false, 'msg', 'You have already used this code.'); end if;
  return jsonb_build_object('ok', true, 'percent', c.percent);
end $$;
revoke all on function studyverse.quote(text) from public, anon;
grant execute on function studyverse.quote(text) to authenticated;

-- price for a plan and code (server function only)
create or replace function studyverse.price_for(p_user uuid, p_plan text, p_code text) returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare p studyverse.plans%rowtype; c studyverse.codes%rowtype; k text := nullif(upper(trim(coalesce(p_code, ''))), ''); pct int := 0;
begin
  select * into p from studyverse.plans where id = p_plan and active;
  if not found then return jsonb_build_object('ok', false, 'msg', 'This plan is not available.'); end if;
  if k is not null then
    select * into c from studyverse.codes where code = k and kind = 'discount' and active
      and (valid_until is null or valid_until >= now()) and (max_uses is null or used < max_uses);
    if not found or exists (select 1 from studyverse.code_uses u where u.code = k and u.user_id = p_user) then
      return jsonb_build_object('ok', false, 'msg', 'This discount code is not valid any more.'); end if;
    pct := c.percent;
  end if;
  return jsonb_build_object('ok', true, 'label', p.label, 'course', p.course, 'months', p.months,
    'price_inr', p.price_inr, 'percent', pct, 'code', k, 'amount_paise', round(p.price_inr * (100 - pct))::int);
end $$;
revoke all on function studyverse.price_for(uuid, text, text) from public, anon, authenticated;
grant execute on function studyverse.price_for(uuid, text, text) to service_role;

-- mark a payment paid and unlock the course (server function only; safe to call twice)
create or replace function studyverse.grant_paid(p_order text, p_payment text) returns jsonb language plpgsql security definer set search_path = '' as $$
declare pay studyverse.payments%rowtype; pl studyverse.plans%rowtype; cur studyverse.course_access%rowtype; base timestamptz; until timestamptz;
begin
  select * into pay from studyverse.payments where order_id = p_order for update;
  if not found then return jsonb_build_object('ok', false, 'msg', 'Order not found.'); end if;
  select * into pl from studyverse.plans where id = pay.plan_id;
  if pay.status = 'paid' then return jsonb_build_object('ok', true, 'label', pl.label, 'until', pay.valid_until); end if;
  select * into cur from studyverse.course_access where user_id = pay.user_id and course = pl.course;
  base := case when found and cur.valid_until is not null and cur.valid_until > now() and coalesce(cur.note, '') <> 'trial' then cur.valid_until else now() end;
  until := base + make_interval(months => pl.months);
  insert into studyverse.course_access(user_id, course, valid_until, note) values (pay.user_id, pl.course, until, 'paid ' || pl.id)
    on conflict (user_id, course) do update set valid_until = excluded.valid_until, note = excluded.note, granted_at = now();
  update studyverse.payments set status = 'paid', payment_id = p_payment, paid_at = now(), valid_until = until where id = pay.id;
  if pay.discount_code is not null then
    insert into studyverse.code_uses(code, user_id, course) values (pay.discount_code, pay.user_id, pl.course) on conflict do nothing;
    update studyverse.codes set used = used + 1 where code = pay.discount_code;
  end if;
  return jsonb_build_object('ok', true, 'label', pl.label, 'until', until);
end $$;
revoke all on function studyverse.grant_paid(text, text) from public, anon, authenticated;
grant execute on function studyverse.grant_paid(text, text) to service_role;
