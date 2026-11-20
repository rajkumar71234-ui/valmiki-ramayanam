/* Valmiki Ramayanam reading site.
 * One page; the part after # says what to show:
 *   #home            home page (also the default)
 *   #bala            list of sargams in Bala Kandam (ayodhya, aranya, kishkindha, sundara, yuddha, uttara)
 *   #bala-2          Bala Kandam, Sargam 2
 *   #bala-2-v15      ... opened at shloka 15
 * Content comes from the JSON files in /data.
 */
(function () {
  "use strict";

  var app = document.getElementById("app");
  var META = null;
  var sargaCache = {};

  // ---------- small helpers ----------
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function pad3(n) { return ("00" + n).slice(-3); }
  var DEV = "०१२३४५६७८९";
  function devNum(n) { return String(n).replace(/[0-9]/g, function (d) { return DEV[+d]; }); }
  function getJSON(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + " → " + r.status);
      return r.json();
    });
  }
  // Browser storage can be missing (private mode, embedded viewers): never let it break the page.
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("vr:" + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("vr:" + k, JSON.stringify(v)); } catch (e) { /* ignore */ } }
  };
  function kandamOf(k) {
    for (var i = 0; i < META.kandams.length; i++) if (META.kandams[i].n === k) return META.kandams[i];
    return null;
  }
  function kandamBySlug(slug) {
    for (var i = 0; i < META.kandams.length; i++) if (META.kandams[i].slug === slug) return META.kandams[i];
    return null;
  }
  function kandamLink(kd) { return "#" + kd.slug; }
  function sargamLink(kd, s, v) { return "#" + kd.slug + "-" + s + (v ? "-v" + v : ""); }
  function isReady(kd, s) { return (kd.ready || []).indexOf(s) >= 0; }
  function issueUrl(title, body) {
    var repo = META.site && META.site.repo;
    if (!repo) return null;
    return "https://github.com/" + repo + "/issues/new?title=" + encodeURIComponent(title) +
      "&body=" + encodeURIComponent(body);
  }
  function showError(msg) {
    app.innerHTML = '<div class="card error">பக்கத்தை ஏற்ற முடியவில்லை. ' + esc(msg) +
      ' <br><a href="#home">முகப்புக்குத் திரும்பு</a></div>';
  }
  function crumbs(items) {
    return '<nav class="crumbs" aria-label="வழி">' + items.map(function (it, i) {
      var sep = i ? '<span class="sep">›</span>' : "";
      return sep + (it.href ? '<a href="' + it.href + '">' + esc(it.text) + "</a>" : "<span>" + esc(it.text) + "</span>");
    }).join("") + "</nav>";
  }
  function setTitle(t) { document.title = t ? t + " · " + META.site.title : META.site.title + " — மூல ஸ்லோகங்கள், தமிழ்ப் பொருள்"; }

  // ---------- home ----------
  function renderHome() {
    setTitle("");
    var readyTotal = 0, total = 0, first = null;
    META.kandams.forEach(function (kd) {
      total += kd.sargas;
      readyTotal += (kd.ready || []).length;
      if (!first && kd.ready && kd.ready.length) first = { s: kd.ready[0], kd: kd };
    });
    var last = store.get("last", null);
    var lastKd = last ? kandamOf(last.k) : null;
    var html = '<section class="hero">' +
      "<h1>" + esc(META.site.title) + "</h1>" +
      '<p class="tag">' + esc(META.site.tagline) + "</p>" +
      "<p>வால்மீகி முனிவர் இயற்றிய மூல ராமாயணம். ஒவ்வொரு ஸர்க்கத்துக்கும் தமிழில் கதைச் சுருக்கம், " +
      "ஸம்ஸ்கிருத ஸ்லோகங்கள் (தமிழ் / தேவநாகரி எழுத்தில்), ஒவ்வொரு ஸ்லோகத்துக்கும் தமிழ்ப் பொருள், காட்சி ஓவியங்கள்.</p>" +
      '<p class="note">இது <b>வால்மீகியின் மூல நூலை மட்டுமே</b> பின்பற்றுகிறது — கம்ப ராமாயணமோ, தொலைக்காட்சித் தொடர்களில் வரும் கூடுதல் கதைகளோ இதில் இல்லை.</p>' +
      "</section>";

    if (lastKd && isReady(lastKd, last.s)) {
      html += '<div class="card continue"><div><small>கடைசியாகப் படித்தது</small><br><b>' +
        esc(lastKd.ta) + " · ஸர்க்கம் " + esc(last.s) + "</b> — " + esc(last.title || "") +
        '</div><a class="btn" href="' + sargamLink(lastKd, last.s) + '">தொடர்ந்து படிக்க</a></div>';
    }

    if (first) {
      var t = (first.kd.titles || {})[String(first.s)] || "";
      html += '<h2 class="section">இப்போது படிக்கலாம்</h2>' +
        '<a class="card feature" href="' + sargamLink(first.kd, first.s) + '">' +
        '<img src="img/' + first.kd.n + "/" + pad3(first.s) + '/chapter.svg" alt="" width="800" height="500">' +
        '<div class="body"><div class="eyebrow">' + esc(first.kd.ta) + " · ஸர்க்கம் " + first.s + "</div>" +
        "<h3>" + esc(t) + "</h3><p>ஸ்லோகங்கள், தமிழ்ப் பொருள், ஓவியங்களுடன் முழு ஸர்க்கம்.</p></div></a>";
    }

    html += '<h2 class="section">ஏழு காண்டங்கள்</h2><div class="kandams">';
    META.kandams.forEach(function (kd) {
      var r = (kd.ready || []).length, pct = Math.max(r ? 2 : 0, Math.round(100 * r / kd.sargas));
      html += '<a class="card kandam-card" href="' + kandamLink(kd) + '">' +
        '<span class="num">' + kd.n + "</span><h3>" + esc(kd.ta) + '</h3><span class="sa" lang="sa">' + esc(kd.sa) + "</span>" +
        "<p>" + esc(kd.about) + "</p>" +
        '<div class="progress" aria-hidden="true"><i style="width:' + pct + '%"></i></div>' +
        '<div class="progress-label">' + kd.sargas + " ஸர்க்கங்கள் · " + r + " தயார்</div></a>";
    });
    html += "</div>" +
      '<p class="legend" style="margin-top:14px">மொத்தம் ' + total + " ஸர்க்கங்கள்; இதுவரை " + readyTotal +
      " தயார். புதிய ஸர்க்கங்கள் தொடர்ந்து சேர்க்கப்படும்.</p>";
    app.innerHTML = html;
  }

  // ---------- kandam ----------
  function renderKandam(kd) {
    setTitle(kd.ta);
    var ready = kd.ready || [];
    var html = crumbs([{ text: "முகப்பு", href: "#home" }, { text: kd.ta }]) +
      '<h1 class="kandam-title">' + esc(kd.ta) + '</h1><div class="kandam-title-sa" lang="sa">' + esc(kd.sa) + "</div>" +
      "<p>" + esc(kd.about) + "</p>" +
      '<div class="progress" aria-hidden="true"><i style="width:' + Math.max(ready.length ? 2 : 0, Math.round(100 * ready.length / kd.sargas)) + '%"></i></div>' +
      '<div class="progress-label">' + kd.sargas + " ஸர்க்கங்கள் · " + ready.length + " தயார்</div>";

    if (ready.length) {
      html += '<div class="ready-list">';
      ready.forEach(function (s) {
        html += '<a class="card" href="' + sargamLink(kd, s) + '"><b>ஸர்க்கம் ' + s + "</b> — " +
          esc((kd.titles || {})[String(s)] || "") + "</a>";
      });
      html += "</div>";
    }

    html += '<h2 class="section">ஸர்க்கங்கள்</h2><div class="sargas">';
    for (var s = 1; s <= kd.sargas; s++) {
      if (isReady(kd, s)) {
        html += '<a class="sarga-tile ready" href="' + sargamLink(kd, s) + '" title="' + esc((kd.titles || {})[String(s)] || "") + '">' + s + "</a>";
      } else {
        html += '<span class="sarga-tile" title="விரைவில்">' + s + "</span>";
      }
    }
    html += '</div><p class="legend">● பச்சைப் புள்ளி உள்ளவை படிக்கத் தயார். மற்றவை விரைவில்.</p>';
    app.innerHTML = html;
  }

  // ---------- sargam ----------
  // Keep a short last word together with the danda / verse-number marker; long compounds wrap on their own.
  function lineWithEnd(text, end) {
    var i = text.lastIndexOf(" ");
    var head = i >= 0 ? text.slice(0, i + 1) : "", tail = i >= 0 ? text.slice(i + 1) : text;
    if (tail.length > 12) return esc(text) + ' <span class="nw">' + end + "</span>";
    return esc(head) + '<span class="nw">' + esc(tail) + " " + end + "</span>";
  }
  function slokaHtml(v) {
    var n = v.sa.length;
    var dev = v.sa.map(function (l, i) {
      return '<span class="line">' + lineWithEnd(l, i < n - 1 ? "।" : "॥ " + devNum(v.n) + " ॥") + "</span>";
    }).join("");
    var tam = v.ta_script.map(function (l, i) {
      return '<span class="line">' + lineWithEnd(l, i < n - 1 ? "।" : "॥ " + v.n + " ॥") + "</span>";
    }).join("");
    return '<p class="sloka dev" lang="sa">' + dev + '</p><p class="sloka tam" lang="sa-Taml">' + tam + "</p>";
  }

  function neighbour(kd, s, step) {
    var kx = kd, ss = s + step;
    if (ss < 1) { kx = kandamOf(kd.n - 1); if (!kx) return null; ss = kx.sargas; }
    else if (ss > kd.sargas) { kx = kandamOf(kd.n + 1); if (!kx) return null; ss = 1; }
    return { kd: kx, s: ss, ready: isReady(kx, ss) };
  }
  function pagerItem(o, label, cls) {
    if (!o) return '<span class="' + cls + '"><small>' + label + "</small>—</span>";
    var name = esc(o.kd.ta) + " " + o.s;
    if (o.ready) return '<a class="' + cls + '" href="' + sargamLink(o.kd, o.s) + '"><small>' + label + "</small>" + name + "</a>";
    return '<span class="' + cls + '"><small>' + label + "</small>" + name + " · விரைவில்</span>";
  }

  function renderSargam(kd, s, d, verse) {
    setTitle(kd.ta + " " + s + " — " + d.title);
    store.set("last", { k: kd.n, s: s, title: d.title });

    var html = crumbs([{ text: "முகப்பு", href: "#home" }, { text: kd.ta, href: kandamLink(kd) }, { text: "ஸர்க்கம் " + s }]) +
      '<header class="chap-head"><div class="eyebrow">' + esc(kd.ta) + " · ஸர்க்கம் " + s +
      " · " + d.verses.length + " ஸ்லோகங்கள்</div><h1>" + esc(d.title) + "</h1>" +
      (d.subtitle ? '<p class="sub">' + esc(d.subtitle) + "</p>" : "") + "</header>" +
      '<figure class="card hero-fig"><img src="' + esc(d.chapter_image.src) + '" alt="' + esc(d.chapter_image.alt) +
      '" width="800" height="500"><figcaption>' + esc(d.chapter_image.alt) + "</figcaption></figure>" +
      '<section class="card story"><div class="story-head"><h2>கதைச் சுருக்கம்</h2>' +
      (Speech.ok ? '<button type="button" class="listen" id="listenStory">' + ICON.speaker + "கேட்க</button>" : "") + "</div>" +
      d.story.map(function (p, i) { return '<p id="sp' + i + '">' + esc(p) + "</p>"; }).join("") + "</section>";

    html += '<div class="toolbar" role="toolbar" aria-label="படிக்கும் அமைப்பு">' +
      '<div class="seg" id="scriptSeg" aria-label="ஸ்லோக எழுத்து">' +
      '<button type="button" data-v="ta">தமிழ்</button><button type="button" data-v="dev" class="dev">देवनागरी</button><button type="button" data-v="both">இரண்டும்</button></div>' +
      '<span class="spacer"></span>' +
      '<div class="seg" aria-label="எழுத்து அளவு"><button type="button" id="fsDown" aria-label="எழுத்தைச் சிறிதாக்கு">அ−</button><button type="button" id="fsUp" aria-label="எழுத்தைப் பெரிதாக்கு">அ+</button></div>' +
      "</div>" +
      '<details class="howto"><summary>தமிழ் எழுத்தில் ஸம்ஸ்கிருதம் படிப்பது எப்படி?</summary><div>' +
      "எழுத்தின் மேலுள்ள சிறிய எண் ஒலியைக் குறிக்கிறது:<br>" +
      "<b>²</b> — மூச்சுடன் (kh, ch, ṭh, th, ph) · <b>³</b> — மென்மையாக (g, j, ḍ, d, b) · <b>⁴</b> — மென்மை + மூச்சு (gh, jh, ḍh, dh, bh)<br>" +
      "உதாரணம்: <b>த⁴ர்ம</b> = dharma, <b>ப⁴க³வான்</b> = bhagavān, <b>ஶ</b> = ś (śloka), <b>(அ)</b> = ऽ</div></details>" +
      (Speech.ok ? '<button type="button" class="listen big" id="listenVerses">' + ICON.speaker + "எல்லா ஸ்லோகங்களையும் தமிழ்ப் பொருளுடன் கேட்க</button>" : "");

    d.scenes.forEach(function (sc) {
      html += '<section class="scene" id="scene' + sc.id + '"><div class="scene-head"><span class="badge">காட்சி ' + sc.id +
        "</span><h3>" + esc(sc.title) + '</h3><span class="range">ஸ்லோ. ' + sc.from + (sc.to > sc.from ? "–" + sc.to : "") + "</span></div>" +
        '<figure class="card scene-fig"><img loading="lazy" src="' + esc(sc.src) + '" alt="' + esc(sc.caption) +
        '" width="800" height="500"><figcaption>' + esc(sc.caption) + "</figcaption></figure>";
      for (var i = sc.from; i <= sc.to; i++) {
        var v = d.verses[i - 1];
        var rep = issueUrl("பிழை: " + kd.ta + " " + s + "." + v.n,
          "காண்டம் " + kd.n + ", ஸர்க்கம் " + s + ", ஸ்லோகம் " + v.n + "\n\nஎன்ன பிழை? (ஸம்ஸ்கிருதம் / தமிழ்ப் பொருள் / ஓவியம்):\n\n");
        html += '<article class="card verse" id="v' + v.n + '"><span class="vnum">' + s + "." + v.n + "</span>" +
          slokaHtml(v) +
          '<p class="meaning"><b>பொருள்</b>' + esc(v.meaning) + "</p>" +
          '<div class="vtools">' + (Speech.ok ? '<button type="button" data-listen="' + v.n + '">' + ICON.speakerSm + "இங்கிருந்து கேட்க</button>" : "") +
          '<button type="button" data-copy="' + v.n + '">இணைப்பை நகலெடு</button>' +
          (rep ? '<a href="' + rep + '" target="_blank" rel="noopener">பிழை தெரிவிக்க</a>' : "") + "</div></article>";
      }
      html += "</section>";
    });

    if (d.colophon_ta) html += '<p class="colophon">' + esc(d.colophon_ta) + "</p>";
    html += '<nav class="pager">' + pagerItem(neighbour(kd, s, -1), "← முந்தைய ஸர்க்கம்", "prev") +
      pagerItem(neighbour(kd, s, 1), "அடுத்த ஸர்க்கம் →", "next") + "</nav>";
    html += '<p class="legend">' + esc(d.source || "") + "</p>";

    app.innerHTML = html;
    wireSargamControls(kd, s, d);
    if (verse) {
      var el = document.getElementById("v" + verse);
      if (el) setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 30);
    }
  }

  function applyScript(v) {
    document.body.classList.remove("script-ta", "script-dev", "script-both");
    document.body.classList.add("script-" + v);
    var btns = document.querySelectorAll("#scriptSeg button");
    for (var i = 0; i < btns.length; i++) btns[i].setAttribute("aria-pressed", btns[i].getAttribute("data-v") === v ? "true" : "false");
  }
  function applyFont(px) { document.documentElement.style.setProperty("--fs", px + "px"); }

  function wireSargamControls(kd, s, d) {
    applyScript(store.get("script", "ta"));
    var fs = store.get("fs", 17);
    applyFont(fs);
    document.getElementById("scriptSeg").onclick = function (e) {
      var b = e.target.closest("button"); if (!b) return;
      var v = b.getAttribute("data-v"); applyScript(v); store.set("script", v);
    };
    document.getElementById("fsUp").onclick = function () { fs = Math.min(24, fs + 1); applyFont(fs); store.set("fs", fs); };
    document.getElementById("fsDown").onclick = function () { fs = Math.max(14, fs - 1); applyFont(fs); store.set("fs", fs); };
    var ls = document.getElementById("listenStory");
    if (ls) ls.onclick = function () { Player.start("story", d, 0); };
    var lv = document.getElementById("listenVerses");
    if (lv) lv.onclick = function () { Player.start("verses", d, 0); };
    app.onclick = function (e) {
      var lb = e.target.closest("button[data-listen]");
      if (lb) { Player.start("verses", d, parseInt(lb.getAttribute("data-listen"), 10) - 1); return; }
      var b = e.target.closest("button[data-copy]"); if (!b) return;
      var url = location.href.split("#")[0] + sargamLink(kd, s, b.getAttribute("data-copy"));
      var original = b.textContent;
      var say = function (t) { b.textContent = t; setTimeout(function () { b.textContent = original; }, 1800); };
      try {
        navigator.clipboard.writeText(url).then(function () { say("நகலெடுக்கப்பட்டது ✓"); },
          function () { say(url); });
      } catch (err) { say(url); }
    };
  }

  // ---------- read aloud (the phone's / browser's own text-to-speech voice) ----------
  var ICON = {
    speaker: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.6 6a8.6 8.6 0 0 1 0 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    speakerSm: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
    pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>',
    prev: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h2.4v14H6zM20 5v14L9 12z"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.6 5H18v14h-2.4zM4 5v14l11-7z"/></svg>',
    stop: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 6.5h11v11h-11z"/></svg>'
  };

  var Speech = (function () {
    var synth = window.speechSynthesis;
    var ok = !!(synth && window.SpeechSynthesisUtterance);
    var voices = [];
    function load() { try { voices = synth.getVoices() || []; } catch (e) { voices = []; } }
    if (ok) {
      load();
      try { synth.addEventListener("voiceschanged", load); } catch (e) { synth.onvoiceschanged = load; }
    }
    function voiceFor(prefix) {
      load();
      for (var i = 0; i < voices.length; i++) {
        var l = String(voices[i].lang || "").toLowerCase().replace(/_/g, "-");
        if (l === prefix || l.indexOf(prefix + "-") === 0) return voices[i];
      }
      return null;
    }
    return { ok: ok, synth: synth, voiceFor: voiceFor };
  })();

  // Text clean-up so the voice reads naturally
  function ttsTamil(t) { return String(t).replace(/ஶ/g, "ஷ"); }
  function ttsSanskritTamil(t) {
    return String(t).replace(/[¹²³⁴]/g, "").replace(/\(அ\)/g, "").replace(/ஶ/g, "ஷ")
      .replace(/:/g, "").replace(/\s+/g, " ").trim();
  }
  function sentences(t) {
    var parts = String(t).match(/[^.!?;—]+[.!?;—]*[”’"]*\s*/g) || [String(t)];
    var out = [];
    parts.forEach(function (p) {
      p = p.trim();
      if (!p) return;
      if (out.length && p.length < 12) out[out.length - 1] += " " + p; else out.push(p);
    });
    return out;
  }

  var Player = (function () {
    var st = { items: [], groups: [], i: 0, playing: false, paused: false, cur: null, title: "", errors: 0, note: "" };
    var bar = null;
    function $(id) { return document.getElementById(id); }

    function ensureBar() {
      if (bar) return;
      bar = document.createElement("div");
      bar.className = "player"; bar.id = "player"; bar.hidden = true;
      bar.setAttribute("role", "region"); bar.setAttribute("aria-label", "ஒலி இயக்கி");
      bar.innerHTML = '<div class="pl-info"><b id="plTitle"></b><span id="plPos"></span><span id="plMsg" class="pl-msg"></span></div>' +
        '<div class="pl-btns">' +
        '<button type="button" id="plPrev" aria-label="முந்தையது">' + ICON.prev + "</button>" +
        '<button type="button" id="plPlay" class="pl-main" aria-label="இடைநிறுத்து">' + ICON.pause + "</button>" +
        '<button type="button" id="plNext" aria-label="அடுத்தது">' + ICON.next + "</button>" +
        '<button type="button" id="plStop" aria-label="நிறுத்து">' + ICON.stop + "</button></div>";
      document.body.appendChild(bar);
      $("plPrev").onclick = prev;
      $("plNext").onclick = next;
      $("plStop").onclick = stop;
      $("plPlay").onclick = function () { if (st.paused) resume(); else pause(); };
    }

    function build(mode, d) {
      st.items = []; st.groups = [];
      var ta = Speech.voiceFor("ta");
      var dv = Speech.voiceFor("sa") || Speech.voiceFor("hi") || Speech.voiceFor("mr") || Speech.voiceFor("ne");
      st.note = ta ? "" : "இந்தக் கருவியில் தமிழ்க் குரல் கிடைக்கவில்லை. Android: Settings → Google Text-to-speech → தமிழ் குரலை நிறுவவும்.";
      function add(g, text, lang, voice, rate) {
        if (text && String(text).trim()) st.items.push({ g: g, text: String(text).trim(), lang: lang, voice: voice, rate: rate });
      }
      if (mode === "story") {
        st.title = "கதைச் சுருக்கம்";
        d.story.forEach(function (p, gi) {
          st.groups.push({ id: "sp" + gi, start: st.items.length, label: "பகுதி " + (gi + 1) + " / " + d.story.length });
          sentences(ttsTamil(p)).forEach(function (x) { add(gi, x, "ta-IN", ta, 0.95); });
        });
      } else {
        st.title = "ஸ்லோகங்களும் பொருளும்";
        d.verses.forEach(function (v, gi) {
          st.groups.push({ id: "v" + v.n, start: st.items.length, label: "ஸ்லோகம் " + v.n + " / " + d.verses.length });
          add(gi, "ஸ்லோகம் " + v.n + ".", "ta-IN", ta, 0.95);
          if (ta || !dv) v.ta_script.forEach(function (l) { add(gi, ttsSanskritTamil(l), "ta-IN", ta, 0.85); });
          else v.sa.forEach(function (l) { add(gi, l, dv.lang, dv, 0.85); });
          add(gi, "பொருள்.", "ta-IN", ta, 0.95);
          sentences(ttsTamil(v.meaning)).forEach(function (x) { add(gi, x, "ta-IN", ta, 0.95); });
        });
      }
    }

    function groupOf(i) { return st.items[i] ? st.items[i].g : -1; }
    function groupStart(g) { return st.groups[g] ? st.groups[g].start : st.items.length; }
    function msg(t) { if ($("plMsg")) $("plMsg").textContent = t || ""; }

    function show() {
      var g = groupOf(st.i);
      var old = document.querySelectorAll(".speaking");
      for (var k = 0; k < old.length; k++) old[k].classList.remove("speaking");
      var el = st.groups[g] ? document.getElementById(st.groups[g].id) : null;
      if (el) {
        el.classList.add("speaking");
        var r = el.getBoundingClientRect();
        if (r.top < 70 || r.top > window.innerHeight - 150) el.scrollIntoView({ block: "center", behavior: "smooth" });
      }
      $("plTitle").textContent = st.title;
      $("plPos").textContent = st.groups[g] ? st.groups[g].label : "";
      var b = $("plPlay");
      b.innerHTML = st.paused ? ICON.play : ICON.pause;
      b.setAttribute("aria-label", st.paused ? "தொடர்ந்து கேட்க" : "இடைநிறுத்து");
    }

    function cancelNow() {
      st.cur = null;
      try { Speech.synth.cancel(); } catch (e) { /* ignore */ }
    }

    function speakCurrent() {
      if (!st.playing || st.paused) return;
      if (st.i >= st.items.length) { stop(); return; }
      show();
      var it = st.items[st.i];
      var u = new SpeechSynthesisUtterance(it.text);
      u.lang = it.lang;
      if (it.voice) u.voice = it.voice;
      u.rate = it.rate || 1;
      u.onend = function () {
        if (u !== st.cur || !st.playing || st.paused) return;
        st.errors = 0;
        st.i++;
        speakCurrent();
      };
      u.onerror = function (e) {
        if (u !== st.cur) return;
        var er = e && e.error;
        if (er === "interrupted" || er === "canceled") return;
        st.errors++;
        if (st.errors >= 3) { msg("குரலை இயக்க முடியவில்லை. " + st.note); st.paused = true; st.cur = null; show(); return; }
        st.i++;
        setTimeout(speakCurrent, 150);
      };
      st.cur = u;
      try { Speech.synth.speak(u); } catch (e) { msg("குரலை இயக்க முடியவில்லை."); }
    }

    function go(i) {
      cancelNow();
      st.i = Math.max(0, Math.min(i, st.items.length - 1));
      st.paused = false;
      setTimeout(speakCurrent, 80);
    }

    function start(mode, d, fromGroup) {
      if (!Speech.ok) return;
      ensureBar();
      cancelNow();
      build(mode, d);
      st.playing = true; st.paused = false; st.errors = 0;
      st.i = groupStart(Math.max(0, Math.min(fromGroup || 0, st.groups.length - 1)));
      bar.hidden = false;
      document.body.classList.add("has-player");
      msg(st.note);
      show();
      setTimeout(speakCurrent, 80);
    }
    function pause() { if (!st.playing) return; st.paused = true; cancelNow(); show(); }
    function resume() { if (!st.playing) return; st.paused = false; show(); setTimeout(speakCurrent, 80); }
    function prev() { if (!st.playing) return; var g = groupOf(st.i); go(groupStart(Math.max(0, g - 1))); }
    function next() {
      if (!st.playing) return;
      var g = groupOf(st.i);
      if (g + 1 < st.groups.length) go(groupStart(g + 1)); else stop();
    }
    function stop() {
      st.playing = false; st.paused = false;
      cancelNow();
      var old = document.querySelectorAll(".speaking");
      for (var k = 0; k < old.length; k++) old[k].classList.remove("speaking");
      if (bar) bar.hidden = true;
      document.body.classList.remove("has-player");
    }
    return { start: start, stop: stop, pause: pause, resume: resume, prev: prev, next: next, state: st };
  })();
  window.__player = Player;

  // ---------- router ----------
  function route() {
    Player.stop();
    var h = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (!h || h === "home") { renderHome(); window.scrollTo(0, 0); return; }
    var m = h.match(/^([a-z]+)(?:-(\d+))?(?:-v(\d+))?$/);
    var kd = m ? kandamBySlug(m[1]) : null;
    if (!kd) { renderHome(); window.scrollTo(0, 0); return; }
    if (!m[2]) { renderKandam(kd); window.scrollTo(0, 0); return; }
    var s = parseInt(m[2], 10), verse = m[3] ? parseInt(m[3], 10) : 0;
    if (!isReady(kd, s)) {
      setTitle(kd.ta + " " + s);
      app.innerHTML = crumbs([{ text: "முகப்பு", href: "#home" }, { text: kd.ta, href: kandamLink(kd) }, { text: "ஸர்க்கம் " + s }]) +
        '<div class="card error">இந்த ஸர்க்கம் இன்னும் தயாராகவில்லை — விரைவில் சேர்க்கப்படும்.</div>';
      window.scrollTo(0, 0);
      return;
    }
    var key = kd.n + "/" + pad3(s);
    var go = function (d) { renderSargam(kd, s, d, verse); if (!verse) window.scrollTo(0, 0); };
    if (sargaCache[key]) return go(sargaCache[key]);
    app.innerHTML = '<div class="loading">ஏற்றுகிறது…</div>';
    getJSON("data/" + key + ".json").then(function (d) { sargaCache[key] = d; go(d); }).catch(function (e) { showError(e.message); });
  }

  // back-to-top button
  var topBtn = document.querySelector(".to-top");
  if (topBtn) {
    window.addEventListener("scroll", function () { topBtn.classList.toggle("show", window.scrollY > 900); }, { passive: true });
    topBtn.addEventListener("click", function () { window.scrollTo(0, 0); });
  }

  getJSON("data/kandams.json").then(function (meta) {
    META = meta;
    window.addEventListener("hashchange", route);
    route();
  }).catch(function (e) { showError(e.message); });
})();
