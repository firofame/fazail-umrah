#!/usr/bin/env python3
"""
Generates the modern local web viewer for Fazail of Umrah.
"""
import json
import os

def build():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(dir_path, "data", "fazail_umrah.json")
    out_html = os.path.join(dir_path, "index.html")

    with open(json_path, "r", encoding="utf-8") as f:
        hadiths = json.load(f)

    json_str = json.dumps(hadiths, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>فضائل العمرة — Fazā'il of 'Umrah</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            amiri: ['Amiri', 'serif', 'Traditional Arabic'],
            sans: ['Inter', 'system-ui', 'sans-serif'],
          }},
          colors: {{
            emerald: {{
              50: '#ecfdf5',
              100: '#d1fae5',
              600: '#059669',
              700: '#047857',
              800: '#065f46',
              900: '#064e3b',
              950: '#022c22',
            }},
            gold: {{
              400: '#fbbf24',
              500: '#f59e0b',
              600: '#d97706',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    .arabic-text {{
      font-family: 'Amiri', 'Traditional Arabic', serif;
      direction: rtl;
      line-height: 2.3;
      word-spacing: 2px;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: transparent;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #4b5563;
      border-radius: 9999px;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased transition-colors duration-200">

  <!-- Header -->
  <header class="border-b border-emerald-900/50 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-3">
            <span class="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-amber-300 bg-clip-text text-transparent">فضائل العمرة</span>
            <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-900/60 text-emerald-300 border border-emerald-700/50">Sunnah.com Data</span>
          </div>
          <p class="text-sm text-slate-400 mt-0.5">Prophetic Virtues & Merits of the Minor Pilgrimage ('Umrah)</p>
        </div>
        <button id="themeToggle" class="md:hidden p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white">
          🌙
        </button>
      </div>

      <!-- Quick Search & Actions -->
      <div class="flex items-center gap-3">
        <div class="relative flex-1 md:w-80">
          <input 
            type="text" 
            id="searchInput" 
            placeholder="Search hadith, narrator, Arabic, or ref..." 
            class="w-full pl-9 pr-4 py-2 text-sm rounded-xl bg-slate-800/90 border border-slate-700 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 placeholder-slate-500 text-slate-100 transition"
          >
          <svg class="w-4 h-4 text-slate-400 absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>

        <button id="bookmarksOnlyBtn" class="flex items-center gap-1.5 px-3 py-2 text-sm rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition">
          <span>⭐</span>
          <span class="hidden sm:inline">Saved</span>
          <span id="bookmarkCount" class="text-xs px-1.5 py-0.2 rounded-full bg-emerald-600 text-white">0</span>
        </button>

        <button id="desktopThemeToggle" class="hidden md:flex p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition">
          🌙
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- Stats Banner -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <div class="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-emerald-950/40 border border-emerald-900/30 flex flex-col">
        <span class="text-2xl font-bold text-emerald-400" id="totalCount">{len(hadiths)}</span>
        <span class="text-xs text-slate-400 uppercase tracking-wider font-medium mt-1">Ahadith Compiled</span>
      </div>
      <div class="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/80 border border-slate-800 flex flex-col">
        <span class="text-2xl font-bold text-amber-400">8</span>
        <span class="text-xs text-slate-400 uppercase tracking-wider font-medium mt-1">Thematic Virtues</span>
      </div>
      <div class="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/80 border border-slate-800 flex flex-col">
        <span class="text-2xl font-bold text-sky-400">9</span>
        <span class="text-xs text-slate-400 uppercase tracking-wider font-medium mt-1">Major Collections</span>
      </div>
      <div class="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/80 border border-slate-800 flex flex-col">
        <span class="text-2xl font-bold text-emerald-300" id="activeShowingCount">{len(hadiths)}</span>
        <span class="text-xs text-slate-400 uppercase tracking-wider font-medium mt-1">Showing Now</span>
      </div>
    </div>

    <!-- Category Filter Tabs -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-400">Filter by Prophetic Virtue (الفضائل)</h2>
        <button id="resetFiltersBtn" class="text-xs text-emerald-400 hover:text-emerald-300 hidden">Reset Filters</button>
      </div>
      <div class="flex flex-wrap gap-2" id="categoryFiltersContainer">
        <!-- Categories populated via JS -->
      </div>
    </div>

    <!-- Collection Filter & Sorters -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
      <div class="flex items-center gap-2 flex-wrap">
        <span class="text-xs text-slate-400 font-medium">Collection:</span>
        <select id="collectionFilter" class="text-xs rounded-lg bg-slate-800 border border-slate-700 text-slate-200 px-3 py-1.5 focus:outline-none focus:border-emerald-500">
          <option value="ALL">All Collections</option>
        </select>
      </div>
      <div class="text-xs text-slate-500">
        Data scraped from <a href="https://sunnah.com" target="_blank" class="text-emerald-400 hover:underline">Sunnah.com</a>
      </div>
    </div>

    <!-- Hadith Cards List -->
    <div id="hadithsList" class="space-y-6">
      <!-- Hadith cards injected by JS -->
    </div>

    <!-- Empty State -->
    <div id="emptyState" class="hidden py-16 text-center">
      <div class="text-4xl mb-3">🔍</div>
      <h3 class="text-lg font-semibold text-slate-200">No matching hadiths found</h3>
      <p class="text-sm text-slate-400 mt-1 max-w-sm mx-auto">Try adjusting your search keywords or clear your active filters.</p>
      <button onclick="resetAllFilters()" class="mt-4 px-4 py-2 text-xs font-medium rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white transition">Clear All Filters</button>
    </div>

  </main>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none px-4 py-3 rounded-xl shadow-2xl bg-emerald-700 text-white text-sm font-medium flex items-center gap-2">
    <span>✓</span>
    <span id="toastMessage">Hadith copied to clipboard!</span>
  </div>

  <script>
    // Embedded Hadith Database
    const ALL_HADITHS = {json_str};

    let currentCategory = 'ALL';
    let currentCollection = 'ALL';
    let searchQuery = '';
    let bookmarksOnly = false;

    // LocalStorage bookmarks
    const getBookmarks = () => {{
      try {{
        return JSON.parse(localStorage.getItem('umrah_bookmarks') || '[]');
      }} catch (e) {{
        return [];
      }}
    }};

    const toggleBookmark = (id) => {{
      let b = getBookmarks();
      if (b.includes(id)) {{
        b = b.filter(x => x !== id);
        showToast('Removed from saved ahadith');
      }} else {{
        b.push(id);
        showToast('Added to saved ahadith');
      }}
      localStorage.setItem('umrah_bookmarks', JSON.stringify(b));
      updateBookmarkUI();
      renderHadiths();
    }};

    const updateBookmarkUI = () => {{
      const count = getBookmarks().length;
      document.getElementById('bookmarkCount').textContent = count;
      const btn = document.getElementById('bookmarksOnlyBtn');
      if (bookmarksOnly) {{
        btn.classList.add('bg-emerald-700', 'text-white', 'border-emerald-600');
        btn.classList.remove('bg-slate-800', 'text-slate-300', 'border-slate-700');
      }} else {{
        btn.classList.remove('bg-emerald-700', 'text-white', 'border-emerald-600');
        btn.classList.add('bg-slate-800', 'text-slate-300', 'border-slate-700');
      }}
    }};

    const showToast = (msg) => {{
      const toast = document.getElementById('toast');
      document.getElementById('toastMessage').textContent = msg;
      toast.classList.remove('translate-y-20', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
      setTimeout(() => {{
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-20', 'opacity-0');
      }}, 2500);
    }};

    const copyHadith = (id) => {{
      const h = ALL_HADITHS.find(x => x.id === id);
      if (!h) return;
      const text = `${{h.reference}} (${{h.collection}})\\n\\nArabic:\\n${{h.arabic_text}}\\n\\nEnglish:\\n${{h.english_text}}\\n\\nReference: ${{h.sunnah_url}}`;
      navigator.clipboard.writeText(text).then(() => {{
        showToast(`Copied ${{h.reference}} to clipboard!`);
      }});
    }};

    // Initialize Category Filters
    const initFilters = () => {{
      const categories = {{}};
      const collections = new Set();

      ALL_HADITHS.forEach(h => {{
        if (!categories[h.category]) {{
          categories[h.category] = {{ arabic: h.category_arabic, count: 0 }};
        }}
        categories[h.category].count += 1;
        collections.add(h.collection);
      }});

      const container = document.getElementById('categoryFiltersContainer');
      container.innerHTML = `
        <button onclick="selectCategory('ALL')" data-category="ALL" class="cat-btn px-3.5 py-1.5 rounded-xl text-xs font-medium transition bg-emerald-600 text-white shadow-sm shadow-emerald-900/50">
          All Virtues (${{ALL_HADITHS.length}})
        </button>
      `;

      Object.entries(categories).forEach(([name, info]) => {{
        const btn = document.createElement('button');
        btn.onclick = () => selectCategory(name);
        btn.dataset.category = name;
        btn.className = 'cat-btn px-3 py-1.5 rounded-xl text-xs font-medium transition bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700/60';
        btn.innerHTML = `${{name}} <span class="opacity-60 ml-1">(${{info.count}})</span>`;
        container.appendChild(btn);
      }});

      // Collections Dropdown
      const colSelect = document.getElementById('collectionFilter');
      Array.from(collections).sort().forEach(c => {{
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        colSelect.appendChild(opt);
      }});
    }};

    const selectCategory = (cat) => {{
      currentCategory = cat;
      document.querySelectorAll('.cat-btn').forEach(btn => {{
        if (btn.dataset.category === cat) {{
          btn.className = 'cat-btn px-3.5 py-1.5 rounded-xl text-xs font-medium transition bg-emerald-600 text-white shadow-sm shadow-emerald-900/50';
        }} else {{
          btn.className = 'cat-btn px-3 py-1.5 rounded-xl text-xs font-medium transition bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700/60';
        }}
      }});
      document.getElementById('resetFiltersBtn').classList.toggle('hidden', cat === 'ALL' && currentCollection === 'ALL' && !searchQuery && !bookmarksOnly);
      renderHadiths();
    }};

    const resetAllFilters = () => {{
      currentCategory = 'ALL';
      currentCollection = 'ALL';
      searchQuery = '';
      bookmarksOnly = false;
      document.getElementById('searchInput').value = '';
      document.getElementById('collectionFilter').value = 'ALL';
      selectCategory('ALL');
      updateBookmarkUI();
      renderHadiths();
    }};

    const renderHadiths = () => {{
      const listEl = document.getElementById('hadithsList');
      const emptyEl = document.getElementById('emptyState');
      const bookmarks = getBookmarks();

      const filtered = ALL_HADITHS.filter(h => {{
        if (currentCategory !== 'ALL' && h.category !== currentCategory) return false;
        if (currentCollection !== 'ALL' && h.collection !== currentCollection) return false;
        if (bookmarksOnly && !bookmarks.includes(h.id)) return false;
        if (searchQuery) {{
          const q = searchQuery.toLowerCase();
          const matchEng = h.english_text.toLowerCase().includes(q);
          const matchAra = h.arabic_text.includes(searchQuery);
          const matchRef = h.reference.toLowerCase().includes(q);
          const matchCat = h.category.toLowerCase().includes(q);
          const matchChap = (h.chapter_english || '').toLowerCase().includes(q);
          if (!matchEng && !matchAra && !matchRef && !matchCat && !matchChap) return false;
        }}
        return true;
      }});

      document.getElementById('activeShowingCount').textContent = filtered.length;

      if (filtered.length === 0) {{
        listEl.innerHTML = '';
        emptyEl.classList.remove('hidden');
        return;
      }}

      emptyEl.classList.add('hidden');
      listEl.innerHTML = filtered.map(h => {{
        const isBookmarked = bookmarks.includes(h.id);
        const gradeBadge = h.grade ? `
          <span class="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-emerald-950/60 text-emerald-400 border border-emerald-800/60">
            ${{h.grade}}
          </span>
        ` : '';

        const inBook = h.in_book_reference ? `
          <span class="text-xs text-slate-500">In-book: ${{h.in_book_reference}}</span>
        ` : '';

        const chapter = h.chapter_english ? `
          <div class="text-xs text-slate-400 flex items-center gap-1.5 flex-wrap">
            <span class="text-slate-500">Chapter:</span>
            <span>${{h.chapter_english}}</span>
            ${{h.chapter_arabic ? `<span class="text-slate-500 font-amiri text-sm">(${{h.chapter_arabic}})</span>` : ''}}
          </div>
        ` : '';

        return `
          <article class="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-emerald-800/60 transition-all duration-200 shadow-lg shadow-black/20 flex flex-col gap-5">
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
              <div class="flex flex-wrap items-center gap-2.5">
                <a href="${{h.sunnah_url}}" target="_blank" class="text-base font-bold text-emerald-400 hover:text-emerald-300 hover:underline flex items-center gap-1.5">
                  ${{h.reference}}
                  <svg class="w-3.5 h-3.5 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
                <span class="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  ${{h.collection}}
                </span>
                ${{gradeBadge}}
              </div>

              <div class="flex items-center gap-2">
                <button onclick="toggleBookmark('${{h.id}}')" title="Save Hadith" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">
                  ${{isBookmarked ? '⭐' : '☆'}}
                </button>
                <button onclick="copyHadith('${{h.id}}')" title="Copy Hadith Text" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition text-xs flex items-center gap-1 px-2.5">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"></path></svg>
                  Copy
                </button>
              </div>
            </div>

            <div class="flex flex-col gap-1.5">
              <div class="flex items-center gap-2 text-xs font-medium text-amber-400/90">
                <span>✦ ${{h.category}}</span>
                <span class="text-slate-600">•</span>
                <span class="font-amiri text-sm text-amber-300/80">${{h.category_arabic}}</span>
              </div>
              ${{chapter}}
            </div>

            <div class="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <p class="arabic-text text-xl sm:text-2xl text-amber-100/95 leading-loose">
                ${{h.arabic_text}}
              </p>
            </div>

            <div class="text-slate-300 text-sm sm:text-base leading-relaxed pl-3 border-l-2 border-emerald-500/70">
              <p>${{h.english_text}}</p>
            </div>

            <div class="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-800/60">
              <div>${{inBook}}</div>
              <a href="${{h.sunnah_url}}" target="_blank" class="text-emerald-400 hover:text-emerald-300 hover:underline">
                View on Sunnah.com →
              </a>
            </div>
          </article>
        `;
      }}).join('');
    }};

    document.getElementById('searchInput').addEventListener('input', (e) => {{
      searchQuery = e.target.value.trim();
      renderHadiths();
    }});

    document.getElementById('collectionFilter').addEventListener('change', (e) => {{
      currentCollection = e.target.value;
      renderHadiths();
    }});

    document.getElementById('bookmarksOnlyBtn').addEventListener('click', () => {{
      bookmarksOnly = !bookmarksOnly;
      updateBookmarkUI();
      renderHadiths();
    }});

    document.getElementById('resetFiltersBtn').addEventListener('click', resetAllFilters);

    const toggleTheme = () => {{
      const html = document.documentElement;
      if (html.classList.contains('dark')) {{
        html.classList.remove('dark');
        document.body.classList.remove('bg-slate-950', 'text-slate-100');
        document.body.classList.add('bg-slate-50', 'text-slate-900');
      }} else {{
        html.classList.add('dark');
        document.body.classList.add('bg-slate-950', 'text-slate-100');
        document.body.classList.remove('bg-slate-50', 'text-slate-900');
      }}
    }};
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    document.getElementById('desktopThemeToggle').addEventListener('click', toggleTheme);

    initFilters();
    updateBookmarkUI();
    renderHadiths();
  </script>
</body>
</html>
"""

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Successfully generated: {out_html}")

if __name__ == "__main__":
    build()
