"""Tiny SVG drawing kit for the Valmiki Ramayanam site.

Flat, friendly cartoon style. Every character is drawn in its own coordinate
system with the feet at (0, 0) and "up" being negative y, so a scene places a
character with G(character(...), x=..., y=..., s=...). Reusing these same
functions in every chapter keeps the characters looking the same everywhere.
"""

W, H = 800, 500
OUT = "#3b2a1f"          # outline colour

# ---- palette -------------------------------------------------------------
SKIN_SAGE = "#c98b5a"
SKIN_YOUNG = "#dba574"
SKIN_FAIR = "#e9b88a"
SKIN_HUNTER = "#8a5634"
SKIN_BRAHMA = "#f1bf63"
WHITE_HAIR = "#f6f3ec"
BLACK_HAIR = "#2e2420"
BARK, BARK_D, BARK_L = "#a9733f", "#86572c", "#c38d55"
OCHRE, OCHRE_D = "#e7a13d", "#c9822a"
WHITE_CLOTH, WHITE_CLOTH_D = "#f7f3ea", "#d9d2c3"
RED_ROBE, RED_ROBE_D = "#c9473d", "#a3362e"
GOLD, GOLD_D = "#f2c14e", "#d39a2a"
YELLOW_ROBE = "#efb84a"
CRANE, CRANE_D, CRANE_DD, CRANE_RED = "#c3ccd4", "#9eabb6", "#7f8c98", "#d6504a"
COPPER, COPPER_L = "#c8733a", "#eeb07a"
LEAF, LEAF_D, LEAF_L = "#5aa060", "#3f8049", "#7cbc6e"
TRUNK = "#7a5230"
WATER, WATER_D, WATER_L = "#86cde3", "#5cb0cf", "#dff4fa"
SAND = "#ecd9a5"
GRASS, GRASS_D = "#a9d68b", "#86bd6a"
BLUSH = "#e8846c"


# ---- primitives ------------------------------------------------------------
def _a(**kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        out.append(f'{k.rstrip("_").replace("_", "-")}="{v}"')
    return " ".join(out)


def P(d, fill="none", stroke=OUT, sw=2.5, **kw):
    return f'<path d="{d}" {_a(fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin="round", stroke_linecap="round", **kw)}/>'


def C(cx, cy, r, fill, stroke=OUT, sw=2.5, **kw):
    return f'<circle {_a(cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=sw, **kw)}/>'


def E(cx, cy, rx, ry, fill, stroke=OUT, sw=2.5, **kw):
    return f'<ellipse {_a(cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=sw, **kw)}/>'


def R(x, y, w, h, fill, stroke="none", sw=0, rx=0, **kw):
    return f'<rect {_a(x=x, y=y, width=w, height=h, rx=rx, fill=fill, stroke=stroke, stroke_width=sw, **kw)}/>'


def G(*items, x=0, y=0, s=1.0, flip=False, rot=0, opacity=None):
    sx = -s if flip else s
    t = f"translate({x:g},{y:g})"
    if rot:
        t += f" rotate({rot:g})"
    t += f" scale({sx:g},{s:g})"
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<g transform="{t}"{op}>' + "".join(items) + "</g>"


def limb(d, color, w=8):
    """An outlined 'tube' (arm, neck, leg) following path d."""
    return (P(d, stroke=OUT, sw=w + 4.5) + P(d, stroke=color, sw=w))


def svg(*items, defs="", title=""):
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img">{t}<defs>{defs}</defs>'
            + "".join(items) + "</svg>")


# ---- faces -----------------------------------------------------------------
def eyes(cx, cy, r, kind="open"):
    lx, rx_, ey = cx - r * 0.38, cx + r * 0.38, cy + r * 0.02
    if kind == "closed":       # serene, eyes closed
        return (P(f"M{lx-4},{ey} Q{lx},{ey+3.5} {lx+4},{ey}", sw=2) +
                P(f"M{rx_-4},{ey} Q{rx_},{ey+3.5} {rx_+4},{ey}", sw=2))
    if kind == "happy":        # smiling eyes
        return (P(f"M{lx-4},{ey+1.5} Q{lx},{ey-3} {lx+4},{ey+1.5}", sw=2) +
                P(f"M{rx_-4},{ey+1.5} Q{rx_},{ey-3} {rx_+4},{ey+1.5}", sw=2))
    out = ""
    for x in (lx, rx_):
        out += E(x, ey, 2.7, 3.5, "#2a1c14", stroke="none")
        out += C(x + 0.9, ey - 1.3, 0.95, "#ffffff", stroke="none")
    if kind == "sad":
        out += P(f"M{lx-4.5},{ey-5} L{lx+3},{ey-7.5}", sw=1.8)
        out += P(f"M{rx_+4.5},{ey-5} L{rx_-3},{ey-7.5}", sw=1.8)
    if kind == "wonder":
        out += P(f"M{lx-4},{ey-7} Q{lx},{ey-10} {lx+4},{ey-7}", sw=1.8)
        out += P(f"M{rx_-4},{ey-7} Q{rx_},{ey-10} {rx_+4},{ey-7}", sw=1.8)
    if kind == "stern":
        out += P(f"M{lx-4.5},{ey-7.5} L{lx+3.5},{ey-5}", sw=2.2)
        out += P(f"M{rx_+4.5},{ey-7.5} L{rx_-3.5},{ey-5}", sw=2.2)
    return out


