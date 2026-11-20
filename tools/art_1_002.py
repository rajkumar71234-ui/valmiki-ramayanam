"""Pictures for Bala Kandam, Sargam 2 (the krauncha birds and the first shloka).

Run from the repo root:  python3 tools/art_1_002.py
Writes img/1/002/chapter.svg and scene-1.svg ... scene-8.svg
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from art import *  # noqa: F401,F403

OUT_DIR = Path(__file__).resolve().parent.parent / "img" / "1" / "002"


def chapter():
    return svg(
        sky(), sun(640, 118, 36), cloud(170, 90, 1.1), cloud(470, 70, 0.8), cloud(720, 170, 0.7, 0.8),
        hills(286),
        tree(40, 312, 1.0, 1), tree(118, 306, 0.8, 0), tree(760, 318, 1.05, 2), tree(690, 304, 0.7, 1),
        river(300, 404), bank(404),
        grass_tufts([(60, 452), (380, 470), (745, 460), (520, 490)]),
        G(disciple("pot", pot=True, eye="happy"), x=112, y=468, s=1.12),
        G(valmiki("point", eye="open"), x=250, y=470, s=1.38),
        G(crane("walk"), x=520, y=446, s=1.15),
        G(crane("stand"), x=640, y=450, s=1.2, flip=True),
        defs=sky_defs("dawn"),
        title="தமஸா நதிக்கரையில் வால்மீகி முனிவரும் க்ரௌஞ்சப் பறவைகளும்")


def scene1():
    return svg(
        sky(), cloud(120, 80, 1.0), cloud(420, 60, 0.7),
        cloud(600, 236, 1.8, 0.97),
        sparkle(520, 150, 1.2), sparkle(700, 120, 0.9), sparkle(660, 260, 0.7),
        P("M690,170 q30,-30 70,-40 M700,196 q36,-26 80,-30", stroke="#ffffff", sw=4, opacity=0.9),
        hills(300), tree(40, 384, 1.1, 0), tree(745, 384, 0.95, 2),
        ground(380), hut(150, 384, 1.0),
        C(600, 150, 95, "url(#glow)", stroke="none"),
        G(narada("bless"), x=600, y=230, s=0.95, flip=True),
        G(disciple("namaste", eye="wonder", mouth_kind="smile"), x=262, y=466, s=1.0),
        G(valmiki("namaste", eye="happy"), x=380, y=470, s=1.32),
        G(disciple("namaste", eye="wonder"), x=490, y=468, s=0.95),
        grass_tufts([(80, 470), (330, 492), (640, 470), (720, 488)]),
        defs=sky_defs("day"),
        title="நாரதர் விடைபெறுகிறார்")


def scene2():
    return svg(
        sky(), sun(110, 110, 30), cloud(320, 80, 0.9), cloud(650, 110, 1.1),
        hills(270), tree(40, 290, 0.9, 1), tree(760, 296, 1.0, 0), tree(690, 286, 0.7, 2),
        river(286, 398), bank(398),
        grass_tufts([(40, 460), (600, 488), (760, 452)]),
        G(valmiki("point", eye="open", mouth_kind="open"), x=300, y=474, s=1.38),
        G(kalasha(full=True), x=560, y=478, s=1.0),
        G(disciple("give", holding_cloth=True, eye="happy"), x=470, y=474, s=1.15, flip=True),
        defs=sky_defs("dawn"),
        title="தமஸா நதிக்கரையில் வால்மீகியும் பரத்வாஜரும்")


def scene3():
    return svg(
        sky(), cloud(160, 90, 0.9), cloud(560, 70, 1.0),
        hills(276), tree(36, 300, 0.95, 0), tree(300, 292, 0.75, 2),
        river(290, 392), bank(392),
        G(valmiki("down", eye="sad"), x=110, y=466, s=1.0),
        G(hunter(), x=700, y=468, s=1.12, flip=True),
        bush(710, 476, 1.35, LEAF_D), bush(620, 486, 0.9, "#4f9a5f"),
        G(crane("fallen"), x=430, y=460, s=1.25),
        G(crane("cry"), x=330, y=452, s=1.2),
        leaf_feather(560, 380, 30), leaf_feather(600, 342, -20), leaf_feather(520, 330, 60),
        grass_tufts([(200, 486), (540, 492), (60, 488)]),
        defs=sky_defs("day"),
        title="இணைபிரியாத க்ரௌஞ்சப் பறவைகளும் வேடனும்")


def scene4():
    return svg(
        sky(), cloud(110, 70, 0.8), cloud(700, 90, 0.9),
        hills(286), tree(770, 300, 0.95, 1),
        river(298, 396), bank(396),
        G(verse_dots(), x=520, y=176, s=1.35),
        sparkle(400, 120, 1.0), sparkle(650, 110, 0.8), sparkle(690, 240, 0.7),
        G(disciple("namaste", eye="wonder", mouth_kind="open"), x=120, y=470, s=1.02),
        G(valmiki("speak", eye="sad", mouth_kind="open"), x=300, y=472, s=1.42),
        G(crane("fallen"), x=600, y=470, s=0.95),
        G(crane("cry"), x=540, y=462, s=1.0),
        defs=sky_defs("dawn"),
        title="சோகம் ஸ்லோகமாகிறது")


def scene5():
    path = P("M120,500 C240,450 380,430 520,410 C600,398 660,392 700,388 L720,396 "
             "C660,404 600,414 540,428 C400,452 300,476 260,500 Z", "#e6cf9a", stroke="none")
    return svg(
        sky(), sun(680, 120, 30), cloud(200, 90, 1.0), cloud(470, 120, 0.7),
        hills(300), tree(60, 384, 1.05, 2), tree(330, 380, 0.85, 0),
        ground(380), path, hut(650, 388, 0.95),
        G(disciple("pot", pot=True, eye="open"), x=250, y=474, s=1.1),
        G(valmiki("think", eye="closed", walking=True), x=430, y=470, s=1.32),
        grass_tufts([(60, 470), (560, 476), (760, 470)]),
        defs=sky_defs("day"),
        title="சிந்தனையுடன் ஆசிரமம் திரும்புதல்")


def scene6():
    return svg(
        sky(), rays(570, 250, n=16, r1=50, r2=420), hills(320, "#e7d9a8", "#d9c98e"),
        ground(384, "#c9dc93"), hut(140, 388, 0.95), tree(760, 386, 0.9, 1),
        sparkle(460, 120, 1.2), sparkle(700, 160, 1.0), sparkle(640, 90, 0.8), sparkle(470, 300, 0.7),
        G(brahma("abhaya"), x=580, y=466, s=1.32),
        G(disciple("namaste", eye="wonder", mouth_kind="open"), x=180, y=470, s=0.95),
        G(valmiki("namaste", eye="wonder"), x=340, y=472, s=1.32),
        defs=sky_defs("divine"),
        title="நான்முகன் பிரம்மாவின் வருகை")


def scene7():
    return svg(
        sky(), rays(590, 300, n=12, r1=40, r2=300, opacity=0.35), hills(320, "#e7d9a8", "#d9c98e"),
        ground(384, "#c9dc93"), tree(60, 384, 1.0, 0),
        thought_bubble(400, 128, 230, 132, tail="right"),
        mountain_icon(350, 150, 0.95), river_icon(450, 158, 0.9),
        G(verse_dots(4, 8, 7, 2.2, glow=False), x=400, y=92, s=1.0),
        G(honoured_seat(110), x=590, y=440, s=1.0),
        G(brahma("abhaya", sitting=True), x=590, y=436, s=1.22),
        G(seat(110), x=250, y=452, s=1.0),
        G(valmiki("namaste", sitting=True, eye="closed"), x=250, y=450, s=1.28),
        defs=sky_defs("divine"),
        title="ராமனின் கதையை இயற்றும்படி பிரம்மா ஆணையிடுதல்")


def scene8():
    return svg(
        sky(), sun(400, 90, 28), hills(310), tree(40, 384, 1.0, 1), tree(770, 384, 1.0, 0),
        ground(384), hut(660, 388, 0.75),
        G(verse_dots(), x=400, y=182, s=1.05),
        G(verse_dots(), x=230, y=150, s=0.62), G(verse_dots(), x=575, y=140, s=0.66),
        G(verse_dots(), x=150, y=70, s=0.42), G(verse_dots(), x=660, y=62, s=0.45),
        note(150, 300, 1.2), note(610, 280, 1.1, "#b8573a"), note(700, 330, 0.9),
        G(seat(110), x=400, y=462),
        G(valmiki("lap", sitting=True, eye="closed"), x=400, y=460, s=1.32),
        G(disciple("namaste", sitting=True, eye="happy", mouth_kind="open"), x=200, y=470, s=1.0),
        G(disciple("namaste", sitting=True, eye="happy", mouth_kind="open"), x=600, y=470, s=1.0, flip=True),
        defs=sky_defs("dawn"),
        title="ராமாயணம் பிறக்கிறது")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pics = {"chapter": chapter, "scene-1": scene1, "scene-2": scene2, "scene-3": scene3,
            "scene-4": scene4, "scene-5": scene5, "scene-6": scene6, "scene-7": scene7, "scene-8": scene8}
    for name, fn in pics.items():
        (OUT_DIR / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print("wrote", len(pics), "pictures to", OUT_DIR)


if __name__ == "__main__":
    main()
