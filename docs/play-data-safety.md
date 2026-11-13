# Knowtopia on Google Play — answers for the Play Console (9 November 2026)

Copy these answers into Play Console → **App content**. They match what the app does after
`supabase/migrations/20261113_play_ready.sql`, the Edge Functions `delete-account` and `studyverse-read`, and
`js/playready.js` are live, and what `legal/privacy.html` says. If the app changes (new SDK, ads, analytics, a new
provider, payments inside the app), update this file, the Privacy Policy **and** the Play form together.

Links you will need:

| What | URL |
|---|---|
| Privacy Policy (store listing + Data safety) | https://knowtopia.in/legal/privacy.html |
| Account deletion (web link Play asks for) | https://knowtopia.in/legal/delete-account.html |
| Terms | https://knowtopia.in/legal/terms.html |
| Support email | support@knowtopia.in |

---

## 1. App access (instructions for reviewers)

The app needs a sign-in, so choose **"All or some functionality is restricted"** and add login details.

**Proposal — please create these yourself (not created by this change):**

1. Supabase → Authentication → Users → **Add user** → "Create new user", tick **Auto Confirm User**:
   * `play-review-student@moneyviel.com` (Class 7 student)
   * `play-review-ca@moneyviel.com` (CA Foundation adult learner)
   * `play-review-parent@moneyviel.com` (parent)
   Use a long random password for each (a password manager can make one).
2. Mark them as test accounts so they never appear in Pulse numbers (SQL editor):
   `update auth.users set raw_user_meta_data = coalesce(raw_user_meta_data, '{}') || '{"demo": true}' where email like 'play-review-%@moneyviel.com';`
3. Give the two students full access so the reviewer never meets the daily limit: create a free-forever code for each
   course in Me → Owner codes (or grant `course_access` rows `school-g7` and `ca-foundation` with a far `valid_until`).
4. Sign in once as each: the student picks Class 7, the CA learner picks CA Foundation; the parent links the Class 7
   student (Parent Hub → + Add child → code). Accept the terms gate once on each.

Text for the "Instructions" box:

> Sign in with the email and password below (tap "Sign in" on the first screen). The student account shows lessons,
> practice, games, Squad (friends with preset cheers only, no chat) and Me. The parent account opens Parent Hub with one
> linked child: tap the child to see progress and the 🛡️ Controls card (friends, live game rooms, friend news).
> Account deletion: Me → Your account → "Delete my account" (please do not delete these review accounts).
> No purchases are possible in this app.

---

## 2. Ads

**Does your app contain ads?** → **No.** There is no ad SDK, no advertising ID use and no ad network.

---

## 3. Content rating (IARC questionnaire)

* **Category:** "Reference, News or Educational" (it is not a game app; games inside are learning games).
* Violence, fear, blood: **No** to every question.
* Sexuality, nudity: **No.**
* Language (profanity, crude humour): **No.**
* Controlled substances (drugs, alcohol, tobacco): **No.**
* Gambling, simulated gambling: **No.** (Snakes & Ladders uses a die to move; nothing is wagered, no prizes, no money.)
* Miscellaneous:
  * **Does the app allow users to interact or exchange content with each other?** → **Yes.** Friends are added only
    with a 6-letter friend code and must accept; they see first name, emoji avatar, weekly stars and streak, and can send
    **preset cheers only** (no free text, no chat, no photos, no links). Live game rooms are joined with a room code;
    players see name, avatar and score and can send emoji reactions only. Parents can switch friends and rooms off.
  * **Does the app share the user's current physical location with other users?** → **No.**
  * **Does the app allow users to purchase digital goods?** → **No** (the Play build shows no prices or buy buttons).
  * **Unrestricted internet / web browser?** → **No.**
  * **Is the app a news app?** → **No.**
* Expected result: **Everyone / 3+** (PEGI 3) with the interactive element **"Users Interact"**.

---

## 4. Target audience and content (Families)

* **Target age groups:** tick **6–8, 9–12, 13–15, 16–17 and 18 and over** (Class 1–12 school students and adult CA
  learners). Do **not** tick "5 and under".
* **Does the app unintentionally appeal to children?** — not asked once children are selected.
* Because children are in the target audience, the **Families policy** applies. What the app does to meet it:
  * no ads, no ad SDKs, no analytics/tracking SDKs, no advertising ID, no device identifiers, no precise or coarse
    location;
  * a parent/guardian consents at sign-up (tick box, recorded with version + time on the server); school students
    without a linked parent confirm once in the app that a parent/guardian agrees, and can invite the parent;
  * adult controls: Parent Hub → child → **🛡️ Controls** switches friends & cheers, live game rooms and friend news
    off; the **server** enforces them;
  * social features are limited to preset messages; children can **report** (preset reasons only) and **block**;
  * handwriting reading (Google Gemini) is **adults only**, checked on the server, never for school-class students;
  * account deletion in the app and on the web.
* **Families Self-Certified Ads SDK:** not needed (no ads).
* **Teacher Approved:** optional; you can apply later.
* **Android manifest (TWA build):** make sure the generated app has **no** `com.google.android.gms.permission.AD_ID`
  permission (Bubblewrap does not add it; if any library adds it, remove it with `tools:node="remove"`), and in
  Play Console → App content → **Advertising ID** answer **No**.
