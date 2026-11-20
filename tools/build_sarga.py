"""Build one sargam's data file for the website.

Reads
  content/<k>/<sss>.sa.wiki   raw Sanskrit text from Sanskrit Wikisource
  content/<k>/<sss>.ta.json   Tamil story, scene list and Tamil meanings
Writes
  data/<k>/<sss>.json         everything the chapter page needs
and marks the sargam as ready in data/kandams.json.

Usage (from the repo root):
  python3 tools/build_sarga.py 1 2 [--check path/to/dharmic_kanda.json]

--check compares every verse with a second source (DharmicData / IIT-K text)
and prints verses that differ a lot, so they can be reviewed by hand.
"""
import argparse
import difflib
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
from aksharamukha import transliterate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEV_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")
DEV_TO_ASCII = str.maketrans("०१२३४५६७८९", "0123456789")


def dev_num(n: int) -> str:
    return str(n).translate(DEV_DIGITS)


def to_tamil_script(line: str) -> str:
    """Devanagari Sanskrit -> Tamil script with superscript numbers (க² க³ க⁴)."""
    t = transliterate.process("Devanagari", "Tamil", line)
    t = t.replace("ʼ", "")      # modifier apostrophe used for anusvara/ṛ
    t = t.replace("꞉", ":")     # visarga sign -> colon, as in Tamil stotra books
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parse_wiki(raw: str):
    """Return {verse_no: [half-verse lines]} from Wikisource <poem> wikitext."""
    m = re.search(r"<poem>(.*?)</poem>", raw, re.S)
    if not m:
        sys.exit("No <poem> block found in the wiki source")
    body = m.group(1)
    body = body.replace("'''", "")
    verses = {}
    blocks = re.split(r"\n\s*\n", body)
    for block in blocks:
        lines = [ln.strip() for ln in block.strip().split("\n") if ln.strip()]
        if not lines:
            continue
        joined = ""
        for ln in lines:
            ln = ln.lstrip(":").strip()
            if joined.endswith("-"):
                joined = joined[:-1] + ln
            elif joined:
                joined += " " + ln
            else:
                joined = ln
        num = re.search(r"॥\s*([०-९0-9]+)\s*-\s*([०-९0-9]+)\s*-\s*([०-९0-9]+)\s*॥", joined)
        if not num:
            continue  # header / colophon lines
        vno = int(num.group(3).translate(DEV_TO_ASCII))
        text = joined[: num.start()]
        text = text.replace("।॥", "।").replace("॥", "।")
        parts = [p.strip() for p in text.split("।") if p.strip()]
        verses[vno] = parts
    return verses


def letters_only(s: str) -> str:
    s = re.sub(r"॥.*?॥", "", s)
    return re.sub(r"[^ऀ-ॣ०-ॿ]", "", s.replace("।", "").replace("॥", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kandam", type=int)
    ap.add_argument("sargam", type=int)
    ap.add_argument("--check", help="DharmicData kanda JSON for a second-source comparison")
    args = ap.parse_args()

    k, s = args.kandam, args.sargam
    sss = f"{s:03d}"
    wiki = (ROOT / "content" / str(k) / f"{sss}.sa.wiki").read_text(encoding="utf-8")
    ta = json.loads((ROOT / "content" / str(k) / f"{sss}.ta.json").read_text(encoding="utf-8"))

    verses = parse_wiki(wiki)
    for fix in ta.get("sanskrit_fixes", []):
        v = fix["verse"]
        before = " । ".join(verses[v])
        if fix["from"] not in before:
            sys.exit(f"Fix for verse {v} not applicable: {fix['from']!r} not found")
        verses[v] = [p.replace(fix["from"], fix["to"]) for p in verses[v]]

    n = max(verses)
    missing = [i for i in range(1, n + 1) if i not in verses]
    if missing:
        sys.exit(f"Missing verses in source: {missing}")
    if sorted(int(x) for x in ta["meanings"]) != list(range(1, n + 1)):
        sys.exit(f"Tamil meanings do not cover verses 1..{n}")
    covered = []
    for sc in ta["scenes"]:
        covered += list(range(sc["from"], sc["to"] + 1))
    if covered != list(range(1, n + 1)):
        sys.exit("Scenes must cover every verse exactly once, in order")

    out_verses = []
    for i in range(1, n + 1):
        sa_lines = verses[i]
        out_verses.append({
            "n": i,
            "sa": sa_lines,
            "ta_script": [to_tamil_script(x) for x in sa_lines],
            "meaning": ta["meanings"][str(i)],
        })

    if args.check:
        rows = json.loads(Path(args.check).read_text(encoding="utf-8"))
        other = {r["shloka"]: r["text"] for r in rows if r["sarg"] == s}
        print(f"second source: {len(other)} verses, wikisource: {n} verses")
        for i in range(1, n + 1):
            a = letters_only("".join(verses[i]))
            b = letters_only(other.get(i, ""))
            ratio = difflib.SequenceMatcher(None, a, b).ratio()
            flag = "  <-- review" if ratio < 0.85 else ""
            print(f"  v{i:3d} similarity {ratio:.2f}{flag}")

    img_base = f"img/{k}/{sss}/"
    data = {
        "kandam": k,
        "sargam": s,
        "title": ta["title"],
        "subtitle": ta.get("subtitle", ""),
        "summary": ta.get("summary", ""),
        "story": ta["story"],
        "chapter_image": {"src": img_base + ta["chapter_image"]["file"], "alt": ta["chapter_image"]["alt"]},
        "scenes": [
            {**{kk: vv for kk, vv in sc.items() if kk != "image"}, "src": img_base + sc["image"]}
            for sc in ta["scenes"]
        ],
        "verses": out_verses,
        "colophon_ta": ta.get("colophon_ta", ""),
        "source": "ஸம்ஸ்கிருத மூலம்: ஸம்ஸ்கிருத விக்கிமூலம் (रामायणम्), இரண்டாவது பதிப்புடன் ஒப்பிடப்பட்டது. தமிழ்ப் பொருளும் கதைச் சுருக்கமும் இந்தத் தளத்துக்காகப் புதிதாக எழுதப்பட்டவை.",
    }
    out = ROOT / "data" / str(k) / f"{sss}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    kp = ROOT / "data" / "kandams.json"
    kandams = json.loads(kp.read_text(encoding="utf-8"))
    for kd in kandams["kandams"]:
        if kd["n"] == k:
            ready = set(kd.get("ready", []))
            ready.add(s)
            kd["ready"] = sorted(ready)
            titles = kd.setdefault("titles", {})
            titles[str(s)] = ta["title"]
    kp.write_text(json.dumps(kandams, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({n} verses, {len(ta['scenes'])} scenes)")


if __name__ == "__main__":
    main()
