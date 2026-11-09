# Knowtopia legal: implementation proposal (v2.0, 9 November 2026)

This file is a **proposal**. Nothing below has been applied to the database or app yet. The legal pages (`legal/*.html`)
already describe the target behaviour, so the items marked **MUST** should be built before relying on those pages
(and well before the DPDP Rules' main date, **13 May 2027**).

Pattern borrowed from Salonzy (`mysalon-app`: `terms_acceptances` table, `terms_status()` / `accept_terms()` RPCs,
`TermsGate.jsx`, Super Admin "Terms & Consent" with important vs small change and CSV export; grievance details kept
in one settings place). Adapted here for children, parents and schools.

---

## 1. What is recorded today vs what is needed

| Today | Gap |
|---|---|
| Sign-up tick box "I am 18 or older … parent or guardian" (js/cloud.js, pricing/index.html) | Not stored. No version, no time, no record of *who* consented for *which* child. |
| Onboarding footer "By continuing you agree…" (js/legal.js) | Not a consent. Fine as a reminder only. |
| School bulk upload creates accounts with email pre-confirmed | No record that the school obtained parental consent. |
| Handwriting reading (Gemini) "off for under-18" | Must be enforced **on the server** (`studyverse-read`), not only in the UI. |
| No in-app account deletion | Google Play requires in-app deletion **and** a web link to request deletion. |
| No parent switch for friends / live rooms | Google Play Families policy requires adults to be able to manage social features for children. Pages promise "email us"; build the switch. |

## 2. Database (new migration, e.g. `supabase/migrations/2026111x_legal_consent.sql`)

```sql
-- one row: current policy version, shown to users when it changes
create table if not exists studyverse.legal_settings (
  id int primary key default 1 check (id = 1),
  version text not null default '2.0',            -- matches SV_LEGAL.version in legal/legal.js
  effective_on date not null default date '2026-11-09',
  summary text,                                   -- "What changed", shown on the gate
  needs_reaccept boolean not null default false   -- true only for IMPORTANT changes
);

-- every acceptance / consent, append-only (proof under DPDP Rule 10 and for disputes)
create table if not exists studyverse.consents (
  id           bigint generated always as identity primary key,
  subject_id   uuid not null references auth.users(id) on delete cascade, -- whose data (the learner)
  actor_id     uuid references auth.users(id) on delete set null,         -- who agreed (self, parent, school admin)
  kind         text not null check (kind in ('terms','parental','school_upload','social','ai_reading','marketing')),
  version      text not null,
  granted      boolean not null default true,      -- false = withdrawal (a new row; never update old rows)
  how          text not null check (how in ('signup','gate','parent_hub','school_upload','existing','support')),
  verify       text,                                -- Rule 10 method: 'email','payment','digilocker','school','known_adult'
  institution_id uuid,                              -- for school uploads
  user_agent   text,
  ip_hash      text,                                -- sha256(ip || secret), never the raw IP
  at           timestamptz not null default now()
);
create index on studyverse.consents (subject_id, kind, at desc);
alter table studyverse.consents enable row level security;   -- read own (subject or actor); writes only via RPCs

-- age band, decided at sign-up; never a full date of birth
alter table studyverse.profiles add column if not exists age_band text
  check (age_band in ('under18','adult')) ;
alter table studyverse.profiles add column if not exists social_off boolean not null default false; -- friends + rooms
```

RPCs (all `security definer`, `set search_path = ''`, like the existing ones):

* `legal_status()` → `{ version, summary, effective_on, accepted, needs_parent }`. `accepted` = latest `terms` row for
  `auth.uid()` has `version` = current, or `needs_reaccept` is false. `needs_parent` = learner is `under18` and the
  current version needs fresh parental consent.
* `accept_terms(p_version, p_agent)` → refuses if `p_version` is not current (same guard as Salonzy). Adults only.
* `parent_consent(p_child uuid, p_version, p_verify)` → caller must be a **linked parent** of `p_child`; writes a
  `parental` row (actor = parent, subject = child).
* `withdraw_consent(p_subject uuid, p_kind)` → subject (adult) or linked parent; writes `granted=false`; for
  `terms`/`parental` this starts account deletion (see 6).
* `set_social(p_child uuid, p_off boolean)` → linked parent or school admin; friends/rooms RPCs check `social_off`.
* Owner only: `sa_publish_terms(p_summary, p_important)`, `sa_terms_report()`, `sa_consents_export()` (CSV),
  copied from Salonzy's pattern.
* Sign-up trigger on `auth.users` (like Salonzy `tg_terms_on_signup`): reads `raw_user_meta_data` →
  `{ age_band, consent_version, for_child }` passed in `supabase.auth.signUp({ options: { data } })` and writes the
  `terms` row (and a `parental` row when `for_child`). Wrap in `begin … exception when others then null` so sign-up
  never fails.
* Existing users: insert `how='existing'` rows for version 1.1, then show the gate once for 2.0.
* `institution-bulk` function: each upload must carry `consent_confirmed: true` from the admin (tick box: "Our school
  has informed parents and has their consent where required"). Write one `school_upload` row per student created
  (actor = school admin, verify = 'school').

## 3. Sign-up flow (js/cloud.js `mode === 'up'`, pricing/index.html)

1. Ask **"Who is this account for?"** → *Me (18 or older)* / *My child (under 18)*. Store `age_band`.
2. Replace the single tick box with:
   * adult: "I am 18 or older and I accept the Terms (v2.0) and Privacy Policy." 
   * for a child: "I am this child's parent or guardian, I am 18 or older, and I consent to Knowtopia processing my
     child's data as the Privacy Policy describes. I accept the Terms (v2.0) for my child."
3. Send `consent_version` = `SV_LEGAL.version` in the sign-up metadata (2.). Keep the existing "please tick" error.
4. **Better (recommended) for children:** parent signs up as Parent first and uses Parent Hub → "Add child" to create
   the child's login. Then actor (parent) and subject (child) are both real accounts and Rule 10 "verify the parent"
   can use the parent's verified email / payment.
5. DPDP Rule 10 (from 13 May 2027): add one verification step for the consenting parent, e.g. (a) a parent who has
   paid by Razorpay = known adult, or (b) DigiLocker age token, or (c) email confirmation + declaration (lowest).
   **Lawyer to confirm which is enough.**

## 4. In-app acceptance gate (like Salonzy TermsGate)

* After sign-in, `js/cloud.js` calls `legal_status()` (cache 1 day). If `accepted` is false:
  * **adult / parent:** full-screen card: "We've updated our Terms", version + date, *What changed* summary, links
    to Terms / Privacy / Refunds, tick box, **Accept & continue**, or "log out / write to support@knowtopia.in".
  * **child:** friendly card: "Our rules changed. Please ask your parent to say OK in Parent Hub." The app keeps
    working in a limited mode (lessons only, no friends/rooms) for 14 days, then pauses until the parent accepts.
    A linked parent gets an email + a Parent Hub banner with the same accept card (`parent_consent`).
* Small changes (`needs_reaccept = false`): no gate; only the change log and "Version" pill update.
* Keep `js/legal.js` first-launch notice as is (it is informational).

## 5. Feature gates to enforce on the server

* `studyverse-read` (Gemini): refuse unless caller's `age_band = 'adult'` and course is CA. Return a friendly error.
* Friends / cheers / rooms RPCs: refuse when `social_off`. Add a toggle in Parent Hub controls and in the school
  admin screen (per class).
* Weekly parent email: already has unsubscribe; record `marketing`-type consent only if offers are ever added
  (adults only).
* Owner analytics: keep it built only from aggregate queries; do not add any third-party analytics/ads SDK. Do not
  add per-child drill-down outside support cases.

## 6. Rights requests, deletion, retention

* **Delete account** button: Me → Account → "Delete my account" (adults), Parent Hub → child → "Delete child's
  account" (parent). Calls an edge function that deletes `auth.users` row (cascades) after a 7-day undo window;
  payments kept (needed for tax) with the user id nulled. Also a public page/form for Play's "web deletion link"
  (could be `legal/contact.html#delete` + email until a form exists).
* **Download my data**: RPC returning JSON of profile, progress, consents, payments.
* **Retention jobs** (pg_cron daily): `live_cleanup()` (exists), cheers 30 days (exists, on read), pilot_requests
  > 12 months, child_codes expired, inactive accounts 3 years (email 30 days before), consent rows 3 years after
  account deletion, security logs ≥ 1 year (check Supabase log retention on your plan).
* **Report button** on a friend card / room player → inserts into a `reports` table + emails the owner.

## 7. Renaming the app

1. Edit `SV_LEGAL.brand` and `SV_LEGAL.brandHTML` in `legal/legal.js` (all pages update when JavaScript runs).
2. Update the plain-text fallback (for search engines / no-JS):
   `sed -i 's/Knowtopia/NewName/g' legal/*.html` (check `Know<span>topia</span>` in the header too).
3. Owner details (address, GSTIN, grievance phone, version, date) are also only in `SV_LEGAL`; for the static
   fallback text run the same kind of replace for the `[OWNER TO FILL…]` strings.

## 8. Other small follow-ups

* `sw.js` precache list does not yet include the new pages (`children`, `parents`, `schools`, `changes`). They work
  online; add them to the list when sw.js is next edited (bump its cache version).
* `pricing/index.html` FAQ already says "7 days of your first purchase" — matches the Refund policy.

## 9. Google Play (planned listing)

* **Payments policy risk (owner + lawyer):** Play's Payments policy generally requires Google Play Billing for
  digital content bought *inside* a Play-distributed app, and restricts linking out to a website to pay. Options:
  (a) Play build has no buy buttons/links (consumption-only, "reader"-style), (b) use Play Billing / user-choice
  billing in India for the Play build. Decide before submitting.
* **Families policy:** target audience includes children → no ad SDKs, no AAID/device identifiers, no precise
  location; privacy policy link in listing and in app; adult controls for social features (section 5); in-app
  online-safety reminder before first friend add.
* **Data safety form (suggested answers):** collects *Personal info* (email, name), *App activity* (in-app actions,
  progress), *App info & performance* (crash/diagnostic logs if any), *Photos* (CA handwriting, adults only,
  not stored, shared with Google for processing), *Financial info* (purchase history; payments processed by
  Razorpay, on the website). Encrypted in transit: yes. Deletion request: yes. Not shared for ads; not sold.
* **Non-trader** status is an EU Digital Services Act declaration; it does not change Indian law duties (Consumer
  Protection / E-Commerce Rules still require seller details on the website).

## 10. Owner must fill / decide

* `[OWNER TO FILL]` in `legal/legal.js` → full postal address with PIN, Grievance Officer phone, GSTIN (or "Not
  registered for GST").
* B2B payment terms (refunds.html §6, schools.html §7).
* **GST:** prices say "+ GST as applicable". If you are not GST-registered you must **not** charge GST — either
  register or show prices as final. Turnover threshold for services is ₹20 lakh, but check with your CA.
* Legal form: pages say "individual (sole proprietor) trading as MoneyViel". Change if MoneyViel is registered
  differently (firm, LLP, company).
* Retention choices in privacy.html §13 (3-year inactivity deletion, 2-year support emails, 12-month pilots).
* 7-day refund on **first** purchase only (as the pricing FAQ says) vs every purchase.
* Gemini free tier: Google may use free-tier inputs to improve products and humans may review them. Consider the
  paid tier (no such use) before scaling, then update privacy.html §7.
* Free-user liability cap (₹1,000) in liability.html.

## 11. Needs a lawyer's review

1. Whether in-app progress tracking, study-time tracking, streaks and teacher "early warnings" count as
   "tracking or behavioural monitoring of children" under DPDP s.9(3), and whether any Fourth Schedule exemption
   (educational institutions, Part A) helps for **school** accounts only. B2C accounts likely get no exemption.
2. Rule 10 verifiable parental consent: which method is enough for Knowtopia.
3. School = Data Fiduciary / Knowtopia = Data Processor split, and the school agreement / DPA wording
   (schools.html), including breach notice within 24 hours.
4. Whether Knowtopia is an "intermediary" under the IT Rules 2021 (minimal user content) and the content-removal
   timelines promised in contact.html.
5. E-Commerce Rules 2020 duties for a seller of its own digital services (seller details, grievance officer
   display), and the refund/cancellation wording.
6. Liability cap and indemnity enforceability against consumers and parents of minors.
7. Cross-border transfer wording (Brevo EU, Google, Cloudflare/GitHub) and CERT-In 6-hour reporting duty.
8. Copyright approach for NCERT/ICAI syllabus references and any quoted material.
9. Google Play payments approach (section 9).