def blush(cx, cy, r):
    return (C(cx - r * 0.58, cy + r * 0.32, r * 0.17, BLUSH, stroke="none", opacity=0.35) +
            C(cx + r * 0.58, cy + r * 0.32, r * 0.17, BLUSH, stroke="none", opacity=0.35))


def mouth(cx, cy, kind="smile"):
    if kind == "open":
        return E(cx, cy, 3.4, 3, "#7a2e2a", sw=1.4)
    if kind == "sad":
        return P(f"M{cx-4},{cy+1.5} Q{cx},{cy-2} {cx+4},{cy+1.5}", sw=1.8)
    if kind == "flat":
        return P(f"M{cx-3.5},{cy} L{cx+3.5},{cy}", sw=1.8)
    return P(f"M{cx-4.5},{cy-1} Q{cx},{cy+3.5} {cx+4.5},{cy-1}", sw=1.8)


# ---- props -----------------------------------------------------------------
def kalasha(full=False):
    """Copper water pot, base at (0,0), about 40 high."""
    out = [E(0, -16, 16, 15, COPPER),
           P("M-7,-30 L-6,-36 L6,-36 L7,-30 Z", COPPER, sw=2),
           E(0, -37, 9.5, 3.4, "#d98a4a", sw=2),
           P("M-10,-21 Q-11,-27 -5,-29", stroke=COPPER_L, sw=2.6)]
    if full:
        out.append(E(0, -37.5, 7, 2, WATER, stroke="none"))
    return "".join(out)


def bark_cloth():
    """Folded bark garment held in a hand, centred at (0,0)."""
    return (P("M-14,-8 L14,-10 L16,8 L-12,10 Z", BARK, sw=2) +
            P("M-12,-3 L14,-4 M-11,3 L15,2", stroke=BARK_D, sw=1.4))


def seat(w=70, color="#7c9a4a"):
    """Kusha-grass mat / honoured seat, top edge at y=0."""
    return (R(-w / 2, -2, w, 10, color, stroke=OUT, sw=2, rx=4) +
            P(f"M{-w/2+6},3 L{w/2-6},3", stroke="#5f7a34", sw=1.4))


def honoured_seat(w=86):
    return (R(-w / 2, -6, w, 16, "#b5452f", stroke=OUT, sw=2.2, rx=5) +
            P(f"M{-w/2+5},2 L{w/2-5},2", stroke=GOLD, sw=2.4) +
            R(-w / 2 + 6, 10, 8, 14, "#8a5a2b", stroke=OUT, sw=2) +
            R(w / 2 - 14, 10, 8, 14, "#8a5a2b", stroke=OUT, sw=2))


def bow(h=120):
    return (P(f"M0,{-h/2} Q-22,0 0,{h/2}", stroke="#6b4421", sw=4.5) +
            P(f"M0,{-h/2} L0,{h/2}", stroke="#e9e0c8", sw=1.2))


def sparkle(x, y, s=1.0, color=GOLD):
    return G(P("M0,-9 L2,-2 L9,0 L2,2 L0,9 L-2,2 L-9,0 L-2,-2 Z", color, stroke="none"), x=x, y=y, s=s)


def note(x, y, s=1.0, color="#7a4fa3"):
    return G(E(0, 0, 5, 3.8, color, stroke="none", transform="rotate(-20)") +
             P("M4.5,-1 L4.5,-18 Q10,-15 12,-10", stroke=color, sw=2.2), x=x, y=y, s=s)


def verse_dots(rows=4, cols=8, gap=13, r=3.6, glow=True):
    """The Anushtubh shloka: 4 padas x 8 syllables, shown as golden dots."""
    w, h = (cols - 1) * gap, (rows - 1) * gap * 1.2
    out = []
    if glow:
        out.append(E(w / 2, h / 2, w / 2 + 30, h / 2 + 22, "#fff4cf", stroke="none", opacity=0.85))
        out.append(E(w / 2, h / 2, w / 2 + 30, h / 2 + 22, "none", stroke=GOLD, sw=2, opacity=0.8))
    for i in range(rows):
        for j in range(cols):
            out.append(C(j * gap, i * gap * 1.2, r, GOLD, stroke=GOLD_D, sw=1.2))
    return G(*out, x=-w / 2, y=-h / 2)


