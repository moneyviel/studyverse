# State boards: Phase 2 plan (own-syllabus boards)

Status: plan only. No content is built. Researched 2026-11-09 for the 2026-27 session.
Phase 1 (NCERT-mapped boards) is in `content/boards.json`.

**Chapter counts below are estimates** (typical book sizes for each stage). They are not counted from the official chapter lists. Check them against the official PDFs before building.

## 0. Quick wins first (cheap, large reach)

Do these before any own-syllabus board. Each one opens more students per hour of work than a new syllabus.

1. **Previous-edition NCERT Class 9 (Beehive/Moments, Mathematics, Science, Contemporary India-I, India and the Contemporary World-I, Democratic Politics-I, Economics).**
   - UP Board ([UPMSP 2026-27 list](https://www.freepressjournal.in/education/up-board-warns-against-unauthorized-textbooks-releases-authorised-publishers-and-books-price-list-for-202627)), MP Board ([careers360](https://school.careers360.com/boards/mpbse/mp-board-class-9-syllabus-2026-27)) and Goa ([careers360](https://news.careers360.com/goa-board-ncert-textbooks-for-classes-9-10-11-academic-year-2027-28-gbshse-nep-2020-ncfse/amp)) still use these books in 2026-27. Most other NCERT states probably do too.
   - Estimated size: about 70 chapters (English 20, Maths 12, Science 12, Social Science about 22).
   - The repo has no git history, and the `/tmp/srv` copy also holds only the new edition, so this needs a fresh build.
   - Add it as a separate course key (for example `g9-ncert2023`) and point the Class 9 entries in `boards.json` at it.
2. **Economics pairing for state boards.** All four NCERT economics books already exist in g11 and g12. UP teaches Statistics + Indian Economic Development in Class 11 and Micro + Macro in Class 12.
   - Support a per-board subject remap in `boards.json` (for example `{"source":"ncert","chapters":["g11/economics:stats","g12/economics:ied"]}`).
   - This unlocks Economics for UP and the other boards without writing new content.
3. **Verify-only boards.** Find the official 2026-27 book list and flip the matching entries to `ncert`; no new content is needed.

   | Board | What to verify |
   |---|---|
   | Bihar (BSEB) | Class 10 Maths/Science; Class 11-12 PCMB, Commerce, Arts |
   | Gujarat (GSHSEB) | Class 9-12 Maths/Science, which moved to the NCERT syllabus from 2016-17 ([collegedekho](https://www.collegedekho.com/news/introduction-of-ncert-syllabus-from-class-6-receives-positive-response-in-gujarat-1560)) |
   | Haryana (BSEH), HP (HPBOSE), Chhattisgarh (CGBSE), Punjab (PSEB), J&K (JKBOSE) | Class 10-12 book lists |
   | Rajasthan, MP, Jharkhand | English and Social Science in Class 10; Arts in Class 11-12. Science/Maths are already mapped. |
   | Uttarakhand, Rajasthan, MP | Which NCERT edition Classes 1-8 use in 2026-27. MP took the new Class 7 books only in 2026-27 ([FPJ](https://www.freepressjournal.in/bhopal/half-the-academic-session-over-teachers-now-being-trained-for-new-class-7-syllabus)). |
   | AP SSC (Class 10) | Reported as studied "under NCERT syllabus" ([Sakshi](https://www.sakshipost.com/news/education/ap-intermediate-syllabus-2025-key-changes-ncert-cbse-syllabus-academic-year-390590)), but AP prints its own bilingual books. Compare the chapters. |
   | Assam, Tripura | Class 11-12 lists, and whether Class 9 uses the new NCERT books |

4. **Language books.** Several NCERT states use their own Hindi books (UP, MP, Bihar). These are small books, about 15-20 chapters per class. Building UP Hindi for Classes 10 and 12 first covers the largest Hindi-medium market.

## 1. Own-syllabus boards

Market size uses approximate state school enrolment (UDISE+ order of magnitude), and the Hindi belt is excluded. Effort is low, medium or high: it depends on book stability, the share of English-medium students and the number of subjects.

| # | Board | Classes / subjects | Official textbook source | Est. chapters (1-12) | Notes |
|---|---|---|---|---|---|
| 1 | **Maharashtra** SSC/HSC (MSBSHSE), Balbharati books | 1-10: First Language, English, Hindi, Maths (Part 1 Algebra, Part 2 Geometry in 9-10), Science & Technology (Parts 1 and 2 in 9-10), History & Political Science, Geography, EVS (1-5). 11-12: Physics, Chemistry, Biology, Maths & Statistics (Parts 1 and 2), Book-Keeping & Accountancy, OCM, Economics, SP, History, Geography, Political Science, Psychology, Sociology | [ebalbharati.in](https://ebalbharati.in/main/aboutus.html) (Balbharati e-books) | about 1,100 | **Books are being replaced.** Revised books (made after reviewing NCERT material) phase in: Class 1 in 2025; 2, 3, 4, 6 in 2026; 5, 7, 9, 11 in 2027; 8, 10, 12 in 2028 ([careers360](https://news.careers360.com/maharashtra-implement-cbse-curriculum-up-class-12-2028-confirms-education-minister-dada-bhuse/amp); new books for 1-6 unveiled June 2026, [FPJ](https://www.freepressjournal.in/mumbai/maharashtra-cm-devendra-fadnavis-dy-cms-eknath-shinde-sunetra-pawar-unveil-new-balbharati-textbooks-for-classes-1-to-6-at-mantralaya)). Build the stable exam years first: SSC Class 10 and HSC Class 12 (current books until 2028), then the new 1-4 and 6 books. Check each new book against NCERT; some may map partly. |
| 2 | **Tamil Nadu** Samacheer Kalvi (DGE TN) | 1-10: Tamil, English, Maths, Science, Social Science (terms 1-3 in 1-9). 11-12: Physics, Chemistry, Biology/Botany/Zoology, Maths (Vol 1 and 2), Computer Science, Accountancy, Commerce, Economics, History, etc. | TN Textbook & Educational Services Corp: [textbookcorp.tn.gov.in](https://www.textbookcorp.tn.gov.in/) / [textbooksonline.tn.nic.in](https://www.india.gov.in/website-tamil-nadu-textbook-corporation) | about 1,000 | Books stable since the 2018-20 revision. Large English-medium share, so **best value per chapter**. Start with Classes 10, 12 and 11, then 9. |
| 3 | **Karnataka** SSLC (KSEAB, KTBS books) | 1-10: Kannada, English, Hindi, Maths, Science, Social Science. PUC 11-12 science is already NCERT-mapped (Phase 1); add Accountancy, Business Studies, History, Political Science, Sociology, Geography, Economics. | KTBS textbooks for 2026-27 ([newsable](https://newsable.asianetnews.com/karnataka-news/karnataka-schools-to-receive-2026-27-textbooks-before-reopening-ktbs-articleshow-2ab92pw)) | about 650 (1-10) + about 120 (PUC commerce/arts) | Class 9-10 Maths/Science were historically NCERT-derived: diff them against NCERT before building. |
| 4 | **West Bengal** WBBSE (Madhyamik) / WBCHSE (HS) | 1-10: Bengali, English (Bliss / Blossoms), Maths (Ganit Prakash), Life Science, Physical Science, History, Geography. 11-12: semester system (WBCHSE). | WBBSE textbook list ([PW](https://www.pw.live/wbbse/exams/wbbse-madhyamik-textbooks-2024)); official portal wbbse.wb.gov.in | about 950 | Mostly Bengali-medium, so English content reaches fewer students. **High effort** (needs Bengali for real reach). Do after TN/Karnataka. |
| 5 | **Andhra Pradesh** SSC (BSEAP) | 1-10: Telugu, English, Hindi, Maths, Physical Science, Biological Science, Social Studies. Intermediate science is already mapped (Phase 1). | SCERT AP / cse.ap.gov.in (portal; confirm the URL) | about 600 | AP moved to NCERT-aligned bilingual books, so first try the **verify-only** route (section 0). |
| 6 | **Telangana** SSC (BSE Telangana) / TGBIE | 1-10: Telugu, English, Hindi, Maths, Physical Science, Biological Science, Social Studies. Intermediate: Telugu Akademi books. | SCERT Telangana e-textbooks ([teachersbadi](https://teachersbadi.in/e-books-e-text-books-scert-telangana-1st-class-to-10th-class-ssc-new-text-books/)); official scert.telangana.gov.in | about 650 + Intermediate about 250 | Classes 1-10 have bilingual (Telugu/English) books, which cuts translation effort. |
| 7 | **Kerala** SSLC (KBPE) | 1-10: Malayalam I and II, English, Hindi, Maths, Physics, Chemistry, Biology (8-10), Basic Science (1-7), Social Science I and II, ICT. HSE science is already mapped (Phase 1). | SCERT Kerala; new books for 1, 3, 5, 7, 9 in 2024 ([onmanorama](https://www.onmanorama.com/career-and-campus/top-news/2024/06/03/new-textbooks-kerala-schools-available-online.html)) and 2, 4, 6, 8, 10 in 2025. 2026-27 revised Plus One books ([hsslive](https://www.hsslive.in/2026/04/class-11-revised-text-book.html)). | about 700 | Books are freshly revised, so they will stay stable. English-medium share is moderate. |
| 8 | **Gujarat** (GSHSEB) | 1-12 Gujarati-medium books from GSSTB | GSSTB textbook portal (confirm the URL) | about 900 | Try **verify-only** first for Maths/Science 9-12 (section 0). |
| 9 | **Odisha** BSE (Class 10) / CHSE (+2) | 1-10: Odia, English, Hindi/Sanskrit, Maths (Algebra/Geometry), Physical Science, Life Science, History & Political Science, Geography & Economics. +2: CBSE-aligned syllabus but Odisha's own books ([Sambad](https://sambadenglish.com/cbse-syllabus-for-odisha-plus-two-science-course-from-this-year)). | BSE Odisha / CHSE portals (confirm the URLs) | about 750 | Odisha is rolling out 55 revised textbooks for Classes 1-8 from 2026-27 ([OdishaTV](https://odishatv.in/odisha/odisha-to-roll-out-55-revised-textbooks-for-classes-iviii-from-202627-11009809)). Wait a session for 1-8. |
| 10 | **Punjab** PSEB, **Haryana** BSEH, **Chhattisgarh** CGBSE, **HP** HPBOSE, **J&K** JKBOSE | Classes 1-12 | Board portals | — | Verify first (section 0). Most are probably NCERT-derived for Classes 9-12. |
| 11 | **NE boards**: Manipur BOSEM/COHSEM, Meghalaya MBOSE, Mizoram MBSE, Nagaland NBSE | Classes 1-12 | Board portals | — | Small markets and largely NCERT-based. Verify only. |

## 2. Recommended build order

1. Section 0, item 1: the old-edition NCERT Class 9 course. It unlocks Class 9 for UP, MP, Goa and probably most NCERT states. This is the biggest single win.
2. Section 0, item 2: the economics remap (app change only).
3. Section 0, item 3: verify-only boards. Start with Bihar and Gujarat (largest markets), then Haryana, Punjab, HP, CG and J&K.
4. Tamil Nadu: Classes 10, 12, 11, then 9. Stable books and a strong English-medium share.
5. Maharashtra: SSC Class 10 and HSC Class 12 on the current books, then the new Classes 1-4 and 6.
6. Karnataka SSLC: Classes 10 and 9 first, after diffing Maths/Science against NCERT. Then PUC commerce/arts.
7. AP / Telangana SSC (after the AP verify step), using the bilingual books.
8. Kerala SSLC, Classes 10 and 9.
9. West Bengal Madhyamik (Class 10 first). Needs Bengali.
10. Odisha, after the revised 1-8 books settle.

## 3. Build notes

- Reuse the existing pipeline (`CONTENT_GUIDE.md`). Own-syllabus content goes under board-specific keys, for example `content/boards/<board-id>/g<N>/<subject>.json`. Add `{"source":"own","status":"live","path":...}` in `boards.json`.
  - The app currently reads only `"ncert"`. Supporting `"own"` + `"live"` means changing `subjectData()` to load from the board path.
- Keep exam-pattern cards (`exam_info`) to facts confirmed from an official circular or news report, with the session year.
- Build for exam classes first (10 and 12). That is where students search for help, and where paid conversion is highest.
