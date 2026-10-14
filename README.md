# فضائل العمرة — Fazā'il of 'Umrah

A dedicated, comprehensive dataset and interactive local web application showcasing the **Prophetic Virtues and Merits of 'Umrah (Minor Pilgrimage)**, scraped directly from [Sunnah.com](https://sunnah.com).

**Live website:** [https://firofame.github.io/fazail-umrah/](https://firofame.github.io/fazail-umrah/)

GitHub Pages serves the repository root from the `main` branch. The
`.nojekyll` file keeps the site as plain static files. Pushed updates to
`main` are deployed automatically; rebuild `index.html` before pushing
changes to the dataset.

---

## 🌟 Key Features

1. **Complete Authentic Dataset:**
   - 66 Prophetic Ahadith across **12 major collections**:
     - *Sahih al-Bukhari*, *Sahih Muslim*, *Jami` at-Tirmidhi*, *Sunan an-Nasa'i*, *Sunan Ibn Majah*, *Sunan Abi Dawud*, *Musnad Ahmad*, *Al-Mu'jam al-Kabir (at-Tabarani)*, *Riyad as-Salihin*, *Mishkat al-Masabih*, *Bulugh al-Maram*, and *Sahih al-Targhib wa al-Tarhib*.
   - Includes **full Arabic text** (with *tashkīl* and *isnād* chains), **English translations**, scholarly **authenticity grades** (*Sahih*, *Hasan*), in-book references, and direct permalinks.

2. **Categorized into 20 Thematic Virtues:**
   - **Expiation of Sins Between Two Umrahs** (*Kaffārah limā baynahumā* / كفارة لما بينهما)
   - **Removal of Poverty & Sins via Alternating Hajj & Umrah** (*Nafy al-Faqr wal-Dhunūb* / نفي الفقر والذنوب)
   - **'Umrah in Ramadan = Hajj with the Prophet (ﷺ)** (*'Umrah fī Ramaḍān ta'dilu Ḥajjah* / عمرة في رمضان تعدل حجة معي)
   - **The Honored Delegation of Allah** (*Wafdullāh* / وفد الله)
   - **Jihad for Women, the Elderly, and the Weak** (*Jihād lā qitāla fīh* / جهاد لا قتال فيه)
   - **Reward Scales with Hardship & Spending** (*'Alā qadri naṣabik wa-nafaqatik* / على قدر النصب والنفقة)
   - **Virtues of Tawaf & Touching the Sacred Corners** (*Faḍl aṭ-Ṭawāf wal-Istilām* / فضل الطواف واستلام الركنين)
   - **Supplication & Blessed Return** (*Du'ā' ar-Rujū'* / دعاء وفضل الرجوع)
   - **Universal Chorus of the Talbiyah (Cosmic Resonance)** (*Faḍl at-Talbiyah* / عظيم فضل التلبية ومشاركة الكائنات)
   - **Perpetual Reward for Dying on Umrah or in Ihram** (*Ajr al-Mawt fī Sabīl al-'Umrah* / ثواب من مات معتمراً أو محرماً)
   - **Seeking the Supplication of the Umrah Pilgrim** (*Talab ad-Du'ā' min al-Mu'tamir* / طلب الدعاء من المعتمر)
   - **Threefold Mercy for Shaving the Head (Halq)** (*Tathlīth ar-Raḥmah lil-Muḥalliqīn* / فضل الحلق وتثليث الرحمة للمحلقين)
   - **Sa'i between Safa and Marwa & Tawaf Freeing Slaves** (*Faḍl as-Sa'ī wal-Iḥṣā'* / فضل السعي وإحصاء الطواف كعتق الرقاب)
   - **Entering Ihram from Masjid al-Aqsa** (*Al-Ihlāl min al-Masjid al-Aqṣā* / الإهلال بالعمرة من المسجد الأقصى)
   - **Heavenly Origin & Testimony of the Black Stone** (*Faḍl al-Ḥajar al-Aswad* / أصل الحجر الأسود من الجنة وشهادته)
   - **Miracle, Nourishment & Cure of Zamzam Water** (*Barakat Mā' Zamzam* / بركة ماء زمزم والشفاء به)
   - **100,000x Multiplied Prayer in Masjid al-Haram** (*Muḍā'afat aṣ-Ṣalāh* / مضاعفة الصلاة بمائة ألف صلاة)
   - **The Sunnah of Four 'Umrahs in Dhu al-Qa'dah** (*Sunnat 'Umrat an-Nabī ﷺ* / سنة عمرة النبي ﷺ في ذي القعدة)
   - **Spending on Pilgrimage Multiplied 700-Fold** (*An-Nafaqah fī Sabīlillāh* / النفقة بسبعمائة ضعف)
   - **Deeds Equivalent to the Complete Reward of Umrah** (*A'māl Ta'dilu Ajr 'Umrah* / أعمال صالحة تعدل أجر عمرة تامة)

3. **Modern Local Web Viewer (`index.html`):**
   - **Offline-ready & Self-contained**: Embedded JSON dataset, no internet or server required.
   - **Real-time instant search**: Search across English, Arabic, Narrator, or Hadith reference.
   - **Category & Collection filter pills**: Filter by specific virtue or book.
   - **Bookmarking**: Save your favorite hadiths locally using browser storage.
   - **One-click Copy**: Easily copy formatted Arabic and English text with reference citation to your clipboard.
   - **Dark / Light mode**: Responsive, elegant theme with Amiri Arabic typography.

---

## 📁 Project Structure

```text
fazail-umrah/
├── index.html            # Standalone interactive web viewer (double-click to open)
├── build_web.py          # Generator script to inject data into index.html
├── scrape.py             # Python scraper to fetch fresh data from Sunnah.com
├── serve.sh              # Quick script to run a local dev server
├── README.md             # Project documentation
└── data/
    ├── fazail_umrah.json # Complete structured JSON database (66 hadiths across 20 categories)
    ├── fazail_umrah.csv  # Spreadsheet-compatible CSV format
    └── FAZAIL_OF_UMRAH.md# Full markdown compendium with Arabic and English
```

---

## 🚀 How to Use

### 1. Open the Web Viewer
You can view the interactive web app in any browser:

**Option A (Direct):**
Simply double-click `index.html` or run:
```bash
open index.html
```

**Option B (Local Web Server):**
```bash
./serve.sh
```
or:
```bash
python3 -m http.server 3000
```
Then visit [http://localhost:3000](http://localhost:3000).

---

### 2. Updating or Re-Scraping Data
To scrape fresh records from Sunnah.com:
```bash
python3 scrape.py
```
This updates the files in the `data/` directory.

To rebuild `index.html` with the updated dataset:
```bash
python3 build_web.py
```

---

### 3. Reviewed Malayalam Narration

The twenty-two chapter files in `data/tts/` contain an introduction, twenty
thematic chapters, and a conclusion. They are a Malayalam **meaning-summary**,
not a complete translation of all 66 records or an Arabic recitation. The
combined script is `data/tts/fazail_umrah_malayalam_full.txt`.

The original eight chapters were checked against the stored Arabic and English sources.
Corrections remove the unsupported lifespan claim, distinguish Bukhari's
Hajj-only wording from Ibn Majah's Hajj-and-Umrah wording, and remove kissing
both corners and two prayer units from the cited tawaf report. Hasan reports
are no longer described indiscriminately as Sahih. The return supplication
is explicitly introduced as a Malayalam meaning, and the travel supplication
includes its previously omitted opening and final request for protection.
Secondary reports without a verified primary reference/grade were omitted.
The unrelated `nasai:2117` and `mishkat:2530` records in the Ramadan category
are not used; the dataset is unchanged by audio generation.

All 29 newly added records are accounted for in
`data/tts/new_hadith_review.json`, with verified primary-page links, grades,
wording corrections, and narration usage. Twelve new thematic chapters
cover these additions; some are explicitly source-review cautions rather
than endorsements of a promised reward. Their audio follows chapter eight
and precedes the existing conclusion, whose filename remains unchanged.

The new narration uses the actual Ibn Majah 2956 wording (tawaf **and two
rak'ahs**, graded Hasan), does not attribute the cure addition to Muslim's
Zamzam report, and does not say all four prophetic Umrahs were completed
in Dhu al-Qa'dah. Darussalam/Al-Albani's weak grades for the pilgrim-dua,
Aqsa-ihram, and sunrise-reward reports are stated explicitly, including
al-Tirmidhi's differing assessments where applicable. Four secondary
records with unverified primary references are not used as evidence;
the perpetual-reward, seventy-slaves, seven-hundred-fold, and added-Umrah
claims are not affirmed. Dataset grades/quotations are retained separately
as provenance and may differ from the verified narration.

Validate locally, without contacting any speech or translation provider:

```bash
../google-docs-tts/.venv/bin/python generate_malayalam.py --validate-only
../google-docs-tts/.venv/bin/python -m unittest discover -s tests
```

Generate fresh audio using the two sibling projects:

```bash
../google-docs-tts/.venv/bin/python generate_malayalam.py
```

To generate the new/changed chapters while retaining existing recordings
whose script and published MP3 checksums match the previous manifest:

```bash
../google-docs-tts/.venv/bin/python generate_malayalam.py --reuse-verified
python3 build_web.py
```

`--reuse-verified` explicitly permits reuse of an older renderer's output
after script/checksum/media verification; it records that provenance.
Without that flag, all chapters are rendered afresh (or resumed from the
matching renderer-keyed cache). The web viewer includes a full player,
MP3/Opus downloads, and chapter players in manifest order.

This reuses `transcribe/src/translate.py` for Malayalam/script/format checks
and `google-docs-tts/tts.py` for Google Docs speech generation, MP3
concatenation, and mono 48 kHz Opus encoding. The saved Google login and
service-account credentials configured in the TTS project are required.
The configured temporary Google document is replaced during generation;
the narration text is sent to Google. No translation API is called, and the
medical-book-specific translation prompt in `transcribe` is not applied to
these hadiths.

Completed outputs replace the existing chapter and full recordings in
`audio/` only after all new files decode successfully and their codecs and
combined duration pass checks. A content-and-renderer-keyed cache permits
interrupted generation to resume without reusing older, unrelated audio.
`audio/malayalam_manifest.json` records text/audio hashes, source references,
stored and reviewed grades, narration usage, reuse provenance, validation
results, and durations.

**Full recording:** `audio/fazail_umrah_malayalam_full.mp3` and
`audio/fazail_umrah_malayalam_full.ogg`.

These checks establish script provenance and playable, complete media;
they do not certify pronunciation. A Malayalam-speaking listener should
review religious names and honorifics before publication. The sibling
`transcribe` project provides script checks, not speech recognition;
no independent pronunciation or audio-to-text accuracy certification is
claimed. Newly reviewed grades are documented separately from stored
dataset labels; neither implies scholarly consensus.

---

## 📜 Example Record (`fazail_umrah.json`)

```json
{
  "id": "bukhari:1773",
  "collection": "Sahih al-Bukhari",
  "reference": "Sahih al-Bukhari 1773",
  "category": "Expiation of Sins Between Two Umrahs",
  "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
  "book_english": "`Umrah (Minor pilgrimage)",
  "chapter_english": "Chapter: 'Umra and its superiority",
  "chapter_arabic": "باب وُجُوبِ الْعُمْرَةِ وَفَضْلِهَا",
  "grade": "Sahih (Sahih al-Bukhari - Authentic)",
  "arabic_text": "حَدَّثَنَا عَبْدُ اللَّهِ بْنُ يُوسُفَ... أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ: الْعُمْرَةُ إِلَى الْعُمْرَةِ كَفَّارَةٌ لِمَا بَيْنَهُمَا، وَالْحَجُّ الْمَبْرُورُ لَيْسَ لَهُ جَزَاءٌ إِلاَّ الْجَنَّةُ",
  "english_text": "Narrated Abu Huraira: Allah's Messenger (ﷺ) said, \"(The performance of) `Umra is an expiation for the sins committed (between it and the previous one). And the reward of Hajj Mabrur is nothing except Paradise.\"",
  "sunnah_url": "https://sunnah.com/bukhari:1773"
}
```

---

## 🤲 Credits
- Hadith texts, chains, translations, and numbering courtesy of [Sunnah.com](https://sunnah.com).