def cry_lines(color="#5a7f9a"):
    return (P("M0,0 L8,-6", stroke=color, sw=2) + P("M2,8 L12,6", stroke=color, sw=2) +
            P("M-2,-8 L4,-16", stroke=color, sw=2))


# ---- characters ------------------------------------------------------------
def _arms(pose, skin, sx=19, sy=-108, w=7.5):
    """Arm shapes for a standing adult (shoulders at (+-sx, sy))."""
    L, Rt = [], []
    hand = lambda x, y, r=4.8: C(x, y, r, skin, sw=2.2)
    if pose == "namaste":
        L += [limb(f"M{-sx},{sy} C{-sx-7},{sy+12} {-14},{sy+19} {-4},{sy+12}", skin, w)]
        Rt += [limb(f"M{sx},{sy} C{sx+7},{sy+12} {14},{sy+19} {4},{sy+12}", skin, w)]
        Rt += [P(f"M0,{sy+1} C5,{sy+7} 5,{sy+16} 0,{sy+19} C-5,{sy+16} -5,{sy+7} 0,{sy+1} Z", skin, sw=2.2)]
    elif pose == "lap":
        L += [limb(f"M{-sx},{sy} C{-sx-6},{sy+18} {-sx},{sy+32} {-8},{sy+34}", skin, w), hand(-7, sy + 34)]
        Rt += [limb(f"M{sx},{sy} C{sx+6},{sy+18} {sx},{sy+32} {8},{sy+34}", skin, w), hand(7, sy + 34)]
    else:
        # left arm (viewer's left) hangs down unless the pose says otherwise
        L += [limb(f"M{-sx},{sy} C{-sx-8},{sy+12} {-sx-10},{sy+26} {-sx-8},{sy+36}", skin, w),
              hand(-sx - 8, sy + 37)]
        if pose == "down" or pose == "walk":
            Rt += [limb(f"M{sx},{sy} C{sx+8},{sy+12} {sx+10},{sy+26} {sx+8},{sy+36}", skin, w),
                   hand(sx + 8, sy + 37)]
        elif pose == "speak":       # hand raised, open palm
            Rt += [limb(f"M{sx},{sy} C{sx+12},{sy-2} {sx+16},{sy-12} {sx+19},{sy-24}", skin, w),
                   E(sx + 20, sy - 29, 5.2, 7, skin, sw=2.2)]
        elif pose == "bless":       # abhaya: palm up near shoulder
            Rt += [limb(f"M{sx},{sy} C{sx+10},{sy+4} {sx+12},{sy-6} {sx+12},{sy-16}", skin, w),
                   E(sx + 12, sy - 21, 5.2, 7, skin, sw=2.2)]
        elif pose == "abhaya":      # blessing palm in front, below the face
            Rt += [limb(f"M{sx},{sy} C{sx+12},{sy+16} {sx+18},{sy+10} {sx+18},{sy}", skin, w),
                   E(sx + 18, sy - 6, 5.4, 7.2, skin, sw=2.2)]
        elif pose == "give":        # arm stretched forward
            Rt += [limb(f"M{sx},{sy} C{sx+10},{sy+8} {sx+20},{sy+10} {sx+30},{sy+8}", skin, w),
                   hand(sx + 32, sy + 8)]
        elif pose == "point":       # pointing forward and down
            Rt += [limb(f"M{sx},{sy} C{sx+12},{sy+2} {sx+24},{sy+8} {sx+34},{sy+16}", skin, w),
                   hand(sx + 36, sy + 17, 4.4)]
        elif pose == "think":       # hand to chin
            Rt += [limb(f"M{sx},{sy} C{sx+10},{sy+12} {sx-2},{sy+10} {sx-11},{sy+3}", skin, w),
                   hand(sx - 12, sy + 2)]
        elif pose == "pot":         # carrying pot at the hip
            Rt += [limb(f"M{sx},{sy} C{sx+8},{sy+12} {sx+12},{sy+28} {sx+14},{sy+38}", skin, w)]
        else:
            Rt += [limb(f"M{sx},{sy} C{sx+8},{sy+12} {sx+10},{sy+26} {sx+8},{sy+36}", skin, w),
                   hand(sx + 8, sy + 37)]
    return "".join(L), "".join(Rt)


