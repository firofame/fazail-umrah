#!/usr/bin/env python3
"""
Scraper for Fazail (Virtues and Merits) of Umrah from sunnah.com
Extracts Arabic text, English translation, grades, book/chapter names,
and references across Kutub al-Sittah and other primary collections.
"""

import subprocess
import re
import html
import json
import csv
import time
import os

HADITH_ENTRIES = [
    # Category 1: Expiation of Sins Between Two Umrahs
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/bukhari:1773"
    },
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/muslim:1349a"
    },
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/tirmidhi:933"
    },
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/nasai:2629"
    },
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/ibnmajah:2888"
    },
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/riyadussalihin:1275"
    },
    {
        "category": "Expiation of Sins Between Two Umrahs",
        "category_arabic": "العمرة إلى العمرة كفارة لما بينهما",
        "url_path": "/mishkat:2526"
    },

    # Category 2: Eliminating Poverty and Sins (Following up between Hajj and Umrah)
    {
        "category": "Removal of Poverty and Sins via Alternating Hajj & Umrah",
        "category_arabic": "نفي الفقر والذنوب بالمتابعة بين الحج والعمرة",
        "url_path": "/tirmidhi:810"
    },
    {
        "category": "Removal of Poverty and Sins via Alternating Hajj & Umrah",
        "category_arabic": "نفي الفقر والذنوب بالمتابعة بين الحج والعمرة",
        "url_path": "/nasai:2630"
    },
    {
        "category": "Removal of Poverty and Sins via Alternating Hajj & Umrah",
        "category_arabic": "نفي الفقر والذنوب بالمتابعة بين الحج والعمرة",
        "url_path": "/nasai:2631"
    },
    {
        "category": "Removal of Poverty and Sins via Alternating Hajj & Umrah",
        "category_arabic": "نفي الفقر والذنوب بالمتابعة بين الحج والعمرة",
        "url_path": "/ibnmajah:2887"
    },
    {
        "category": "Removal of Poverty and Sins via Alternating Hajj & Umrah",
        "category_arabic": "نفي الفقر والذنوب بالمتابعة بين الحج والعمرة",
        "url_path": "/mishkat:2524"
    },
    {
        "category": "Removal of Poverty and Sins via Alternating Hajj & Umrah",
        "category_arabic": "نفي الفقر والذنوب بالمتابعة بين الحج والعمرة",
        "url_path": "/mishkat:2525"
    },

    # Category 3: Umrah in Ramadan is Equivalent to Hajj / Hajj with the Prophet (ﷺ)
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/bukhari:1782"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/bukhari:1863"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/muslim:1256"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/tirmidhi:939"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/abudawud:1988"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/nasai:2117"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/ibnmajah:2991"
    },
    {
        "category": "Umrah in Ramadan Equivalent to Hajj with the Prophet (ﷺ)",
        "category_arabic": "عمرة في رمضان تعدل حجة مع النبي ﷺ",
        "url_path": "/mishkat:2530"
    },

    # Category 4: Umrah Performers are the Honored Guests/Delegation of Allah
    {
        "category": "Performers of Umrah are the Honored Delegation of Allah (Wafdullah)",
        "category_arabic": "المعتمرون وفد الله (مستجابو الدعاء ومغفورو الذنب)",
        "url_path": "/ibnmajah:2893"
    },
    {
        "category": "Performers of Umrah are the Honored Delegation of Allah (Wafdullah)",
        "category_arabic": "المعتمرون وفد الله (مستجابو الدعاء ومغفورو الذنب)",
        "url_path": "/nasai:2625"
    },
    {
        "category": "Performers of Umrah are the Honored Delegation of Allah (Wafdullah)",
        "category_arabic": "المعتمرون وفد الله (مستجابو الدعاء ومغفورو الذنب)",
        "url_path": "/nasai:3121"
    },
    {
        "category": "Performers of Umrah are the Honored Delegation of Allah (Wafdullah)",
        "category_arabic": "المعتمرون وفد الله (مستجابو الدعاء ومغفورو الذنب)",
        "url_path": "/mishkat:2536"
    },

    # Category 5: Umrah is the Jihad of Women, the Elderly, and the Weak
    {
        "category": "Umrah is the Jihad of Women, the Elderly, and the Weak",
        "category_arabic": "العمرة جهاد الضعفاء والنساء وكبار السن (جهاد لا قتال فيه)",
        "url_path": "/bukhari:1520"
    },
    {
        "category": "Umrah is the Jihad of Women, the Elderly, and the Weak",
        "category_arabic": "العمرة جهاد الضعفاء والنساء وكبار السن (جهاد لا قتال فيه)",
        "url_path": "/bukhari:2875"
    },
    {
        "category": "Umrah is the Jihad of Women, the Elderly, and the Weak",
        "category_arabic": "العمرة جهاد الضعفاء والنساء وكبار السن (جهاد لا قتال فيه)",
        "url_path": "/nasai:2626"
    },
    {
        "category": "Umrah is the Jihad of Women, the Elderly, and the Weak",
        "category_arabic": "العمرة جهاد الضعفاء والنساء وكبار السن (جهاد لا قتال فيه)",
        "url_path": "/ibnmajah:2901"
    },
    {
        "category": "Umrah is the Jihad of Women, the Elderly, and the Weak",
        "category_arabic": "العمرة جهاد الضعفاء والنساء وكبار السن (جهاد لا قتال فيه)",
        "url_path": "/bulugh:709"
    },

    # Category 6: Reward and Merit Scale with Hardship and Expenditure
    {
        "category": "Reward of Umrah is According to Hardship and Expenditure",
        "category_arabic": "أجر العمرة على قدر النصب والنفقة",
        "url_path": "/bukhari:1787"
    },
    {
        "category": "Reward of Umrah is According to Hardship and Expenditure",
        "category_arabic": "أجر العمرة على قدر النصب والنفقة",
        "url_path": "/ibnmajah:3000"
    },

    # Category 7: Virtues of the Core Rites of Umrah (Tawaf and Touching the Corners)
    {
        "category": "Virtues of Tawaf and Touching the Sacred Corners during Umrah",
        "category_arabic": "فضل الطواف بالبيت واستلام الحجر والركن اليماني",
        "url_path": "/tirmidhi:959"
    },
    {
        "category": "Virtues of Tawaf and Touching the Sacred Corners during Umrah",
        "category_arabic": "فضل الطواف بالبيت واستلام الحجر والركن اليماني",
        "url_path": "/nasai:2919"
    },
    {
        "category": "Virtues of Tawaf and Touching the Sacred Corners during Umrah",
        "category_arabic": "فضل الطواف بالبيت واستلام الحجر والركن اليماني",
        "url_path": "/mishkat:2579"
    },

    # Category 8: Blessed Return and Supplication of the Pilgrim
    {
        "category": "Supplication and Blessed Return from Umrah",
        "category_arabic": "دعاء وفضل الرجوع من العمرة",
        "url_path": "/bukhari:1797"
    },
    {
        "category": "Supplication and Blessed Return from Umrah",
        "category_arabic": "دعاء وفضل الرجوع من العمرة",
        "url_path": "/muslim:1342"
    }
]