* **📳 Phone reminders (added 13 Nov 2026):** in the Bubblewrap/TWA config set `"enableNotifications": true`
  (notification delegation) so the app asks for Android 13+'s notification permission and shows web-push reminders.
  Data safety: the push address is **App info and performance → Other**/**Device or other IDs**, collected,
  not shared (the push service only delivers it, encrypted), purpose **App functionality**, **optional** (off until the
  student switches it on), deletable (switch off = deleted at once). Families policy: reminders are study-only,
  max one a day, never at night or school hours, parent can switch off (Parent Hub → Controls), no ads or offers.

---

## 5. Data safety form

### Overview questions

| Question | Answer |
|---|---|
| Does your app collect or share any of the required user data types? | **Yes** |
| Is all of the user data collected by your app encrypted in transit? | **Yes** (HTTPS only) |
| Which of the following methods of account creation does your app support? | **Username and password** (email + password) |
| Do you provide a way for users to request that their data is deleted? | **Yes** — in the app (Me → Your account → Delete my account; Parent Hub → Your account) and https://knowtopia.in/legal/delete-account.html |
| Delete account URL | https://knowtopia.in/legal/delete-account.html |
| Is your app compliant with the Families Policy? | **Yes** |
| Has your app been independently validated against a global security standard? | **No** |

"Shared" below is always **No**: our providers (Supabase, Brevo, Google Gemini, Cloudflare/GitHub) process data **for
us** as service providers, which Play does not count as sharing. Nothing is sold or used for ads.

### Data types

| Category → type | Collected | Shared | Ephemeral only | Required / optional | Purposes |
|---|---|---|---|---|---|
| Personal info → **Name** (first name or nickname; display name) | Yes | No | No | Required | App functionality, Account management |
| Personal info → **Email address** | Yes | No | No | Required | App functionality, Account management, Developer communications (sign-in emails; parents' weekly summary, which can be switched off) |
| Personal info → **Phone number** (school / coaching admins only, institution contact) | Yes | No | No | Optional | App functionality, Account management |
| Personal info → **Address** (school / coaching institution address only) | Yes | No | No | Optional | App functionality, Account management |
| Personal info → **Other info** (account type, board, class, stream, subjects; school class and roll number when a school adds the student) | Yes | No | No | Required | App functionality, Account management |
| Financial info → **Purchase history** (plans bought on the website, trials, free codes — shown as plan status) | Yes | No | No | Optional | App functionality, Account management |
| Photos and videos → **Photos** (CA handwritten answer, adults only, only when the learner taps "read it") | Yes | No | **Yes** (not stored; sent to Google Gemini to turn into text) | Optional | App functionality |
| Messages → **Other in-app messages** (preset cheers and emoji reactions between friends / room players) | Yes | No | No | Optional | App functionality |
| App activity → **App interactions** (lessons, quiz and test answers, stars, streaks, study minutes per day, game results, puzzle times, features used) | Yes | No | No | Required | App functionality, Analytics (owner's own aggregate dashboard; no third-party analytics), Personalisation (practice suggestions) |
| App activity → **Other user-generated content** (typed answers, notes, safety reports with a preset reason) | Yes | No | No | Optional | App functionality |

Answer **No / not collected** for: Location (approximate and precise), Web browsing, Contacts, Calendar, Audio
(the read-aloud voice runs on the phone), Files and docs, Health and fitness, App info and performance (no crash or
diagnostics SDK), Device or other IDs.

---

## 6. Other App content declarations

* **Government app:** No. **Financial features:** No (it teaches accounting; it does not offer financial services).
* **Health apps:** No. **News app:** No. **COVID-19:** No.
* **Data safety for children:** covered above.
* **Privacy policy:** https://knowtopia.in/legal/privacy.html

---

## 7. Payments in the Play build (owner + lawyer decision)

The Play build (`window.SV_PLAY`, set when the app is opened from the Android app, remembered in `sv_play`) is
**consumption only**: no prices, no "Subscribe"/"Renew"/"See plans" buttons, no plan names with prices, no link to the
pricing page, no Razorpay. Free-access codes from a school still work (they are not a purchase). Legal pages opened from
the app turn links to the pricing page into plain text. Plans bought on the website still unlock the account.
Google Play's Payments policy is strict about telling users where to buy; keep the Play build free of any "buy on our
website" message. Decide with your lawyer whether to stay with this, or add Google Play Billing later.

---

## 8. Before you press "Submit"

1. Apply `supabase/migrations/20261113_play_ready.sql` (after all earlier migrations) and run
   `supabase/tests/play_ready_test.sql` on a branch/copy first.
2. Deploy the Edge Function `delete-account` (Verify JWT **on**) and the updated `studyverse-read`.
3. Add `<script src="js/playready.js?v=59"></script>` to `index.html` (last script, after `js/owner.js`) and to the
   `sw.js` precache list; bump the cache version; also precache `legal/delete-account.html`.
4. Create the reviewer accounts (section 1).
5. On a real phone with the Play build: sign up as a child (tick box), accept the terms gate, turn a control off in
   Parent Hub, report and block a test friend, then delete a throw-away account.