def valmiki(pose="down", sitting=False, eye="open", mouth_kind="calm", walking=False):
    """Sage Valmiki: elderly, white beard and jata, bark (valkala) garments."""
    skin = SKIN_SAGE
    parts = []
    if sitting:
        parts += [P("M-44,-3 C-47,-24 -27,-38 0,-38 C27,-38 47,-24 44,-3 Z", BARK),
                  P("M-36,-12 Q-18,-20 0,-14 Q18,-20 36,-12", stroke=BARK_D, sw=1.8),
                  E(-22, -6, 9, 4.5, skin, sw=2), E(22, -6, 9, 4.5, skin, sw=2)]
        dy = 36
    else:
        if walking:
            parts += [E(-15, -3, 9, 4, skin, sw=2), E(15, -2, 9, 4, skin, sw=2)]
            robe = "M-23,-72 C-28,-50 -33,-26 -32,-7 L31,-7 C33,-26 28,-50 23,-72 Z"
        else:
            parts += [E(-10, -3, 9, 4, skin, sw=2), E(10, -3, 9, 4, skin, sw=2)]
            robe = "M-23,-72 C-27,-50 -31,-26 -29,-7 L29,-7 C31,-26 27,-50 23,-72 Z"
        parts += [P(robe, BARK),
                  P("M-26,-52 Q-19,-55 -13,-52 T0,-52 T13,-52 T26,-52", stroke=BARK_D, sw=1.6),
                  P("M-28,-32 Q-21,-35 -14,-32 T0,-32 T14,-32 T28,-32", stroke=BARK_D, sw=1.6)]
        dy = 0
    up = []
    up.append(P("M-20,-113 C-25,-100 -25,-84 -23,-72 L23,-72 C25,-84 25,-100 20,-113 Z", skin))
    up.append(P("M-20,-113 L-8,-113 L23,-81 L23,-72 L12,-72 Z", BARK_L, sw=2.2))
    up.append(P("M-23,-74 L23,-74", stroke=BARK_D, sw=3.5))
    la, ra = _arms(pose, skin)
    up.append(la)
    # head
    up += [E(-19, -128, 4, 6, skin, sw=2), E(19, -128, 4, 6, skin, sw=2),
           C(0, -128, 19, skin),
           P("M-19,-131 C-21,-151 21,-151 19,-131 C13,-141 -13,-141 -19,-131 Z", WHITE_HAIR, sw=2.2),
           E(0, -153, 10, 11, WHITE_HAIR, sw=2.2),
           P("M-9,-146 Q0,-143 9,-146", stroke=BARK_D, sw=3),
           P("M-12,-135 Q-8,-138 -3,-136", stroke=WHITE_HAIR, sw=3.2),
           P("M12,-135 Q8,-138 3,-136", stroke=WHITE_HAIR, sw=3.2),
           eyes(0, -128, 19, eye),
           P("M0,-126 Q2.5,-121 -1,-119", sw=1.6),
           C(-11, -121, 3.2, BLUSH, stroke="none", opacity=0.3),
           C(11, -121, 3.2, BLUSH, stroke="none", opacity=0.3),
           P("M-18,-125 C-19,-107 -11,-93 0,-88 C11,-93 19,-107 18,-125 C12,-117 -12,-117 -18,-125 Z",
             WHITE_HAIR, sw=2.2),
           P("M-9,-116 Q-4,-120 0,-117 Q4,-120 9,-116 Q4,-113 0,-115 Q-4,-113 -9,-116 Z", WHITE_HAIR, sw=1.6)]
    if mouth_kind == "open":
        up.append(E(0, -110, 3.2, 2.8, "#7a2e2a", sw=1.3))
    up.append(ra)
    parts.append(G(*up, y=dy))
    return "".join(parts)


def disciple(pose="down", sitting=False, eye="open", mouth_kind="smile", cloth=OCHRE, cloth_d=OCHRE_D,
             skin=SKIN_YOUNG, pot=False, holding_cloth=False):
    """A young brahmachari disciple (Bharadvaja and the others)."""
    parts = []
    if sitting:
        parts += [P("M-38,-3 C-40,-22 -23,-34 0,-34 C23,-34 40,-22 38,-3 Z", cloth),
                  P("M-30,-11 Q-15,-18 0,-12 Q15,-18 30,-11", stroke=cloth_d, sw=1.8),
                  E(-19, -5, 8, 4, skin, sw=2), E(19, -5, 8, 4, skin, sw=2)]
        dy = 32
    else:
        parts += [E(-9, -3, 8, 3.8, skin, sw=2), E(9, -3, 8, 3.8, skin, sw=2),
                  P("M-21,-66 C-24,-46 -25,-26 -22,-8 L22,-8 C25,-26 24,-46 21,-66 Z", cloth),
                  P("M-3,-62 L-5,-12 M8,-60 L9,-14", stroke=cloth_d, sw=1.6)]
        dy = 0
    up = [P("M-18,-104 C-22,-92 -22,-78 -21,-66 L21,-66 C22,-78 22,-92 18,-104 Z", skin),
          P("M-21,-68 L21,-68", stroke=cloth_d, sw=3.2),
          P("M-13,-103 C-3,-91 9,-79 18,-69", stroke="#fff7e2", sw=2)]
    la, ra = _arms(pose, skin, sx=17, sy=-99, w=7)
    up.append(la)
    up += [E(-17, -120, 3.6, 5.4, skin, sw=2), E(17, -120, 3.6, 5.4, skin, sw=2),
           C(0, -120, 17, skin),
           P("M-17,-122 C-18,-140 18,-140 17,-122 C12,-131 -12,-131 -17,-122 Z", BLACK_HAIR, sw=2),
           C(0, -139, 6.5, BLACK_HAIR, sw=2),
           eyes(0, -120, 17, eye),
           P("M0,-118 Q2,-114 -0.8,-112.5", sw=1.5),
           blush(0, -120, 17),
           mouth(0, -110, mouth_kind)]
    if pot:
        up.append(G(kalasha(full=True), x=36, y=-52, s=0.82))
    up.append(ra)
    if holding_cloth:
        up.append(G(bark_cloth(), x=50, y=-92, s=0.9))
    parts.append(G(*up, y=dy))
    return "".join(parts)