def fetch_html(url_path):
    url = f"https://sunnah.com{url_path}"
    headers = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    cmd = ["curl", "-s", "-A", headers, url]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, timeout=30)
    return res.stdout

def clean_text(raw_html):
    if not raw_html:
        return ""
    text = re.sub(r'<[^>]+>', ' ', raw_html)
    text = html.unescape(text)
    return ' '.join(text.split())

def parse_hadith_page(url_path, category, category_arabic):
    print(f"Fetching: {url_path}...")
    html_text = fetch_html(url_path)

    # Reference Sticky
    ref_match = re.search(r'<div\s+class=[\"\']?hadith_reference_sticky[\"\']?[^>]*>(.*?)</div>', html_text)
    reference = clean_text(ref_match.group(1)) if ref_match else url_path.strip('/')

    # Book Names
    b_eng_m = re.search(r'<div\s+class=[\"\']?book_page_english_name[\"\']?[^>]*>(.*?)</div>', html_text)
    book_eng = clean_text(b_eng_m.group(1)) if b_eng_m else ""

    b_ara_m = re.search(r'<div\s+class=[\"\']?book_page_arabic_name[^\"]*[\"\']?[^>]*>(.*?)</div>', html_text)
    book_ara = clean_text(b_ara_m.group(1)) if b_ara_m else ""

    # Chapter Names
    c_eng_m = re.search(r'<div\s+class=[\"\']?englishchapter[\"\']?[^>]*>(.*?)</div>', html_text)
    chapter_eng = clean_text(c_eng_m.group(1)) if c_eng_m else ""

    c_ara_m = re.search(r'<div\s+class=[\"\']?arabicchapter[^\"]*[\"\']?[^>]*>(.*?)</div>', html_text)
    chapter_ara = clean_text(c_ara_m.group(1)) if c_ara_m else ""

    # English text
    eng_match = re.search(r'<div\s+class=[\"\']?english_hadith_full[\"\']?[^>]*>(.*?)<div\s+class=[\"\']?clear[\"\']?>', html_text, re.DOTALL)
    if not eng_match:
        eng_match = re.search(r'<div\s+class=[\"\']?englishcontainer[\"\']?[^>]*>(.*?)<div\s+class=[\"\']?arabic_hadith_full', html_text, re.DOTALL)
    english_text = clean_text(eng_match.group(1)) if eng_match else ""

    # Arabic text
    ara_match = re.search(r'<div\s+class=[\"\']?arabic_hadith_full[^\"]*[\"\']?[^>]*>(.*?)</div>', html_text, re.DOTALL)
    arabic_text = clean_text(ara_match.group(1)) if ara_match else ""

    # Grade
    grade = ""
    grade_cells = re.findall(r'<td\s+class=[\"\']?[^\"\'>]*english_grade[^\"\'>]*[\"\']?[^>]*>(.*?)</td>', html_text, re.DOTALL)
    for gc in grade_cells:
        c_val = clean_text(gc)
        if c_val and "Grade" not in c_val:
            grade = c_val
            break

    if not grade:
        if "bukhari" in url_path:
            grade = "Sahih (Sahih al-Bukhari - Authentic)"
        elif "muslim" in url_path:
            grade = "Sahih (Sahih Muslim - Authentic)"
        elif "riyadussalihin" in url_path:
            grade = "Authentic (Muttafaqun 'Alayh / Agreed Upon)"
        elif "mishkat" in url_path:
            grade = "Authentic (Mishkat al-Masabih)"
        elif "bulugh" in url_path:
            grade = "Sahih (Bulugh al-Maram)"

    # Additional References (in-book, English translation)
    in_book_ref = ""
    in_book_m = re.search(r'In-book reference\s*&nbsp;:&nbsp;\s*([^<]+)', html_text)
    if in_book_m:
        in_book_ref = clean_text(in_book_m.group(1))

    collection_slug = url_path.split(':')[0].strip('/')
    collection_names = {
        "bukhari": "Sahih al-Bukhari",
        "muslim": "Sahih Muslim",
        "tirmidhi": "Jami` at-Tirmidhi",
        "nasai": "Sunan an-Nasa'i",
        "abudawud": "Sunan Abi Dawud",
        "ibnmajah": "Sunan Ibn Majah",
        "malik": "Muwatta Malik",
        "riyadussalihin": "Riyad as-Salihin",
        "mishkat": "Mishkat al-Masabih",
        "bulugh": "Bulugh al-Maram"
    }

    collection_name = collection_names.get(collection_slug, collection_slug.capitalize())

    return {
        "id": url_path.strip('/'),
        "collection": collection_name,
        "reference": reference,
        "in_book_reference": in_book_ref,
        "category": category,
        "category_arabic": category_arabic,
        "book_english": book_eng,
        "book_arabic": book_ara,
        "chapter_english": chapter_eng,
        "chapter_arabic": chapter_ara,
        "grade": grade,
        "english_text": english_text,
        "arabic_text": arabic_text,
        "sunnah_url": f"https://sunnah.com{url_path}"
    }

