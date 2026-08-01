/* My Skills catalog — interaction only.
   The catalog markup is server-baked into index.html (good for SEO and works
   with JS disabled); this script adds language, theme, search, and filtering. */
(function () {
  "use strict";

  var root = document.documentElement;
  var LANG_KEY = "cs-lang";
  var THEME_KEY = "cs-theme";

  /* ---- language ------------------------------------------------------- */
  function applyLang(lang) {
    lang = lang === "zh" ? "zh" : "en";
    root.dataset.lang = lang;
    root.setAttribute("lang", lang === "zh" ? "zh-Hant" : "en");
    document.querySelectorAll("[data-lang-val]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.langVal === lang));
    });
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }

  /* ---- theme ---------------------------------------------------------- */
  function systemDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function currentTheme() {
    return root.dataset.theme || (systemDark() ? "dark" : "light");
  }
  function applyTheme(theme) {
    root.dataset.theme = theme === "dark" ? "dark" : "light";
    try { localStorage.setItem(THEME_KEY, root.dataset.theme); } catch (e) {}
  }

  /* ---- search + category filter --------------------------------------- */
  var cards = [];
  var groups = [];
  var searchInput, noResults;
  var activeCat = "all";
  var activeInv = "all";
  var query = "";

  function normalize(s) { return (s || "").toLowerCase().trim(); }

  function runFilter() {
    var q = normalize(query);
    var anyVisible = false;

    groups.forEach(function (group) {
      var cat = group.dataset.cat;
      var groupVisible = false;
      var groupCards = group.querySelectorAll(".card");
      groupCards.forEach(function (card) {
        var matchCat = activeCat === "all" || card.dataset.cat === activeCat;
        var matchInv = activeInv === "all" || card.dataset.inv === activeInv;
        var matchQ = q === "" || (card.dataset.search || "").indexOf(q) !== -1;
        var show = matchCat && matchInv && matchQ;
        card.hidden = !show;
        if (show) { groupVisible = true; anyVisible = true; }
      });
      group.hidden = !groupVisible;
    });

    if (noResults) noResults.hidden = anyVisible;
  }

  /* ---- clipboard ------------------------------------------------------ */
  function wireCopy() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-copy");
        var done = function () {
          var label = btn.querySelector(".copy-label");
          if (!label) return;
          var prevEn = label.querySelector(".l-en");
          var prevZh = label.querySelector(".l-zh");
          var oe = prevEn ? prevEn.textContent : "";
          var oz = prevZh ? prevZh.textContent : "";
          if (prevEn) prevEn.textContent = "Copied";
          if (prevZh) prevZh.textContent = "已複製";
          setTimeout(function () {
            if (prevEn) prevEn.textContent = oe;
            if (prevZh) prevZh.textContent = oz;
          }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(function () {});
        } else {
          var ta = document.createElement("textarea");
          ta.value = text; document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); done(); } catch (e) {}
          document.body.removeChild(ta);
        }
      });
    });
  }

  /* ---- boot ----------------------------------------------------------- */
  function init() {
    // restore persisted prefs (inline script in <head> already set them to
    // avoid flash; this re-syncs button state)
    var storedLang, storedTheme;
    try { storedLang = localStorage.getItem(LANG_KEY); } catch (e) {}
    try { storedTheme = localStorage.getItem(THEME_KEY); } catch (e) {}
    applyLang(storedLang || root.dataset.lang || "en");
    if (storedTheme) applyTheme(storedTheme);

    document.querySelectorAll("[data-lang-val]").forEach(function (b) {
      b.addEventListener("click", function () { applyLang(b.dataset.langVal); });
    });

    var themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        applyTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    }

    cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
    groups = Array.prototype.slice.call(document.querySelectorAll(".cat-group"));
    searchInput = document.getElementById("search");
    noResults = document.querySelector(".no-results");

    if (searchInput) {
      searchInput.addEventListener("input", function () {
        query = searchInput.value; runFilter();
      });
    }

    document.querySelectorAll(".chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        var group = chip.closest(".filters");
        if (chip.dataset.cat !== undefined) activeCat = chip.dataset.cat || "all";
        if (chip.dataset.inv !== undefined) activeInv = chip.dataset.inv || "all";
        var scope = group ? group.querySelectorAll(".chip") : [chip];
        scope.forEach(function (c) {
          c.setAttribute("aria-pressed", String(c === chip));
        });
        runFilter();
      });
    });

    wireCopy();
    runFilter();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