def narada(pose="bless"):
    """Devarishi Narada, travelling through the sky."""
    return disciple(pose=pose, cloth=WHITE_CLOTH, cloth_d=WHITE_CLOTH_D, skin=SKIN_FAIR,
                    eye="happy", mouth_kind="smile")


def brahma(pose="bless", sitting=False, eye="happy", mouth_kind="smile"):
    """Four-faced Brahma (three faces visible), golden, radiant."""
    skin = SKIN_BRAHMA
    parts = []
    if sitting:
        parts += [P("M-48,-3 C-51,-26 -29,-42 0,-42 C29,-42 51,-26 48,-3 Z", YELLOW_ROBE),
                  P("M-48,-6 C-30,-12 30,-12 48,-6", stroke=RED_ROBE, sw=3.5),
                  E(-24, -6, 9, 4.5, skin, sw=2), E(24, -6, 9, 4.5, skin, sw=2)]
        dy = 40
    else:
        parts += [E(-11, -3, 9, 4, skin, sw=2), E(11, -3, 9, 4, skin, sw=2),
                  P("M-27,-66 C-31,-44 -34,-24 -32,-7 L32,-7 C34,-24 31,-44 27,-66 Z", YELLOW_ROBE),
                  P("M-32,-12 L32,-12", stroke=RED_ROBE, sw=4)]
        dy = 0
    up = []
    up.append(C(0, -140, 60, "#fff4c9", stroke="none", opacity=0.9))
    up.append(C(0, -140, 60, "none", stroke=GOLD, sw=3))

    def side_face(x, flip):
        f = [C(0, 0, 15, skin),
             P("M-8,-12 L-7,-30 L-1,-24 L4,-34 L8,-24 L12,-30 L13,-11 Z", GOLD, sw=2),
             C(3, -21, 2.2, "#d23b3b", stroke="none"),
             P("M-3,4 C-2,16 6,22 12,20 C14,12 13,6 12,2 Z", WHITE_HAIR, sw=1.8),
             P("M6,-2 Q9,-4 11,-1", sw=1.8),
             P("M12,-3 L16,0 L12,2", sw=1.6, fill=skin)]
        return G(*f, x=x, y=-126, s=0.92, flip=flip)
    up += [side_face(-27, True), side_face(27, False)]
    up.append(P("M-25,-113 C-31,-94 -31,-76 -27,-64 L27,-64 C31,-76 31,-94 25,-113 Z", RED_ROBE))
    up.append(P("M-15,-111 Q0,-98 15,-111", stroke=GOLD, sw=4))
    up.append(P("M-27,-66 L27,-66", stroke=GOLD, sw=4))
    la, ra = _arms(pose, skin, sx=23, sy=-107, w=8)
    up.append(la)
    up += [C(0, -130, 19, skin),
           P("M-17,-141 L-15,-168 L-7,-158 L0,-176 L7,-158 L15,-168 L17,-141 Z", GOLD, sw=2.2),
           P("M-17,-141 L17,-141", stroke=GOLD_D, sw=3),
           C(0, -156, 3.2, "#d23b3b", stroke="none"),
           eyes(0, -130, 19, eye),
           P("M0,-128 Q2.5,-123 -1,-121", sw=1.6),
           P("M-15,-124 C-15,-109 -8,-99 0,-97 C8,-99 15,-109 15,-124 C10,-118 -10,-118 -15,-124 Z",
             WHITE_HAIR, sw=2.2),
           P("M-8,-119 Q-4,-122 0,-120 Q4,-122 8,-119 Q4,-116 0,-118 Q-4,-116 -8,-119 Z", WHITE_HAIR, sw=1.5),
           mouth(0, -113, mouth_kind) if mouth_kind != "smile" else P("M-3.5,-114 Q0,-111.5 3.5,-114", sw=1.6),
           C(-0, -140, 1.8, "#d23b3b", stroke="none")]
    up.append(ra)
    parts.append(G(*up, y=dy))
    return "".join(parts)


