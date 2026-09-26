#!/usr/bin/env python3
"""Generate static/images/events-map.svg from data/places.yaml.
Requires: pip install basemap pyyaml   (coastlines from GSHHS, crude resolution)."""
import yaml, numpy as np
from mpl_toolkits.basemap import Basemap

places = yaml.safe_load(open('data/places.yaml'))
# Robinson projection centred on 0°, then crop to the region of interest
m = Basemap(projection='robin', lon_0=0, resolution='c')
def P(lon, lat):
    x, y = m(lon, lat); return x, y
# crop box in projected coords (lon -110..110, lat 0..80 roughly)
x0, y0 = P(-100, 5); x1, y1 = P(100, 5); _, yt = P(0, 84); _, yb = P(0, 5)
W = x1 - x0; H = yt - yb
sx = 1000 / W                        # scale to a 1000-wide viewBox
def T(x, y): return (x - x0) * sx, (yt - y) * sx
land = []
for poly, typ in zip(m.coastpolygons, m.coastpolygontypes):
    if typ != 1: continue           # 1 = land (skip lakes etc.)
    xs, ys = poly
    pts = [T(x, y) for x, y in zip(xs, ys)]
    pts = [(round(x, 1), round(y, 1)) for x, y in pts]
    if len(pts) < 8: continue
    # skip polygons fully outside the crop
    if max(p[0] for p in pts) < 0 or min(p[0] for p in pts) > 1000 or max(p[1] for p in pts) < 0 or min(p[1] for p in pts) > H * sx: continue
    land.append('M' + ' '.join(f'{x},{y}' for x, y in pts) + 'Z')
vh = round(H * sx, 1)
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {vh}" role="img" aria-label="Map of places where Cordian Riener has organized events">',
       '<style>.land{fill:var(--tint,#EDF1EF);stroke:var(--hairline,#D9DFE1);stroke-width:0.6}.dot{fill:var(--accent,#1E647F)}.home{fill:none;stroke:var(--accent,#1E647F);stroke-width:1.2}.lbl{font:11px "STIX Two Text",Georgia,serif;fill:var(--soft,#4E6076)}</style>',
       f'<clipPath id="c"><rect width="1000" height="{vh}"/></clipPath><g clip-path="url(#c)">',
       '<path class="land" d="' + ' '.join(land) + '"/>']
# label offsets (dx, dy) per place to avoid collisions
off = {'Tromsø': (11, 1), 'Narvik': (11, 14), 'Nordfjordeid': (-8, -6), 'Bergen': (-8, 10), 'Helsinki': (8, 4),
       'Konstanz': (8, 10), 'Oberwolfach': (-8, -6), 'Marseille': (8, 8), 'Barcelona': (-8, 12), 'Providence': (8, 4), 'Mumbai': (8, 4)}
for p in places:
    x, y = T(*P(p['lon'], p['lat']))
    dx, dy = off.get(p['name'], (8, 4))
    anchor = 'end' if dx < 0 else 'start'
    out.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="3.2"><title>{p["name"]}: {p.get("note","")}</title></circle>')
    if p.get('home'): out.append(f'<circle class="home" cx="{x:.1f}" cy="{y:.1f}" r="7"/>')
    out.append(f'<text class="lbl" x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}">{p["name"]}</text>')
out.append('</g></svg>')
open('static/images/events-map.svg', 'w').write('\n'.join(out))
print('wrote events-map.svg', sum(len(s) for s in out)//1024, 'KB; viewBox 1000 x', vh)
