#!/usr/bin/env python3
"""Build the homepage scanpath figure for emipws.org from the corrected EMIP dataset.

Data: "Corrected EMIP Dataset" (finalset_line_part.csv) from the EMIP Toolkit,
https://github.com/nalmadi/EMIP-Toolkit (Al Madi et al., ETRA 2021), derived from the
EMIP dataset (Bednarik et al., 2020, CC BY 4.0).

Usage:
  python3 make_scanpath.py finalset_line_part.csv --participant 182 --n 45 > _includes/scanpath.html

The code text is re-typeset at the stimulus' original pixel coordinates (recovered from
the token AOIs in the same file), so fixation coordinates are drawn unmodified.
"""
import argparse, csv, html, math, sys
from collections import defaultdict

SRC = """public class Rectangle {
private int x1 , y1 , x2 , y2 ;
public Rectangle ( int x1 , int y1 , int x2 , int y2 ) {
this.x1 = x1 ;
this.y1 = y1 ;
this.x2 = x2 ;
this.y2 = y2 ;
}
public int width ( ) { return this.x2 - this.x1 ; }
public int height ( ) { return this.y2 - this.y1 ; }
public double area ( ) { return this.width ( ) * this.height ( ) ; }
public static void main ( String [ ] args ) {
Rectangle rect1 = new Rectangle ( 0 , 0 , 10 , 10 ) ;
System.out.println ( rect1.area ( ) ) ;
Rectangle rect2 = new Rectangle ( 5 , 5 , 10 , 10 ) ;
System.out.println ( rect2.area ( ) ) ;
}
}""".split("\n")
STIMULUS = "rectangle_java2.jpg"
CHAR_W = 9.79   # px per character, least-squares fit over all token AOIs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--participant", type=int, default=182)
    ap.add_argument("--n", type=int, default=45)
    a = ap.parse_args()

    rows = [r for r in csv.DictReader(open(a.csv, newline="")) if r["code_file"] == STIMULUS]
    # line geometry: first token's AOI per line gives x0, AOI y gives the line box
    first = {}
    for r in rows:
        ln, part = int(r["line"]), int(r["part"])
        if ln not in first or part < first[ln][0]:
            first[ln] = (part, float(r["aoi_x"]), float(r["aoi_y"]), float(r["aoi_height"]))
    fx = sorted((r for r in rows if int(r["participant"]) == a.participant),
                key=lambda r: int(r["timestamp"]))[: a.n]
    if not fx:
        sys.exit("no fixations for that participant")
    # Offset correction (as in EMTK): shift the trial vertically by the median distance
    # between each fixation and the centre of the code line it was assigned to.
    allp = [r for r in rows if int(r["participant"]) == a.participant]
    dys = sorted(float(r["y_cord"]) - (float(r["aoi_y"]) + float(r["aoi_height"]) / 2) for r in allp)
    dy = dys[len(dys) // 2]
    t0 = int(fx[0]["timestamp"])
    pts = [(float(r["x_cord"]), float(r["y_cord"]) - dy, int(r["duration"]),
            round((int(r["timestamp"]) - t0) / 1000)) for r in fx]
    span_s = (pts[-1][3] + pts[-1][2]) / 1000

    X0, Y0, W, H = 556, 186, 800, 690
    # On phones the frame crops to the region the fixations cover, so the code stays legible.
    pad = 26
    cx0 = max(X0, min(p[0] for p in pts) - pad - 20)
    cx1 = min(X0 + W, max(p[0] for p in pts) + pad + 20)
    cy0 = max(Y0, min(p[1] for p in pts) - pad)
    cy1 = min(Y0 + H, max(p[1] for p in pts) + pad)
    cw, ch = cx1 - cx0, cy1 - cy0
    crop = (f"--crop-ar:{cw:.0f}/{ch:.0f};--crop-w:{100*W/cw:.2f}%;"
            f"--crop-x:{-100*(cx0-X0)/cw:.2f}%;--crop-y:{-100*(cy0-Y0)/ch:.2f}%")
    out = []
    o = out.append
    o('<figure class="scanpath" data-scanpath>')
    o(f'<div class="scanpath__frame" style="{crop}">')
    o(f'<svg viewBox="{X0} {Y0} {W} {H}" role="img" aria-labelledby="scanpath-title scanpath-desc">')
    o(f'<title id="scanpath-title">Scanpath of one programmer reading Rectangle.java</title>')
    o(f'<desc id="scanpath-desc">{len(pts)} fixations from participant {a.participant} of the EMIP dataset, '
      f'drawn as circles sized by duration and joined in reading order over the Java stimulus.</desc>')
    o('<g class="scanpath__code">')
    for ln, text in enumerate(SRC, start=1):
        if ln not in first:
            continue
        _, x, y, h = first[ln]
        base = y + 12.5  # token AOIs start at the ascender line; baseline sits ~12.5px below
        o(f'<text x="{x:.0f}" y="{base:.0f}" textLength="{len(text)*CHAR_W:.0f}" lengthAdjust="spacing">{html.escape(text)}</text>')
    o('</g>')
    o('<g class="scanpath__saccades">')
    for i in range(1, len(pts)):
        (x1, y1, _, _), (x2, y2, _, t) = pts[i-1], pts[i]
        o(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" style="--t:{t}"/>')
    o('</g>')
    o('<g class="scanpath__fixations">')
    for i, (x, y, d, t) in enumerate(pts, start=1):
        r = 3 + math.sqrt(d) * 1.15
        label = ""
        if i == 1 or i == len(pts):
            label = f'<text x="{x:.1f}" y="{y - r - 4:.1f}">{i}</text>'
        o(f'<g style="--t:{t}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>{label}</g>')
    o('</g>')
    o('</svg>')
    o('</div>')
    o('<figcaption><span class="scanpath__label">Fig. 1</span> '
      f'The first {len(pts)} fixations on the code ({span_s:.1f}&nbsp;s) of participant {a.participant} reading '
      '<code>Rectangle.java</code>, from the <a href="/#corrected-dataset">corrected EMIP dataset</a>. '
      'Circle size follows fixation duration. '
      + (f'The trial is shifted {abs(dy):.0f}&nbsp;px vertically by its median line offset. ' if abs(dy) >= 2 else '')
      +
      '<button type="button" class="scanpath__replay" hidden>Replay</button></figcaption>')
    o('</figure>')
    print("\n".join(out))

if __name__ == "__main__":
    main()