def hunter(pose="bow"):
    """The nishada hunter, holding a bow (drawn half hidden in scenes)."""
    skin = SKIN_HUNTER
    parts = [E(-9, -3, 8, 3.8, skin, sw=2), E(9, -3, 8, 3.8, skin, sw=2),
             limb("M-8,-60 L-10,-6", skin, 8), limb("M8,-60 L10,-6", skin, 8),
             P("M-20,-70 L20,-70 L18,-50 L-18,-50 Z", "#5f6b3a"),
             P("M-18,-108 C-22,-94 -22,-80 -20,-68 L20,-68 C22,-80 22,-94 18,-108 Z", skin),
             P("M-16,-106 L20,-74", stroke="#6b4421", sw=3)]
    la, ra = _arms("give", skin, sx=17, sy=-102, w=7.5)
    parts += [la,
              E(-16, -124, 3.6, 5.4, skin, sw=2), E(16, -124, 3.6, 5.4, skin, sw=2),
              C(0, -124, 17, skin),
              P("M-17,-126 C-18,-144 18,-144 17,-126 C10,-134 -10,-134 -17,-126 Z", "#1f1714", sw=2),
              P("M-17,-131 L17,-131", stroke="#a33a2a", sw=3),
              eyes(0, -124, 17, "stern"),
              P("M0,-122 Q2,-118 -1,-116.5", sw=1.5),
              mouth(0, -114, "flat"),
              ra,
              G(bow(118), x=52, y=-94)]
    return "".join(parts)


def crane(pose="stand"):
    """Krauncha bird (sarus crane): grey, copper-red head ('tamra-shirsha'), long legs.
    Faces right. Feet at (0,0)."""
    out = []
    if pose == "fallen":
        out += [P("M-30,-14 C-20,-34 18,-34 28,-18 C30,-10 20,-4 4,-4 C-14,-4 -28,-6 -30,-14 Z", CRANE),
                P("M-22,-16 C-10,-30 10,-28 18,-18 C6,-12 -10,-10 -22,-16 Z", CRANE_D),
                P("M-30,-14 C-40,-12 -44,-6 -40,-2 C-34,-6 -30,-8 -26,-8 Z", CRANE_DD),
                limb("M26,-14 C40,-12 50,-8 60,-6", CRANE, 6),
                E(66, -6, 7, 5.5, CRANE_RED, sw=2),
                P("M60,-9 q6,-5 12,0", stroke=CRANE, sw=2.6),
                P("M64,-6.5 q2,1.6 4,0", sw=1.4),
                P("M72,-5 L88,-2 L72,-2 Z", "#6b5a46", sw=1.4),
                P("M-8,-6 L-26,4 M-26,4 l-5,-2 M-26,4 l-3,4", stroke="#b5655a", sw=2.4),
                P("M2,-5 L-12,8 M-12,8 l-5,-1 M-12,8 l-2,5", stroke="#b5655a", sw=2.4),
                E(2, -12, 6, 3.4, "#b9473f", stroke="none", opacity=0.8)]
        return "".join(out)
    if pose == "fly":
        out += [P("M-6,-56 C-26,-96 -52,-110 -70,-112 C-56,-96 -42,-78 -22,-62 Z", CRANE_D),
                limb("M-26,-50 L-62,-40", "#b5655a", 2.2),
                P("M-34,-52 C-26,-66 6,-70 22,-60 C30,-54 26,-44 10,-40 C-8,-37 -28,-40 -34,-52 Z", CRANE),
                P("M-34,-52 C-44,-50 -48,-44 -44,-38 C-38,-44 -34,-46 -30,-46 Z", CRANE_DD),
                limb("M18,-58 C30,-62 40,-66 50,-68", CRANE, 6.5),
                E(56, -69, 7, 6, CRANE_RED, sw=2),
                P("M50,-72 q6,-6 12,0", stroke=CRANE, sw=2.6),
                C(58, -70, 1.4, "#222", stroke="none"),
                P("M62,-70 L80,-66 L62,-66 Z", "#6b5a46", sw=1.4),
                P("M4,-60 C-6,-96 -26,-116 -42,-122 C-36,-104 -24,-80 -10,-62 Z", CRANE_D)]
        return "".join(out)
    # standing / walking / crying share the body
    legs = ("M-4,-46 L-6,0 M-6,0 l-6,1 M-6,0 l5,2", "M8,-46 L11,0 M11,0 l-5,1 M11,0 l6,2")
    if pose == "walk":
        legs = ("M-4,-46 L-14,-2 M-14,-2 l-6,1 M-14,-2 l5,2", "M8,-46 L14,0 M14,0 l-5,1 M14,0 l6,2")
    out += [P(legs[0], stroke="#b5655a", sw=2.6), P(legs[1], stroke="#b5655a", sw=2.6),
            P("M-34,-60 C-30,-78 0,-84 18,-74 C28,-68 26,-52 10,-46 C-6,-42 -26,-44 -34,-60 Z", CRANE),
            P("M-26,-62 C-14,-76 6,-74 14,-64 C4,-56 -14,-52 -26,-62 Z", CRANE_D),
            P("M-34,-60 C-46,-58 -50,-50 -46,-44 C-40,-50 -34,-52 -30,-52 Z", CRANE_DD)]
    if pose == "cry":
        out += [limb("M14,-72 C24,-90 14,-108 18,-126", CRANE, 7),
                E(19, -131, 7.5, 6.5, CRANE_RED, sw=2),
                P("M13,-134 q6,-6 12,0", stroke=CRANE, sw=2.6),
                C(21, -133, 1.5, "#222", stroke="none"),
                P("M24,-134 L36,-152 L27,-131 Z", "#6b5a46", sw=1.4),
                P("M25,-129 L42,-140 L26,-127 Z", "#6b5a46", sw=1.4),
                G(cry_lines(), x=46, y=-150)]
    else:
        out += [limb("M14,-72 C26,-86 18,-104 26,-116", CRANE, 7),
                E(28, -120, 7.5, 6.5, CRANE_RED, sw=2),
                P("M22,-124 q6,-6 12,0", stroke=CRANE, sw=2.6),
                C(30, -122, 1.5, "#222", stroke="none"),
                P("M34,-122 L54,-117 L34,-117.5 Z", "#6b5a46", sw=1.4)]
    return "".join(out)