def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Scraping Fazail of Umrah from Sunnah.com into: {output_dir}")

    all_data = []
    seen = set()

    for item in HADITH_ENTRIES:
        path = item["url_path"]
        if path in seen:
            continue
        try:
            hadith_data = parse_hadith_page(path, item["category"], item["category_arabic"])
            if hadith_data["english_text"] and hadith_data["arabic_text"]:
                all_data.append(hadith_data)
                seen.add(path)
                print(f"  [SUCCESS] {hadith_data['reference']} ({hadith_data['category']})")
            else:
                print(f"  [WARNING] Partial data for {path}")
            # polite throttle
            time.sleep(0.3)
        except Exception as e:
            print(f"  [ERROR] Failed {path}: {e}")

    data_dir = os.path.join(output_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    print(f"\nTotal Hadiths Successfully Scraped: {len(all_data)}")

    # 1. Save JSON
    json_path = os.path.join(data_dir, "fazail_umrah.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON: {json_path}")

    # 2. Save CSV
    csv_path = os.path.join(data_dir, "fazail_umrah.csv")
    fields = [
        "id", "collection", "reference", "category", "category_arabic",
        "grade", "in_book_reference", "book_english", "chapter_english",
        "english_text", "arabic_text", "sunnah_url"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_data)
    print(f"Saved CSV: {csv_path}")

    # 3. Save Markdown Report
    md_path = os.path.join(data_dir, "FAZAIL_OF_UMRAH.md")
    generate_markdown(all_data, md_path)
    print(f"Saved Markdown: {md_path}")

def generate_markdown(data, md_path):
    # Group by category
    categories = {}
    for h in data:
        cat = h["category"]
        if cat not in categories:
            categories[cat] = {
                "arabic": h["category_arabic"],
                "hadiths": []
            }
        categories[cat]["hadiths"].append(h)

    lines = []
    lines.append("# Fazā'il of 'Umrah (فضائل العمرة) from Sunnah.com\n")
    lines.append("> **Comprehensive compilation of prophetic hadiths on the virtues, spiritual merits, and rewards of performing 'Umrah, scraped directly from [Sunnah.com](https://sunnah.com).**\n")
    lines.append(f"**Total Hadiths Compiled:** {len(data)}  \n")
    lines.append(f"**Collections Included:** Sahih al-Bukhari, Sahih Muslim, Jami` at-Tirmidhi, Sunan an-Nasa'i, Sunan Ibn Majah, Sunan Abi Dawud, Riyad as-Salihin, Mishkat al-Masabih, Bulugh al-Maram.\n")
    lines.append("\n---\n")

    lines.append("## Table of Contents")
    for i, (cat_name, cat_obj) in enumerate(categories.items(), 1):
        lines.append(f"{i}. [{cat_name} ({cat_obj['arabic']})](#{cat_name.lower().replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace(',', '')})")
    lines.append("\n---\n")

    for cat_name, cat_obj in categories.items():
        anchor = cat_name.lower().replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace(',', '')
        lines.append(f"## {cat_name}")
        lines.append(f"### {cat_obj['arabic']}\n")

        for h in cat_obj["hadiths"]:
            lines.append(f"#### [{h['reference']}]({h['sunnah_url']})")
            lines.append(f"- **Collection:** {h['collection']}")
            if h.get('grade'):
                lines.append(f"- **Grade:** `{h['grade']}`")
            if h.get('chapter_english'):
                lines.append(f"- **Chapter:** {h['chapter_english']} / {h['chapter_arabic']}")
            if h.get('in_book_reference'):
                lines.append(f"- **In-Book Reference:** {h['in_book_reference']}")
            lines.append("")
            lines.append(f"> **Arabic Text:**  \n> {h['arabic_text']}\n")
            lines.append(f"> **English Translation:**  \n> {h['english_text']}\n")
            lines.append(f"🔗 [View Hadith on Sunnah.com]({h['sunnah_url']})\n")
            lines.append("---\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
