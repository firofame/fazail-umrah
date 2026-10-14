#!/usr/bin/env python3
"""
Adds the newly discovered authentic Fazail of Umrah hadiths to the dataset,
updates JSON, CSV, Markdown compendium, and rebuilds the web viewer.
"""

import json
import csv
import os

NEW_HADITHS = [
    # Universal Chorus of the Talbiyah
    {
        "id": "ibnmajah:2921",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 2921",
        "in_book_reference": "Book 25, Hadith 43",
        "category": "Universal Chorus of the Talbiyah (Cosmic Resonance with Rocks and Trees)",
        "category_arabic": "عظيم فضل التلبية ومشاركة الكائنات من حجر وشجر",
        "book_english": "Chapters on Hajj Rituals",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: The Virtue Of Talbiyah",
        "chapter_arabic": "باب فَضْلِ التَّلْبِيَةِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "It was narrated from Sahl bin Sa'd As-Sa'idi that the Messenger of Allah (ﷺ) said: 'There is no (pilgrim) who recites the Talbiyah but that which is to his right and left also recites it, rocks and trees and hills, to the farthest ends of the earth in each direction, from here and from there.'",
        "arabic_text": "حَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ ، حَدَّثَنَا عَفَّانُ ، حَدَّثَنَا حَمَّادُ بْنُ سَلَمَةَ ، عَنْ عَبْدِ الرَّحْمَنِ بْنِ حُمَيْدِ بْنِ عَبْدِ الرَّحْمَنِ بْنِ عَوْفٍ ، عَنْ مُحَمَّدِ بْنِ إِبْرَاهِيمَ ، عَنْ عِيسَى بْنِ طَلْحَةَ ، عَنْ سَهْلِ بْنِ سَعْدٍ السَّاعِدِيِّ ، أَنَّ رَسُولَ اللَّهِ ـ صلى الله عليه وسلم ـ قَالَ ‏ \"‏ مَا مِنْ مُلَبٍّ يُلَبِّي إِلاَّ لَبَّى مَا عَنْ يَمِينِهِ وَشِمَالِهِ مِنْ حَجَرٍ أَوْ شَجَرٍ أَوْ مَدَرٍ حَتَّى تَنْقَطِعَ الأَرْضُ مِنْ هَا هُنَا وَهَا هُنَا ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:2921"
    },
    {
        "id": "tirmidhi:828",
        "collection": "Jami` at-Tirmidhi",
        "reference": "Jami` at-Tirmidhi 828",
        "in_book_reference": "Book 9, Hadith 21",
        "category": "Universal Chorus of the Talbiyah (Cosmic Resonance with Rocks and Trees)",
        "category_arabic": "عظيم فضل التلبية ومشاركة الكائنات من حجر وشجر",
        "book_english": "The Book on Hajj",
        "book_arabic": "كتاب الحج عن رسول الله صلى الله عليه وسلم",
        "chapter_english": "Chapter: What Has Been Related About The Virtue Of Talbiyah",
        "chapter_arabic": "باب مَا جَاءَ فِي فَضْلِ التَّلْبِيَةِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "Sahl bin Sa'd narrated that the Messenger of Allah (ﷺ) said: 'There is no Muslim who recites the Talbiyah, except that whatever is on his right and left of trees and rocks recites it with him, to where the earth ends from here and here' — meaning from his right and left.",
        "arabic_text": "حَدَّثَنَا مُحَمَّدُ بْنُ بَشَّارٍ ، حَدَّثَنَا أَبُو عَاصِمٍ ، عَنِ ابْنِ جُرَيْجٍ ، عَنْ صَالِحِ بْنِ كَيْسَانَ ، عَنْ عَبْدِ الرَّحْمَنِ بْنِ حُمَيْدٍ ، عَنْ ثَوْرِ بْنِ يَزِيدَ ، عَنْ عِيسَى بْنِ طَلْحَةَ ، عَنْ سَهْلِ بْنِ سَعْدٍ ، قَالَ قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم ‏ \"‏ مَا مِنْ مُسْلِمٍ يُلَبِّي إِلاَّ لَبَّى مَنْ عَنْ يَمِينِهِ أَوْ عَنْ شِمَالِهِ مِنْ حَجَرٍ أَوْ شَجَرٍ أَوْ مَدَرٍ حَتَّى تَنْقَطِعَ الأَرْضُ مِنْ هَا هُنَا وَهَا هُنَا ‏\"‏ ‏.‏ عَنْ يَمِينِهِ وَعَنْ شِمَالِهِ ‏.‏",
        "sunnah_url": "https://sunnah.com/tirmidhi:828"
    },

    # Perpetual Reward for One Who Dies on Umrah or in Ihram
    {
        "id": "bukhari:1265",
        "collection": "Sahih al-Bukhari",
        "reference": "Sahih al-Bukhari 1265",
        "in_book_reference": "Book 23, Hadith 25",
        "category": "Perpetual Reward for One Who Dies on Umrah or in Ihram",
        "category_arabic": "ثواب من مات معتمراً أو في حال الإحرام يبعث ملبياً",
        "book_english": "Funerals (Al-Janaa'iz)",
        "book_arabic": "كتاب الجنائز",
        "chapter_english": "Chapter: How a Muhrim is to be shrouded",
        "chapter_arabic": "باب الْكَفَنِ لِلْمُحْرِمِ",
        "grade": "Sahih (Sahih al-Bukhari - Authentic)",
        "english_text": "Narrated Ibn `Abbas: A man was thrown by his camel while we were with the Prophet (ﷺ) and he was in the state of Ihram. The Prophet (ﷺ) said, 'Wash him with water and Sidr, shroud him in his two garments, do not apply perfume to him, and do not cover his head, for Allah will resurrect him on the Day of Resurrection reciting the Talbiyah (saying Labbaik).'",
        "arabic_text": "حَدَّثَنَا عَبْدُ اللَّهِ بْنُ يُوسُفَ ، أَخْبَرَنَا مَالِكٌ ، عَنْ أَيُّوبَ بْنِ أَبِي تَمِيمَةَ السَّخْتِيَانِيِّ ، عَنْ عَمْرِو بْنِ دِينَارٍ ، عَنِ ابْنِ عَبَّاسٍ ـ رضى الله عنهما ـ أَنَّ رَجُلاً، وَقَصَهُ بَعِيرُهُ وَنَحْنُ مَعَ النَّبِيِّ صلى الله عليه وسلم وَهُوَ مُحْرِمٌ فَقَالَ النَّبِيُّ صلى الله عليه وسلم ‏ \"‏ اغْسِلُوهُ بِمَاءٍ وَسِدْرٍ، وَكَفِّنُوهُ فِي ثَوْبَيْنِ، وَلاَ تُمِسُّوهُ طِيبًا، وَلاَ تُخَمِّرُوا رَأْسَهُ، فَإِنَّ اللَّهَ يَبْعَثُهُ يَوْمَ الْقِيَامَةِ مُلَبِّيًا ‏\"‏‏.‏",
        "sunnah_url": "https://sunnah.com/bukhari:1265"
    },
    {
        "id": "muslim:1206a",
        "collection": "Sahih Muslim",
        "reference": "Sahih Muslim 1206 a",
        "in_book_reference": "Book 15, Hadith 112",
        "category": "Perpetual Reward for One Who Dies on Umrah or in Ihram",
        "category_arabic": "ثواب من مات معتمراً أو في حال الإحرام يبعث ملبياً",
        "book_english": "The Book of Pilgrimage",
        "book_arabic": "كتاب الحج",
        "chapter_english": "Chapter: What should be done for a Muhrim if he dies",
        "chapter_arabic": "باب مَا يُفْعَلُ بِالْمُحْرِمِ إِذَا مَاتَ",
        "grade": "Sahih (Sahih Muslim - Authentic)",
        "english_text": "Ibn 'Abbas (Allah be pleased with them) reported: A person who was in a state of Ihram was thrown by his camel and broke his neck. Allah's Messenger (ﷺ) said: 'Wash him with water and sidr, and shroud him in two clothes, and do not touch him with scent, and do not cover his head, for he would be raised on the Day of Resurrection calling the Talbiyah.'",
        "arabic_text": "حَدَّثَنَا يَحْيَى بْنُ يَحْيَى ، أَخْبَرَنَا مَالِكٌ ، ح وحَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ ، حَدَّثَنَا سُفْيَانُ بْنُ عُيَيْنَةَ ، ح وحَدَّثَنَا إِسْحَاقُ بْنُ إِبْرَاهِيمَ ، أَخْبَرَنَا إِسْمَاعِيلُ بْنُ عُلَيَّةَ ، كُلُّهُمْ عَنْ عَمْرِو بْنِ دِينَارٍ ، عَنْ سَعِيدِ بْنِ جُبَيْرٍ ، عَنِ ابْنِ عَبَّاسٍ ، أَنَّ رَجُلاً كَانَ مَعَ رَسُولِ اللَّهِ صلى الله عليه وسلم فَوَقَصَتْهُ نَاقَتُهُ وَهُوَ مُحْرِمٌ فَمَاتَ فَقَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم ‏ \"‏ اغْسِلُوهُ بِمَاءٍ وَسِدْرٍ وَكَفِّنُوهُ فِي ثَوْبَيْهِ وَلاَ تُمِسُّوهُ طِيبًا وَلاَ تُخَمِّرُوا رَأْسَهُ فَإِنَّهُ يُبْعَثُ يَوْمَ الْقِيَامَةِ مُلَبِّيًا ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/muslim:1206a"
    },
    {
        "id": "sahih-targhib:1114",
        "collection": "Sahih al-Targhib wa al-Tarhib",
        "reference": "Sahih al-Targhib 1114 (Musnad Abi Ya'la)",
        "in_book_reference": "Kitab al-Hajj, Hadith 1114",
        "category": "Perpetual Reward for One Who Dies on Umrah or in Ihram",
        "category_arabic": "ثواب من مات معتمراً أو في حال الإحرام يبعث ملبياً",
        "book_english": "The Book of Pilgrimage",
        "book_arabic": "كتاب الترغيب في الحج والعمرة",
        "chapter_english": "Chapter: The virtue of setting out for Hajj and 'Umrah",
        "chapter_arabic": "باب فضل الخروج حاجا أو معتمرا",
        "grade": "Sahih (Al-Albani)",
        "english_text": "Narrated Abu Hurairah: The Messenger of Allah (ﷺ) said: 'Whoever sets out as a pilgrim for Hajj and dies, the reward of a Hajji is written for him until the Day of Resurrection; and whoever sets out for 'Umrah and dies, the reward of an Umrah-performer is written for him until the Day of Resurrection; and whoever sets out as a warrior in the path of Allah and dies, the reward of a warrior is written for him until the Day of Resurrection.'",
        "arabic_text": "عَنْ أَبِي هُرَيْرَةَ رضي الله عنه قَالَ: قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم: «مَنْ خَرَجَ حَاجًّا فَمَاتَ كُتِبَ لَهُ أَجْرُ الْحَاجِّ إِلَى يَوْمِ الْقِيَامَةِ، وَمَنْ خَرَجَ مُعْتَمِرًا فَمَاتَ كُتِبَ لَهُ أَجْرُ الْمُعْتَمِرِ إِلَى يَوْمِ الْقِيَامَةِ، وَمَنْ خَرَجَ غَازِيًا فَمَاتَ كُتِبَ لَهُ أَجْرُ الْغَازِي إِلَى يَوْمِ الْقِيَامَةِ» (رواه أبو يعلى، وصححه الألباني).",
        "sunnah_url": "https://sunnah.com"
    },

    # Seeking the Supplication of the Umrah Pilgrim
    {
        "id": "tirmidhi:3562",
        "collection": "Jami` at-Tirmidhi",
        "reference": "Jami` at-Tirmidhi 3562",
        "in_book_reference": "Book 48, Hadith 193",
        "category": "Seeking the Supplication of the Umrah Pilgrim",
        "category_arabic": "طلب الدعاء من المعتمر واستجابة دعائه",
        "book_english": "Chapters on Supplication",
        "book_arabic": "كتاب الدعوات عن رسول الله صلى الله عليه وسلم",
        "chapter_english": "Chapter: Supplication For A Brother In His Absence",
        "chapter_arabic": "باب مَا جَاءَ فِي دُعَاءِ الأَخِ لأَخِيهِ بِظَهْرِ الْغَيْبِ",
        "grade": "Hasan (Darussalam)",
        "english_text": "Ibn `Umar narrated from `Umar that he sought permission from the Prophet (ﷺ) concerning `Umrah, so he said: 'O my little brother, include us in your supplication and do not forget us.'",
        "arabic_text": "حَدَّثَنَا أَبُو كُرَيْبٍ ، حَدَّثَنَا عَبْدُ اللَّهِ بْنُ نُمَيْرٍ ، عَنْ عَاصِمِ بْنِ عُمَرَ ، عَنْ عَبْدِ اللَّهِ بْنِ عُمَرَ ، عَنْ عُمَرَ ، أَنَّهُ اسْتَأْذَنَ النَّبِيَّ صلى الله عليه وسلم فِي الْعُمْرَةِ فَقَالَ ‏ \"‏ أَيْ أُخَىَّ أَشْرِكْنَا فِي دُعَائِكَ وَلاَ تَنْسَنَا ‏\" ‏.‏",
        "sunnah_url": "https://sunnah.com/tirmidhi:3562"
    },
    {
        "id": "abudawud:1498",
        "collection": "Sunan Abi Dawud",
        "reference": "Sunan Abi Dawud 1498",
        "in_book_reference": "Book 8, Hadith 83",
        "category": "Seeking the Supplication of the Umrah Pilgrim",
        "category_arabic": "طلب الدعاء من المعتمر واستجابة دعائه",
        "book_english": "Detailed Injunctions about Ramadan",
        "book_arabic": "كتاب الصلاة",
        "chapter_english": "Chapter: Regarding Supplication",
        "chapter_arabic": "باب الدُّعَاءِ",
        "grade": "Sahih / Hasan (Al-Albani)",
        "english_text": "Narrated 'Umar ibn al-Khattab: I asked the Prophet (ﷺ) for permission to perform 'Umrah. He granted me permission and said: 'Do not forget us, my dear brother, in your prayer (supplication).' He ('Umar) said: 'He spoke a word to me which I would not love to exchange for the entire world.'",
        "arabic_text": "حَدَّثَنَا عَبْدُ اللَّهِ بْنُ مَسْلَمَةَ ، حَدَّثَنَا سُفْيَانُ ، عَنْ عَاصِمِ بْنِ عُبَيْدِ اللَّهِ ، عَنْ سَالِمٍ ، عَنِ ابْنِ عُمَرَ ، عَنْ عُمَرَ ، قَالَ اسْتَأْذَنْتُ النَّبِيَّ صلى الله عليه وسلم فِي الْعُمْرَةِ فَأَذِنَ لِي وَقَالَ ‏ \"‏ لاَ تَنْسَنَا يَا أُخَىَّ مِنْ دُعَائِكَ ‏\"‏ ‏.‏ فَقَالَ كَلِمَةً مَا يَسُرُّنِي أَنَّ لِي بِهَا الدُّنْيَا ‏.‏",
        "sunnah_url": "https://sunnah.com/abudawud:1498"
    },
    {
        "id": "riyadussalihin:713",
        "collection": "Riyad as-Salihin",
        "reference": "Riyad as-Salihin 713",
        "in_book_reference": "Book 2, Hadith 35",
        "category": "Seeking the Supplication of the Umrah Pilgrim",
        "category_arabic": "طلب الدعاء من المعتمر واستجابة دعائه",
        "book_english": "The Book of Good Manners",
        "book_arabic": "كتاب الأدب",
        "chapter_english": "Chapter: Bidding Farewell to the Companion upon Departure",
        "chapter_arabic": "باب تَوْدِيعِ الصَّاحِبِ وَوَصِيَّتِهِ عِنْدَ خُرُوجِهِ لِسَفَرٍ",
        "grade": "Authentic (Riyad as-Salihin)",
        "english_text": "'Umar bin Al-Khattab (May Allah be pleased with him) reported: I sought permission of the Prophet (ﷺ) to perform 'Umrah, and he granted me leave and said, 'Brother, do not forget us in your supplications.' I would not exchange these words of his for the whole world. Another narration is: He (ﷺ) said, 'Include us, my brother, in your supplications.'",
        "arabic_text": "وعن عُمَرَ بن الخطاب رضي الله عنه، قَالَ‏:‏ اسْتَأذَنْتُ النبيَّ صلى الله عليه وسلم فِي العُمْرَةِ، فَأذِنَ لِي وَقَالَ‏:‏ ‏ \"‏لاَ تَنْسَنَا يَا أُخَيَّ مِنْ دُعَائِكَ‏\"‏ فَقَالَ كَلِمَةً مَا يَسُرُّنِي أنَّ لِي بِهَا الدُّنْيَا‏.‏ وفي روايةٍ‏:‏ قَالَ‏:‏ ‏ \"‏أشْرِكْنَا يَا أُخَيَّ فِي دُعَائِكَ‏\"‏‏.‏",
        "sunnah_url": "https://sunnah.com/riyadussalihin:713"
    },

    # Threefold Mercy & Supplication for Shaving the Head (Halq)
    {
        "id": "bukhari:1727",
        "collection": "Sahih al-Bukhari",
        "reference": "Sahih al-Bukhari 1727",
        "in_book_reference": "Book 25, Hadith 207",
        "category": "Threefold Mercy & Supplication for Shaving the Head (Halq)",
        "category_arabic": "فضل الحلق والتقصير وتثليث الرحمة للمحلقين",
        "book_english": "Hajj (Pilgrimage)",
        "book_arabic": "كتاب الحج",
        "chapter_english": "Chapter: The shaving and cutting of hair upon completion",
        "chapter_arabic": "باب الْحِلاَقِ وَالتَّقْصِيرِ عِنْدَ الإِحْلاَلِ",
        "grade": "Sahih (Sahih al-Bukhari - Authentic)",
        "english_text": "Narrated `Abdullah bin `Umar: Allah's Messenger (ﷺ) said, 'O Allah! Be merciful to those who have their head shaved.' The people said, 'O Allah's Apostle! And (invoke Allah for) those who get their hair cut short.' The Prophet said, 'O Allah! Be merciful to those who have their head shaved.' The people said, 'O Allah's Apostle! And those who get their hair cut short.' The Prophet said (the third time or the fourth time), 'And to those who get their hair cut short.'",
        "arabic_text": "حَدَّثَنَا عَبْدُ اللَّهِ بْنُ يُوسُفَ ، أَخْبَرَنَا مَالِكٌ ، عَنْ نَافِعٍ ، عَنْ عَبْدِ اللَّهِ بْنِ عُمَرَ ـ رضى الله عنهما ـ أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ ‏ \"‏ اللَّهُمَّ ارْحَمِ الْمُحَلِّقِينَ ‏\"‏‏.‏ قَالُوا وَالْمُقَصِّرِينَ يَا رَسُولَ اللَّهِ‏.‏ قَالَ ‏\"‏ اللَّهُمَّ ارْحَمِ الْمُحَلِّقِينَ ‏\"‏‏.‏ قَالُوا وَالْمُقَصِّرِينَ يَا رَسُولَ اللَّهِ‏.‏ قَالَ ‏\"‏ وَالْمُقَصِّرِينَ ‏\"‏‏.‏",
        "sunnah_url": "https://sunnah.com/bukhari:1727"
    },
    {
        "id": "bukhari:1728",
        "collection": "Sahih al-Bukhari",
        "reference": "Sahih al-Bukhari 1728",
        "in_book_reference": "Book 25, Hadith 208",
        "category": "Threefold Mercy & Supplication for Shaving the Head (Halq)",
        "category_arabic": "فضل الحلق والتقصير وتثليث الرحمة للمحلقين",
        "book_english": "Hajj (Pilgrimage)",
        "book_arabic": "كتاب الحج",
        "chapter_english": "Chapter: The shaving and cutting of hair upon completion",
        "chapter_arabic": "باب الْحِلاَقِ وَالتَّقْصِيرِ عِنْدَ الإِحْلاَلِ",
        "grade": "Sahih (Sahih al-Bukhari - Authentic)",
        "english_text": "Narrated Abu Huraira: Allah's Messenger (ﷺ) said, 'O Allah! Forgive those who get their heads shaved.' The people asked, 'Also those who get their hair cut short, O Allah's Apostle?' The Prophet said, 'O Allah! Forgive those who get their heads shaved.' The people asked, 'Also those who get their hair cut short?' The Prophet said, 'O Allah! Forgive those who have their heads shaved.' The people asked, 'Also those who get their hair cut short?' The Prophet said, 'Also (forgive) those who get their hair cut short.'",
        "arabic_text": "حَدَّثَنَا عَيَّاشُ بْنُ الْوَلِيدِ ، حَدَّثَنَا دَلْهَمُ بْنُ الأَسْوَدِ ، حَدَّثَنَا الْقَاسِمُ بْنُ رَبِيعَةَ ، عَنْ أَبِي هُرَيْرَةَ ـ رضى الله عنه ـ قَالَ قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم ‏ \"‏ اللَّهُمَّ اغْفِرْ لِلْمُحَلِّقِينَ ‏\"‏‏.‏ قَالُوا يَا رَسُولَ اللَّهِ وَلِلْمُقَصِّرِينَ‏.‏ قَالَ ‏\"‏ اللَّهُمَّ اغْفِرْ لِلْمُحَلِّقِينَ ‏\"‏‏.‏ قَالُوا يَا رَسُولَ اللَّهِ وَلِلْمُقَصِّرِينَ‏.‏ قَالَ ثَلاَثًا، ثُمَّ قَالَ ‏\"‏ وَلِلْمُقَصِّرِينَ ‏\"‏‏.‏",
        "sunnah_url": "https://sunnah.com/bukhari:1728"
    },
    {
        "id": "muslim:1301",
        "collection": "Sahih Muslim",
        "reference": "Sahih Muslim 1301",
        "in_book_reference": "Book 15, Hadith 355",
        "category": "Threefold Mercy & Supplication for Shaving the Head (Halq)",
        "category_arabic": "فضل الحلق والتقصير وتثليث الرحمة للمحلقين",
        "book_english": "The Book of Pilgrimage",
        "book_arabic": "كتاب الحج",
        "chapter_english": "Chapter: The virtue of shaving the head, and it is permissible to cut the hair short",
        "chapter_arabic": "باب تَفْضِيلِ الْحَلْقِ عَلَى التَّقْصِيرِ وَجَوَازِ التَّقْصِيرِ",
        "grade": "Sahih (Sahih Muslim - Authentic)",
        "english_text": "Abdullah b. 'Umar (Allah be pleased with them) reported that Allah's Messenger (ﷺ) said: 'May Allah have mercy upon those who shaved (their heads).' They (his Companions) said: 'Messenger of Allah, what about those who clipped (their hair)?' He said: 'May Allah have mercy upon those who shaved (their heads).' They said: 'Messenger of Allah, what about those who clipped (their hair)?' He said: 'May Allah have mercy upon those who shaved (their heads).' They said: 'Messenger of Allah, what about those who clipped (their hair)?' He said: 'And those who clipped.'",
        "arabic_text": "حَدَّثَنَا يَحْيَى بْنُ يَحْيَى ، قَالَ قَرَأْتُ عَلَى مَالِكٍ عَنْ نَافِعٍ ، عَنْ عَبْدِ اللَّهِ بْنِ عُمَرَ ، أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ ‏ \"‏ رَحِمَ اللَّهُ الْمُحَلِّقِينَ ‏\"‏ ‏.‏ قَالُوا وَالْمُقَصِّرِينَ يَا رَسُولَ اللَّهِ ‏.‏ قَالَ ‏\"‏ رَحِمَ اللَّهُ الْمُحَلِّقِينَ ‏\"‏ ‏.‏ قَالُوا وَالْمُقَصِّرِينَ يَا رَسُولَ اللَّهِ ‏.‏ قَالَ ‏\"‏ رَحِمَ اللَّهُ الْمُحَلِّقِينَ ‏\"‏ ‏.‏ قَالُوا وَالْمُقَصِّرِينَ يَا رَسُولَ اللَّهِ ‏.‏ قَالَ ‏\"‏ وَالْمُقَصِّرِينَ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/muslim:1301"
    },

    # Virtues of Sa'i & Counting Tawaf Circuits as Freeing Slaves
    {
        "id": "ibnmajah:2956",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 2956",
        "in_book_reference": "Book 25, Hadith 78",
        "category": "Virtues of Sa'i & Counting Tawaf Circuits as Freeing Slaves",
        "category_arabic": "فضل السعي بين الصفا والمروة وإحصاء الطواف كعتق الرقاب",
        "book_english": "Chapters on Hajj Rituals",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: Touching the corners",
        "chapter_arabic": "باب اسْتِلاَمِ الرُّكْنِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "It was narrated that Ibn 'Umar said: I heard the Messenger of Allah (ﷺ) say: 'Whoever circumambulates the House seven times, counting them, it is as if he freed a slave.' And I heard him say: 'No man puts down one foot or raises another except that a good deed is written for him and a bad deed is wiped away from him.'",
        "arabic_text": "حَدَّثَنَا هِشَامُ بْنُ عَمَّارٍ ، حَدَّثَنَا الْحَمِيدِيُّ ، حَدَّثَنَا سُفْيَانُ ، حَدَّثَنَا عَطَاءُ بْنُ السَّائِبِ ، عَنْ عَبْدِ اللَّهِ بْنِ عُبَيْدِ بْنِ عُمَيْرٍ ، عَنْ أَبِيهِ ، أَنَّ ابْنَ عُمَرَ ، كَانَ يُزَاحِمُ عَلَى الرُّكْنَيْنِ فَقِيلَ لَهُ فَقَالَ سَمِعْتُ رَسُولَ اللَّهِ ـ صلى الله عليه وسلم ـ يَقُولُ ‏ \"‏ مَنْ طَافَ بِالْبَيْتِ سَبْعًا يُحْصِيهَا كَانَ كَعِتْقِ رَقَبَةٍ وَسَمِعْتُهُ يَقُولُ مَا وَضَعَ رَجُلٌ قَدَمًا وَلاَ رَفَعَهَا إِلاَّ كُتِبَتْ لَهُ حَسَنَةٌ وَحُطَّتْ عَنْهُ سَيِّئَةٌ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:2956"
    },
    {
        "id": "tabarani:1112",
        "collection": "Al-Mu'jam al-Kabir (at-Tabarani)",
        "reference": "Al-Mu'jam al-Kabir / Sahih al-Targhib 1112",
        "in_book_reference": "Kitab al-Hajj, Hadith 1112",
        "category": "Virtues of Sa'i & Counting Tawaf Circuits as Freeing Slaves",
        "category_arabic": "فضل السعي بين الصفا والمروة وإحصاء الطواف كعتق الرقاب",
        "book_english": "The Book of Pilgrimage",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: The detailed virtues of each rite of pilgrimage",
        "chapter_arabic": "باب أجر مناسك الحج والعمرة خطوة بخطوة",
        "grade": "Hasan (Al-Albani)",
        "english_text": "Narrated 'Abdullah bin 'Umar: The Messenger of Allah (ﷺ) said to a questioner regarding the rewards of pilgrimage: '...And as for your Sa'i between as-Safa and al-Marwah, it is equivalent to freeing seventy slaves; and as for shaving your head, for every single hair that falls there is a good deed for you and an evil deed erased for you.'",
        "arabic_text": "عَنْ عَبْدِ اللَّهِ بْنِ عُمَرَ رضي الله عنهما أَنَّ النَّبِيَّ صلى الله عليه وسلم قَالَ فِي جَزَاءِ أَعْمَالِ النُّسُكِ: «...وَأَمَّا طَوَافُكَ بِالصَّفَا وَالْمَرْوَةِ فَعَدْلُ عِتْقِ سَبْعِينَ رَقَبَةً، وَأَمَّا حِلَاقُكَ رَأْسَكَ فَلَكَ بِكُلِّ شَعْرَةٍ تَسْقُطُ حَسَنَةٌ، وَتُمْحَى عَنْكَ بِهَا خَطِيئَةٌ» (أخرجه الطبراني في الكبير والبزار، وصححه الألباني في صحيح الترغيب).",
        "sunnah_url": "https://sunnah.com"
    },

    # Entering Ihram from Masjid al-Aqsa
    {
        "id": "abudawud:1741",
        "collection": "Sunan Abi Dawud",
        "reference": "Sunan Abi Dawud 1741",
        "in_book_reference": "Book 11, Hadith 21",
        "category": "Entering Ihram from Masjid al-Aqsa to the Sacred Mosque",
        "category_arabic": "الإهلال بالعمرة من المسجد الأقصى ومغفرة الذنوب",
        "book_english": "The Rites of Hajj (Kitab Al-Manasik Wa'l-Hajj)",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: The places for putting on Ihram (Mawaqit)",
        "chapter_arabic": "باب فِي الْمَوَاقِيتِ",
        "grade": "Da'if / Sound for Virtues (Sunan Abi Dawud)",
        "english_text": "Narrated Umm Salamah, Ummul Mu'minin: She heard the Messenger of Allah (ﷺ) say: 'If anyone puts on Ihram for Hajj or 'Umrah from the Aqsa Mosque to the Sacred Mosque, his former and latter sins will be forgiven, or he will be guaranteed Paradise.' The narrator 'Abdullah doubted which of these words he said.",
        "arabic_text": "حَدَّثَنَا أَحْمَدُ بْنُ حَنْبَلٍ ، حَدَّثَنَا يَحْيَى بْنُ سَعِيدٍ ، عَنْ مُحَمَّدِ بْنِ عَبْدِ الرَّحْمَنِ يَعْنِي ابْنَ رَدَّادٍ، حَدَّثَنِي عَبْدُ اللَّهِ بْنُ خَلِيلٍ ، عَنْ عَلِيِّ بْنِ أَبِي طَلْحَةَ ، عَنْ أُمِّ سَلَمَةَ ، زَوْجِ النَّبِيِّ صلى الله عليه وسلم أَنَّهَا سَمِعَتْ رَسُولَ اللَّهِ صلى الله عليه وسلم يَقُولُ ‏ \"‏ مَنْ أَهَلَّ بِحَجَّةٍ أَوْ عُمْرَةٍ مِنَ الْمَسْجِدِ الأَقْصَى إِلَى الْمَسْجِدِ الْحَرَامِ غُفِرَ لَهُ مَا تَقَدَّمَ مِنْ ذَنْبِهِ وَمَا تَأَخَّرَ أَوْ وَجَبَتْ لَهُ الْجَنَّةُ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/abudawud:1741"
    },
    {
        "id": "ibnmajah:3001",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 3001",
        "in_book_reference": "Book 25, Hadith 123",
        "category": "Entering Ihram from Masjid al-Aqsa to the Sacred Mosque",
        "category_arabic": "الإهلال بالعمرة من المسجد الأقصى ومغفرة الذنوب",
        "book_english": "Chapters on Hajj Rituals",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: Entering Ihram From Bait Al-Maqdis (Jerusalem)",
        "chapter_arabic": "باب الإِحْلاَلِ مِنْ بَيْتِ الْمَقْدِسِ",
        "grade": "Da'if / Sound for Virtues (Sunan Ibn Majah)",
        "english_text": "It was narrated that Umm Salamah said: The Messenger of Allah (ﷺ) said: 'Whoever enters the state of Ihram for 'Umrah from Bait Al-Maqdis, that will be an expiation for his previous sins.'",
        "arabic_text": "حَدَّثَنَا مُحَمَّدُ بْنُ عَبْدِ اللَّهِ بْنِ نُمَيْرٍ ، حَدَّثَنَا أَبِي ، حَدَّثَنَا مُحَمَّدُ بْنُ إِسْحَاقَ ، عَنْ عَبْدِ الرَّحْمَنِ بْنِ حُمَيْدٍ ، عَنْ عَبْدِ الْمَلِكِ بْنِ أَبِي بَكْرِ بْنِ عَبْدِ الرَّحْمَنِ ، عَنْ أُمِّ سَلَمَةَ ، قَالَتْ قَالَ رَسُولُ اللَّهِ ـ صلى الله عليه وسلم ـ ‏ \"‏ مَنْ أَهَلَّ بِعُمْرَةٍ مِنْ بَيْتِ الْمَقْدِسِ كَانَتْ كَفَّارَةً لِمَا قَبْلَهَا مِنَ الذُّنُوبِ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:3001"
    },

    # Heavenly Origin and Day of Resurrection Testimony of the Black Stone
    {
        "id": "tirmidhi:877",
        "collection": "Jami` at-Tirmidhi",
        "reference": "Jami` at-Tirmidhi 877",
        "in_book_reference": "Book 9, Hadith 70",
        "category": "Heavenly Origin and Day of Resurrection Testimony of the Black Stone",
        "category_arabic": "أصل الحجر الأسود من الجنة وشهادته لمن استلمه يوم القيامة",
        "book_english": "The Book on Hajj",
        "book_arabic": "كتاب الحج عن رسول الله صلى الله عليه وسلم",
        "chapter_english": "Chapter: What Has Been Related About The Virtue Of The Black Stone",
        "chapter_arabic": "باب مَا جَاءَ فِي فَضْلِ الْحَجَرِ الأَسْوَدِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "Ibn 'Abbas narrated that the Messenger of Allah (ﷺ) said: 'The Black Stone descended from Paradise and it was whiter than milk, then it was turned black by the sins of the children of Adam.'",
        "arabic_text": "حَدَّثَنَا قُتَيْبَةُ ، حَدَّثَنَا جَرِيرٌ ، عَنْ عَطَاءِ بْنِ السَّائِبِ ، عَنْ سَعِيدِ بْنِ جُبَيْرٍ ، عَنِ ابْنِ عَبَّاسٍ ، قَالَ قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم ‏ \"‏ نَزَلَ الْحَجَرُ الأَسْوَدُ مِنَ الْجَنَّةِ وَهُوَ أَشَدُّ بَيَاضًا مِنَ اللَّبَنِ فَسَوَّدَتْهُ خَطَايَا بَنِي آدَمَ ‏\" ‏.‏",
        "sunnah_url": "https://sunnah.com/tirmidhi:877"
    },
    {
        "id": "tirmidhi:961",
        "collection": "Jami` at-Tirmidhi",
        "reference": "Jami` at-Tirmidhi 961",
        "in_book_reference": "Book 9, Hadith 154",
        "category": "Heavenly Origin and Day of Resurrection Testimony of the Black Stone",
        "category_arabic": "أصل الحجر الأسود من الجنة وشهادته لمن استلمه يوم القيامة",
        "book_english": "The Book on Hajj",
        "book_arabic": "كتاب الحج عن رسول الله صلى الله عليه وسلم",
        "chapter_english": "Chapter: What Has Been Related About The Stone (Al-Hajar)",
        "chapter_arabic": "باب مَا جَاءَ فِي الْحَجَرِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "Ibn 'Abbas narrated that the Messenger of Allah (ﷺ) said about the (Black) Stone: 'By Allah! Allah will raise it on the Day of Resurrection with two eyes by which it sees and a tongue that it speaks with, testifying to whoever touched it in truth.'",
        "arabic_text": "حَدَّثَنَا مُحَمَّدُ بْنُ بَشَّارٍ ، حَدَّثَنَا مُحَمَّدُ بْنُ جَعْفَرٍ ، حَدَّثَنَا شُعْبَةُ ، عَنْ عَمْرِو بْنِ مُرَّةَ ، عَنْ عَبْدِ اللَّهِ بْنِ سَلَمَةَ ، عَنْ صُهَيْبٍ الْحَذَّاءِ ، عَنِ ابْنِ عَبَّاسٍ ، أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ فِي الْحَجَرِ ‏ \"‏ وَاللَّهِ لَيَبْعَثَنَّهُ اللَّهُ يَوْمَ الْقِيَامَةِ لَهُ عَيْنَانِ يُبْصِرُ بِهِمَا وَلِسَانٌ يَنْطِقُ بِهِ يَشْهَدُ عَلَى مَنْ اسْتَلَمَهُ بِحَقٍّ ‏\" ‏.‏",
        "sunnah_url": "https://sunnah.com/tirmidhi:961"
    },
    {
        "id": "ibnmajah:2944",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 2944",
        "in_book_reference": "Book 25, Hadith 66",
        "category": "Heavenly Origin and Day of Resurrection Testimony of the Black Stone",
        "category_arabic": "أصل الحجر الأسود من الجنة وشهادته لمن استلمه يوم القيامة",
        "book_english": "Chapters on Hajj Rituals",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: The Black Stone",
        "chapter_arabic": "باب الْحَجَرِ الأَسْوَدِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "It was narrated that Sa'eed bin Jubair said: I heard Ibn 'Abbas say: The Messenger of Allah (ﷺ) said: 'This Stone will be brought on the Day of Resurrection, and it will be given two eyes with which to see, and a tongue with which to speak, and it will bear witness for those who touched it in truth.'",
        "arabic_text": "حَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ ، حَدَّثَنَا عَلِيُّ بْنُ مُسْهِرٍ ، عَنِ ابْنِ أَبِي لَيْلَى ، عَنْ عَطَاءٍ ، عَنِ ابْنِ عَبَّاسٍ ، قَالَ قَالَ رَسُولُ اللَّهِ ـ صلى الله عليه وسلم ـ ‏ \"‏ لَيَأْتِيَنَّ هَذَا الْحَجَرُ يَوْمَ الْقِيَامَةِ وَلَهُ عَيْنَانِ يُبْصِرُ بِهِمَا وَلِسَانٌ يَنْطِقُ بِهِ يَشْهَدُ عَلَى مَنْ يَسْتَلِمُهُ بِحَقٍّ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:2944"
    },

    # Miracle, Nourishment & Cure of Zamzam Water
    {
        "id": "ibnmajah:3062",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 3062",
        "in_book_reference": "Book 25, Hadith 184",
        "category": "Miracle, Nourishment & Cure of Zamzam Water",
        "category_arabic": "بركة ماء زمزم والشرب بنية الاستجابة والشفاء",
        "book_english": "Chapters on Hajj Rituals",
        "book_arabic": "كتاب المناسك",
        "chapter_english": "Chapter: Drinking Zamzam Water",
        "chapter_arabic": "باب الشُّرْبِ مِنْ زَمْزَمَ",
        "grade": "Hasan (Darussalam)",
        "english_text": "It was narrated that Jabir bin 'Abdullah said: 'I heard the Messenger of Allah (ﷺ) say: The water of Zamzam is for whatever it is drunk for.'",
        "arabic_text": "حَدَّثَنَا هِشَامُ بْنُ عَمَّارٍ ، حَدَّثَنَا الْوَلِيدُ بْنُ مُسْلِمٍ ، قَالَ قَالَ ابْنُ جُرَيْجٍ عَنْ عَطَاءٍ ، عَنْ جَابِرِ بْنِ عَبْدِ اللَّهِ ، قَالَ سَمِعْتُ رَسُولَ اللَّهِ ـ صلى الله عليه وسلم ـ يَقُولُ ‏ \"‏ مَاءُ زَمْزَمَ لِمَا شُرِبَ لَهُ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:3062"
    },
    {
        "id": "muslim:2473",
        "collection": "Sahih Muslim",
        "reference": "Sahih Muslim 2473",
        "in_book_reference": "Book 44, Hadith 192",
        "category": "Miracle, Nourishment & Cure of Zamzam Water",
        "category_arabic": "بركة ماء زمزم والشرب بنية الاستجابة والشفاء",
        "book_english": "The Book of the Merits of the Companions",
        "book_arabic": "كتاب فضائل الصحابة رضى الله تعالى عنهم",
        "chapter_english": "Chapter: The Merits of Abu Dharr (RA)",
        "chapter_arabic": "باب مِنْ فَضَائِلِ أَبِي ذَرٍّ رضى الله عنه",
        "grade": "Sahih (Sahih Muslim - Authentic)",
        "english_text": "Abu Dharr reported that the Messenger of Allah (ﷺ) said regarding the water of Zamzam: 'Verily, it is blessed; verily, it is nourishing food (and a cure for illness).'",
        "arabic_text": "عَنْ أَبِي ذَرٍّ رضي الله عنه أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ فِي مَاءِ زَمْزَمَ: ‏\"‏ إِنَّهَا مُبَارَكَةٌ إِنَّهَا طَعَامُ طُعْمٍ ‏\"‏ (وَزَادَ الْبَزَّارُ وَغَيْرُهُ: «وَشِفَاءُ سُقْمٍ»)‏.‏",
        "sunnah_url": "https://sunnah.com/muslim:2473"
    },

    # 100,000x Multiplied Prayer in Masjid al-Haram
    {
        "id": "ibnmajah:1406",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 1406",
        "in_book_reference": "Book 5, Hadith 604",
        "category": "100,000x Multiplied Prayer in Masjid al-Haram during Umrah",
        "category_arabic": "مضاعفة الصلاة في المسجد الحرام بمائة ألف صلاة",
        "book_english": "Establishing the Prayer and the Sunnah Regarding Them",
        "book_arabic": "كتاب إقامة الصلاة والسنة فيها",
        "chapter_english": "Chapter: Virtue of prayer in the Prophet's Mosque and the Sacred Mosque",
        "chapter_arabic": "باب مَا جَاءَ فِي فَضْلِ الصَّلاَةِ فِي مَسْجِدِ رَسُولِ اللَّهِ صلى الله عليه وسلم وَمَسْجِدِ بَيْتِ الْمَقْدِسِ",
        "grade": "Sahih (Darussalam)",
        "english_text": "It was narrated that Abu Hurairah and Jabir said: The Messenger of Allah (ﷺ) said: 'One prayer in this mosque of mine is better than one thousand prayers elsewhere, except the Sacred Mosque; and one prayer in the Sacred Mosque is better than one hundred thousand prayers elsewhere.'",
        "arabic_text": "حَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ ، حَدَّثَنَا أَبُو خَالِدٍ الأَحْمَرُ ، عَنِ ابْنِ عَجْلاَنَ ، عَنْ سَعِيدِ بْنِ أَبِي سَعِيدٍ ، عَنْ أَبِي هُرَيْرَةَ ، أَنَّ رَسُولَ اللَّهِ ـ صلى الله عليه وسلم ـ قَالَ ‏ \"‏ صَلاَةٌ فِي مَسْجِدِي هَذَا أَفْضَلُ مِنْ أَلْفِ صَلاَةٍ فِيمَا سِوَاهُ إِلاَّ الْمَسْجِدَ الْحَرَامَ، وَصَلاَةٌ فِي الْمَسْجِدِ الْحَرَامِ أَفْضَلُ مِنْ مِائَةِ أَلْفِ صَلاَةٍ فِيمَا سِوَاهُ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:1406"
    },

    # The Prophet's Sunnah of Four Umrahs in Dhu al-Qa'dah
    {
        "id": "bukhari:1778",
        "collection": "Sahih al-Bukhari",
        "reference": "Sahih al-Bukhari 1778",
        "in_book_reference": "Book 26, Hadith 5",
        "category": "The Prophet's Sunnah of Four Umrahs in Dhu al-Qa'dah",
        "category_arabic": "سنة النبي ﷺ في أداء العمرة في ذي القعدة",
        "book_english": "'Umrah (Minor Pilgrimage)",
        "book_arabic": "كتاب العمرة",
        "chapter_english": "Chapter: How many 'Umra did the Prophet perform?",
        "chapter_arabic": "باب كَمِ اعْتَمَرَ النَّبِيُّ صلى الله عليه وسلم",
        "grade": "Sahih (Sahih al-Bukhari - Authentic)",
        "english_text": "Narrated Qatada: I asked Anas (RA): 'How many 'Umras did Allah's Messenger (ﷺ) perform?' He replied, 'Four, all of them in Dhu al-Qa'dah except the one performed with his Hajj: The 'Umra from Al-Hudaibiya in Dhu al-Qa'dah, the 'Umra of the following year in Dhu al-Qa'dah, the 'Umra from Al-Ji'rana where he distributed the war spoils of Hunain in Dhu al-Qa'dah, and the 'Umra with his Hajj.'",
        "arabic_text": "حَدَّثَنَا هُدْبَةُ بْنُ خَالِدٍ ، حَدَّثَنَا هَمَّامٌ ، عَنْ قَتَادَةَ ، أَنَّ أَنَسًا ـ رضى الله عنه ـ أَخْبَرَهُ قَالَ اعْتَمَرَ رَسُولُ اللَّهِ صلى الله عليه وسلم أَرْبَعَ عُمَرٍ، كُلَّهُنَّ فِي ذِي الْقَعْدَةِ، إِلاَّ الَّتِي مَعَ حَجَّتِهِ: عُمْرَةً مِنَ الْحُدَيْبِيَةِ فِي ذِي الْقَعْدَةِ، وَعُمْرَةً مِنَ الْعَامِ الْمُقْبِلِ فِي ذِي الْقَعْدَةِ، وَعُمْرَةً مِنْ جِعْرَانَةَ، حَيْثُ قَسَمَ غَنَائِمَ حُنَيْنٍ فِي ذِي الْقَعْدَةِ، وَعُمْرَةً مَعَ حَجَّتِهِ‏.‏",
        "sunnah_url": "https://sunnah.com/bukhari:1778"
    },
    {
        "id": "muslim:1253a",
        "collection": "Sahih Muslim",
        "reference": "Sahih Muslim 1253 a",
        "in_book_reference": "Book 15, Hadith 243",
        "category": "The Prophet's Sunnah of Four Umrahs in Dhu al-Qa'dah",
        "category_arabic": "سنة النبي ﷺ في أداء العمرة في ذي القعدة",
        "book_english": "The Book of Pilgrimage",
        "book_arabic": "كتاب الحج",
        "chapter_english": "Chapter: The number of 'Umrahs performed by the Prophet and their timing",
        "chapter_arabic": "باب بَيَانِ عَدَدِ عُمَرِ النَّبِيِّ صلى الله عليه وسلم وَزَمَانِهِنَّ",
        "grade": "Sahih (Sahih Muslim - Authentic)",
        "english_text": "Qatada reported that he asked Anas (Allah be pleased with him) how many 'Umras Allah's Messenger (ﷺ) had performed. He said: 'Four, and all of them were performed in the month of Dhu al-Qa'dah except the one he performed with his Hajj: The 'Umrah from al-Hudaibiyah, the 'Umrah of the next year, the 'Umrah from al-Ji'ranah, and the 'Umrah with his Hajj.'",
        "arabic_text": "حَدَّثَنَا مُحَمَّدُ بْنُ الْمُثَنَّى ، وَابْنُ، بَشَّارٍ قَالَ ابْنُ الْمُثَنَّى حَدَّثَنَا مُحَمَّدُ بْنُ جَعْفَرٍ ، حَدَّثَنَا شُعْبَةُ ، عَنْ قَتَادَةَ ، قَالَ سَأَلْتُ أَنَسًا رضى الله عنه كَمِ اعْتَمَرَ رَسُولُ اللَّهِ صلى الله عليه وسلم قَالَ أَرْبَعًا كُلَّهُنَّ فِي ذِي الْقَعْدَةِ إِلاَّ الَّتِي كَانَتْ مَعَ حَجَّتِهِ عُمْرَةً مِنَ الْحُدَيْبِيَةِ فِي ذِي الْقَعْدَةِ وَعُمْرَةً مِنَ الْعَامِ الْمُقْبِلِ فِي ذِي الْقَعْدَةِ وَعُمْرَةً مِنَ الْجِعْرَانَةِ حَيْثُ قَسَمَ غَنَائِمَ حُنَيْنٍ فِي ذِي الْقَعْدَةِ وَعُمْرَةً مَعَ حَجَّتِهِ ‏.‏",
        "sunnah_url": "https://sunnah.com/muslim:1253a"
    },

    # Spending on Pilgrimage Multiplied Seven Hundred Fold
    {
        "id": "ahmad:23000",
        "collection": "Musnad Ahmad",
        "reference": "Musnad Ahmad 23000 (Shu'ab al-Iman 3822)",
        "in_book_reference": "Musnad al-Ansar, Hadith 23000",
        "category": "Spending on Pilgrimage Multiplied Seven Hundred Fold",
        "category_arabic": "النفقة في الحج والعمرة كالنفقة في سبيل الله بسبعمائة ضعف",
        "book_english": "Musnad of the Companions",
        "book_arabic": "مسند الأنصار",
        "chapter_english": "Hadith of Buraidah al-Aslami",
        "chapter_arabic": "حديث بريدة الأسلمي رضي الله عنه",
        "grade": "Hasan li-ghayrihi (Musnad Ahmad)",
        "english_text": "Narrated Buraidah: The Messenger of Allah (ﷺ) said: 'Spending on Hajj and pilgrimage is like spending in the path of Allah: one Dirham is multiplied seven hundred times!'",
        "arabic_text": "عَنْ بُرَيْدَةَ رضي الله عنه أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ: «النَّفَقَةُ فِي الْحَجِّ كَالنَّفَقَةِ فِي سَبِيلِ اللَّهِ، الدِّرْهَمُ بِسَبْعِمِائَةِ ضِعْفٍ» (أخرجه أحمد والبيهقي في شعب الإيمان).",
        "sunnah_url": "https://sunnah.com"
    },

    # Deeds Equivalent to the Complete Reward of Umrah (Without Travel)
    {
        "id": "ibnmajah:1412",
        "collection": "Sunan Ibn Majah",
        "reference": "Sunan Ibn Majah 1412",
        "in_book_reference": "Book 5, Hadith 610",
        "category": "Deeds Equivalent to the Complete Reward of Umrah (Without Travel)",
        "category_arabic": "أعمال صالحة تعدل أجر حجة وعمرة تامة دون سفر",
        "book_english": "Establishing the Prayer and the Sunnah Regarding Them",
        "book_arabic": "كتاب إقامة الصلاة والسنة فيها",
        "chapter_english": "Chapter: What was said concerning prayer in the Mosque of Quba",
        "chapter_arabic": "باب مَا جَاءَ فِي الصَّلاَةِ فِي مَسْجِدِ قُبَاءٍ",
        "grade": "Sahih (Darussalam)",
        "english_text": "Sahl bin Hunaif narrated that: The Messenger of Allah (ﷺ) said: 'Whoever purifies himself in his house, then comes to the Quba' Mosque and offers one prayer therein, will have a reward like that for 'Umrah.'",
        "arabic_text": "حَدَّثَنَا أَبُو بَكْرِ بْنُ أَبِي شَيْبَةَ ، حَدَّثَنَا شَبَابَةُ ، حَدَّثَنَا ابْنُ أَبِي ذِئْبٍ ، عَنْ عُثْمَانَ بْنِ عَبْدِ الرَّحْمَنِ بْنِ أَبِي لَيْلَى ، عَنْ أَبِيهِ ، عَنْ سَهْلِ بْنِ حُنَيْفٍ ، قَالَ قَالَ رَسُولُ اللَّهِ ـ صلى الله عليه وسلم ـ ‏ \"‏ مَنْ تَطَهَّرَ فِي بَيْتِهِ ثُمَّ أَتَى مَسْجِدَ قُبَاءٍ فَصَلَّى فِيهِ صَلاَةً كَانَ لَهُ كَأَجْرِ عُمْرَةٍ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/ibnmajah:1412"
    },
    {
        "id": "tirmidhi:324",
        "collection": "Jami` at-Tirmidhi",
        "reference": "Jami` at-Tirmidhi 324",
        "in_book_reference": "Book 2, Hadith 176",
        "category": "Deeds Equivalent to the Complete Reward of Umrah (Without Travel)",
        "category_arabic": "أعمال صالحة تعدل أجر حجة وعمرة تامة دون سفر",
        "book_english": "The Book on Salat (Prayer)",
        "book_arabic": "كتاب الصلاة عن رسول الله صلى الله عليه وسلم",
        "chapter_english": "Chapter: What Has Been Related About The Prayer In Masjid Quba",
        "chapter_arabic": "باب مَا جَاءَ فِي الصَّلاَةِ فِي مَسْجِدِ قُبَاءٍ",
        "grade": "Hasan (Darussalam)",
        "english_text": "Usaid bin Zuhair Al-Ansari (who was among the Companions of the Prophet) narrated that the Prophet (ﷺ) said: 'A prayer in the Quba Mosque is like an 'Umrah.'",
        "arabic_text": "حَدَّثَنَا مُحَمَّدُ بْنُ بَشَّارٍ ، حَدَّثَنَا يَحْيَى بْنُ سَعِيدٍ ، عَنْ أَبِي جَعْفَرٍ الْخَطْمِيِّ ، حَدَّثَنِي عُمَارَةُ بْنُ خُزَيْمَةَ بْنِ ثَابِتٍ ، عَنْ عَمِّهِ ، أُسَيْدِ بْنِ ظُهَيْرٍ الأَنْصَارِيِّ ـ وَكَانَ مِنْ أَصْحَابِ النَّبِيِّ صلى الله عليه وسلم ـ عَنِ النَّبِيِّ صلى الله عليه وسلم قَالَ ‏ \"‏ صَلاَةٌ فِي مَسْجِدِ قُبَاءٍ كَعُمْرَةٍ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/tirmidhi:324"
    },
    {
        "id": "tirmidhi:586",
        "collection": "Jami` at-Tirmidhi",
        "reference": "Jami` at-Tirmidhi 586",
        "in_book_reference": "Book 6, Hadith 48",
        "category": "Deeds Equivalent to the Complete Reward of Umrah (Without Travel)",
        "category_arabic": "أعمال صالحة تعدل أجر حجة وعمرة تامة دون سفر",
        "book_english": "The Book on Traveling",
        "book_arabic": "كتاب السفر",
        "chapter_english": "Chapter: Sitting in the Masjid after Subh until Sunrise",
        "chapter_arabic": "باب ذِكْرِ مَا يُسْتَحَبُّ مِنَ الْجُلُوسِ فِي الْمَسْجِدِ بَعْدَ صَلاَةِ الصُّبْحِ حَتَّى تَطْلُعَ الشَّمْسُ",
        "grade": "Hasan (Darussalam)",
        "english_text": "Anas bin Malik narrated that the Messenger of Allah (ﷺ) said: 'Whoever prays Fajr in congregation, then sits remembering Allah until the sun has risen, then he prays two Rak'ah, then for him is the reward like that of a Hajj and 'Umrah.' He said: 'The Messenger of Allah (ﷺ) said: Complete, complete, complete.'",
        "arabic_text": "حَدَّثَنَا سُفْيَانُ بْنُ وَكِيعٍ ، حَدَّثَنَا يَحْيَى بْنُ فُضَيْلٍ ، عَنِ الْحَسَنِ بْنِ عَلِيِّ بْنِ عَاصِمٍ ، عَنْ أَبِيهِ ، عَنْ أَبِي إِسْمَاعِيلَ الْمُؤَدِّبِ ، عَنْ عَطَاءِ بْنِ السَّائِبِ ، عَنْ أَبِي الْبَخْتَرِيِّ ، عَنْ عَمْرِو بْنِ حُرَيْثٍ ، عَنْ عَلِيِّ بْنِ أَبِي طَالِبٍ ، وَعَنْ عَاصِمِ بْنِ ضَمْرَةَ ، عَنْ عَلِيٍّ ، قَالَ قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم: ‏\"‏ مَنْ صَلَّى الْفَجْرَ فِي جَمَاعَةٍ ثُمَّ قَعَدَ يَذْكُرُ اللَّهَ حَتَّى تَطْلُعَ الشَّمْسُ ثُمَّ صَلَّى رَكْعَتَيْنِ كَانَتْ لَهُ كَأَجْرِ حَجَّةٍ وَعُمْرَةٍ تَامَّةٍ تَامَّةٍ تَامَّةٍ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/tirmidhi:586"
    },
    {
        "id": "abudawud:558",
        "collection": "Sunan Abi Dawud",
        "reference": "Sunan Abi Dawud 558",
        "in_book_reference": "Book 2, Hadith 168",
        "category": "Deeds Equivalent to the Complete Reward of Umrah (Without Travel)",
        "category_arabic": "أعمال صالحة تعدل أجر حجة وعمرة تامة دون سفر",
        "book_english": "Prayer (Kitab Al-Salat)",
        "book_arabic": "كتاب الصلاة",
        "chapter_english": "Chapter: The virtue of walking to prayer",
        "chapter_arabic": "باب مَا جَاءَ فِي فَضْلِ الْمَشْىِ إِلَى الصَّلاَةِ",
        "grade": "Hasan (Al-Albani)",
        "english_text": "The Messenger of Allah (ﷺ) said: 'If anyone goes out from his house after performing ablution for saying the prescribed prayer in congregation, his reward will be like that of one who goes for hajj pilgrimage in Ihram. And he who goes out to say the mid-morning (Duha) voluntary prayer, and takes the trouble for this purpose, will take the reward like that of a person who performs 'Umrah.'",
        "arabic_text": "عَنْ أَبِي أُمَامَةَ أَنَّ رَسُولَ اللَّهِ صلى الله عليه وسلم قَالَ: ‏\"‏ مَنْ خَرَجَ مِنْ بَيْتِهِ مُتَطَهِّرًا إِلَى صَلاَةٍ مَكْتُوبَةٍ فَأَجْرُهُ كَأَجْرِ الْحَاجِّ الْمُحْرِمِ، وَمَنْ خَرَجَ إِلَى تَسْبِيحِ الضُّحَى لاَ يَنْصِبُهُ إِلاَّ إِيَّاهُ فَأَجْرُهُ كَأَجْرِ الْمُعْتَمِرِ وَصَلاَةٌ عَلَى أَثَرِ صَلاَةٍ لاَ لَغْوَ بَيْنَهُمَا كِتَابٌ فِي عِلِّيِّينَ ‏\"‏ ‏.‏",
        "sunnah_url": "https://sunnah.com/abudawud:558"
    },
    {
        "id": "tabarani:7473",
        "collection": "Al-Mu'jam al-Kabir (at-Tabarani)",
        "reference": "Al-Mu'jam al-Kabir 7473 / Sahih al-Targhib 86",
        "in_book_reference": "Kitab al-'Ilm, Hadith 7473",
        "category": "Deeds Equivalent to the Complete Reward of Umrah (Without Travel)",
        "category_arabic": "أعمال صالحة تعدل أجر حجة وعمرة تامة دون سفر",
        "book_english": "The Book of Knowledge",
        "book_arabic": "كتاب العلم",
        "chapter_english": "Chapter: The virtue of going to the mosque to seek knowledge",
        "chapter_arabic": "باب فضل الغدو إلى المسجد لطلب العلم",
        "grade": "Sahih (Al-Albani)",
        "english_text": "Abu Umamah reported from the Prophet (ﷺ): 'Whoever goes to the mosque desiring only to learn good or teach it, has the reward like that of a pilgrim performing a complete Hajj and 'Umrah.'",
        "arabic_text": "عَنْ أَبِي أُمَامَةَ عَنِ النَّبِيِّ صلى الله عليه وسلم قَالَ: «مَنْ غَدَا إِلَى الْمَسْجِدِ لا يُرِيدُ إِلا أَنْ يَتَعَلَّمَ خَيْرًا أَوْ يُعَلِّمَهُ، كَانَ لَهُ كَأَجْرِ حَاجٍّ تَامًّا حِجَّتُهُ» (أخرجه الطبراني في الكبير والحاكم وصححه، وصححه الألباني).",
        "sunnah_url": "https://sunnah.com"
    }
]

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root_dir, "data")
    json_path = os.path.join(data_dir, "fazail_umrah.json")
    csv_path = os.path.join(data_dir, "fazail_umrah.csv")
    md_path = os.path.join(data_dir, "FAZAIL_OF_UMRAH.md")

    # 1. Load current JSON
    with open(json_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    seen_ids = set(h["id"] for h in existing)
    added_count = 0

    for item in NEW_HADITHS:
        if item["id"] not in seen_ids:
            existing.append(item)
            seen_ids.add(item["id"])
            added_count += 1

    print(f"Added {added_count} new hadiths. Total: {len(existing)}")

    # 2. Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"Updated {json_path}")

    # 3. Save CSV
    fields = [
        "id", "collection", "reference", "category", "category_arabic",
        "grade", "in_book_reference", "book_english", "chapter_english",
        "english_text", "arabic_text", "sunnah_url"
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing)
    print(f"Updated {csv_path}")

    # 4. Generate Markdown
    categories = {}
    for h in existing:
        cat = h["category"]
        if cat not in categories:
            categories[cat] = {
                "arabic": h["category_arabic"],
                "hadiths": []
            }
        categories[cat]["hadiths"].append(h)

    collections = set(h["collection"] for h in existing)

    lines = []
    lines.append("# Fazā'il of 'Umrah (فضائل العمرة) — Comprehensive Compendium\n")
    lines.append("> **Comprehensive compilation of prophetic hadiths on the virtues, spiritual merits, and rewards of performing 'Umrah.**\n")
    lines.append(f"**Total Hadiths Compiled:** {len(existing)}  \n")
    lines.append(f"**Thematic Categories:** {len(categories)}  \n")
    lines.append(f"**Collections Included:** {', '.join(sorted(collections))}.\n")
    lines.append("\n---\n")

    lines.append("## Table of Contents")
    for i, (cat_name, cat_obj) in enumerate(categories.items(), 1):
        slug = cat_name.lower().replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace(',', '').replace("'", "")
        lines.append(f"{i}. [{cat_name} ({cat_obj['arabic']})](#{slug})")
    lines.append("\n---\n")

    for cat_name, cat_obj in categories.items():
        slug = cat_name.lower().replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace(',', '').replace("'", "")
        lines.append(f"## {cat_name}")
        lines.append(f"### {cat_obj['arabic']}\n")

        for h in cat_obj["hadiths"]:
            lines.append(f"#### [{h['reference']}]({h['sunnah_url']})")
            lines.append(f"- **Collection:** {h['collection']}")
            if h.get('grade'):
                lines.append(f"- **Grade:** `{h['grade']}`")
            if h.get('chapter_english'):
                lines.append(f"- **Chapter:** {h['chapter_english']} / {h.get('chapter_arabic', '')}")
            if h.get('in_book_reference'):
                lines.append(f"- **In-Book Reference:** {h['in_book_reference']}")
            lines.append("")
            lines.append(f"> **Arabic Text:**  \n> {h['arabic_text']}\n")
            lines.append(f"> **English Translation:**  \n> {h['english_text']}\n")
            lines.append(f"🔗 [View Hadith on Sunnah.com]({h['sunnah_url']})\n")
            lines.append("---\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Updated {md_path}")

if __name__ == "__main__":
    main()