# ---- scenery ---------------------------------------------------------------
def sky_defs(kind="dawn"):
    stops = {
        "dawn": ("#ffe3bf", "#fdf0d5", "#cfeaf3"),
        "day": ("#bfe6f6", "#dff3fa", "#f4fbfd"),
        "divine": ("#fff1c9", "#ffe8b0", "#fbd9a0"),
        "evening": ("#f7c9a1", "#fbe0c4", "#e3eef3"),
    }[kind]
    return (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{stops[0]}"/><stop offset="0.55" stop-color="{stops[1]}"/>'
            f'<stop offset="1" stop-color="{stops[2]}"/></linearGradient>'
            f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{WATER}"/><stop offset="1" stop-color="{WATER_D}"/></linearGradient>'
            f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="#fffbe6" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>')


def sky():
    return R(0, 0, W, H, "url(#sky)")


def sun(x, y, r=34):
    return C(x, y, r * 1.8, "#fff6d8", stroke="none", opacity=0.6) + C(x, y, r, "#fff0b3", stroke="none")


def cloud(x, y, s=1.0, opacity=0.9):
    c = (E(0, 0, 38, 14, "#ffffff", stroke="none") + C(-14, -8, 14, "#ffffff", stroke="none") +
         C(8, -12, 18, "#ffffff", stroke="none") + C(26, -4, 11, "#ffffff", stroke="none"))
    return G(c, x=x, y=y, s=s, opacity=opacity)


def hills(y=300, c1="#b7d9b0", c2="#9cc99a"):
    return (P(f"M0,{y} C120,{y-70} 220,{y-60} 330,{y-20} C430,{y-70} 560,{y-80} 680,{y-30} "
              f"C730,{y-50} 770,{y-40} 800,{y-30} L800,{y+60} L0,{y+60} Z", c1, stroke="none") +
            P(f"M0,{y+20} C150,{y-30} 260,{y-10} 400,{y+10} C520,{y-30} 650,{y-20} 800,{y+5} "
              f"L800,{y+80} L0,{y+80} Z", c2, stroke="none"))


def tree(x, y, s=1.0, shade=0):
    greens = [(LEAF, LEAF_D, LEAF_L), ("#4f9a5f", "#3a7a48", "#6db06a"), ("#68ad62", "#4b8e4d", "#8cc77a")][shade % 3]
    t = [P("M-7,0 L-5,-60 L5,-60 L7,0 Z", TRUNK, sw=2.2),
         P("M-4,-40 L-18,-58 M3,-46 L16,-62", stroke=TRUNK, sw=4),
         C(-26, -70, 26, greens[1], sw=2.2), C(24, -72, 26, greens[1], sw=2.2),
         C(0, -98, 34, greens[0], sw=2.2), C(-22, -84, 20, greens[0], stroke="none"),
         C(20, -84, 20, greens[0], stroke="none"),
         C(-10, -110, 10, greens[2], stroke="none", opacity=0.8), C(12, -96, 7, greens[2], stroke="none", opacity=0.7)]
    return G(*t, x=x, y=y, s=s)


def bush(x, y, s=1.0, color=LEAF_D):
    b = (C(-22, -12, 18, color, sw=2.2) + C(0, -22, 22, color, sw=2.2) + C(24, -12, 17, color, sw=2.2) +
         R(-40, -12, 82, 12, color) + P("M-40,0 L42,0", stroke=OUT, sw=2.2) +
         C(-6, -28, 6, LEAF_L, stroke="none", opacity=0.7))
    return G(b, x=x, y=y, s=s)


def ground(y=360, color=GRASS):
    return R(0, y, W, H - y, color) + P(f"M0,{y} L{W},{y}", stroke=GRASS_D, sw=2)


def grass_tufts(points):
    out = ""
    for x, y in points:
        out += P(f"M{x-6},{y} L{x-3},{y-9} M{x},{y} L{x},{y-12} M{x+6},{y} L{x+3},{y-9}", stroke=GRASS_D, sw=2.2)
    return out


def river(y_top=300, y_bot=420):
    out = [P(f"M0,{y_top} C200,{y_top-14} 420,{y_top+12} 800,{y_top-6} L800,{y_bot} "
             f"C520,{y_bot+12} 240,{y_bot-10} 0,{y_bot+4} Z", "url(#water)", stroke="none")]
    for i, yy in enumerate(range(y_top + 18, y_bot - 8, 22)):
        off = (i * 97) % 160
        for x in range(40 + off, 800, 210):
            out.append(P(f"M{x},{yy} q12,-6 24,0 t24,0", stroke=WATER_L, sw=2.4, opacity=0.9))
    out.append(P(f"M0,{y_top} C200,{y_top-14} 420,{y_top+12} 800,{y_top-6}", stroke="#ffffff", sw=3, opacity=0.6))
    return "".join(out)


def bank(y=420, color=SAND):
    return P(f"M0,{y+4} C240,{y-10} 520,{y+12} 800,{y} L800,{H} L0,{H} Z", color, stroke="none")


def hut(x, y, s=1.0):
    h = [R(-60, -70, 120, 70, "#dcb27c", stroke=OUT, sw=2.4),
         P("M-60,-46 L60,-46 M-60,-24 L60,-24", stroke="#c39761", sw=1.6),
         R(-16, -48, 32, 48, "#6b4a2e", stroke=OUT, sw=2.4, rx=3),
         P("M-82,-66 L0,-124 L82,-66 Z", "#cfa458", sw=2.4),
         P("M-60,-80 L-48,-74 M-36,-96 L-24,-88 M-12,-112 L0,-104 M20,-104 L30,-96 M44,-92 L56,-84",
           stroke="#a87f3a", sw=2),
         P("M-82,-66 L82,-66", stroke="#a87f3a", sw=3)]
    return G(*h, x=x, y=y, s=s)


def rays(cx, cy, n=14, r1=40, r2=330, color="#ffe9a8", opacity=0.55):
    import math
    out = []
    for i in range(n):
        a1 = 2 * math.pi * i / n
        a2 = a1 + math.pi / n * 0.55
        p = (f"M{cx},{cy} L{cx + r2*math.cos(a1):.1f},{cy + r2*math.sin(a1):.1f} "
             f"L{cx + r2*math.cos(a2):.1f},{cy + r2*math.sin(a2):.1f} Z")
        out.append(P(p, color, stroke="none", opacity=opacity))
    out.append(C(cx, cy, r1 * 2.6, "url(#glow)", stroke="none"))
    return "".join(out)


def thought_bubble(x, y, w=150, h=96, tail="left"):
    k = -1 if tail == "left" else 1
    return G(E(0, 0, w / 2, h / 2, "#ffffff", sw=2.2, opacity=0.95),
             C(k * (w / 2 - 6), h / 2 + 4, 9, "#ffffff", sw=2), C(k * (w / 2 + 8), h / 2 + 18, 5, "#ffffff", sw=2),
             x=x, y=y)


def mountain_icon(x, y, s=1.0):
    m = (P("M-40,0 L-12,-46 L4,-20 L18,-38 L44,0 Z", "#9db7c9", sw=2.2) +
         P("M-12,-46 L-4,-34 L-12,-36 L-18,-34 Z", "#ffffff", sw=1.6))
    return G(m, x=x, y=y, s=s)


def river_icon(x, y, s=1.0):
    r = (P("M-44,0 C-24,-10 -8,6 8,-4 C22,-12 32,0 44,-6", stroke=WATER_D, sw=7) +
         P("M-44,0 C-24,-10 -8,6 8,-4 C22,-12 32,0 44,-6", stroke=WATER, sw=4))
    return G(r, x=x, y=y, s=s)


def leaf_feather(x, y, rot=0, color=CRANE_D):
    return G(P("M0,0 C4,-6 4,-14 0,-20 C-4,-14 -4,-6 0,0 Z", color, sw=1.4) +
             P("M0,0 L0,-18", stroke=OUT, sw=0.9), x=x, y=y, rot=rot)
