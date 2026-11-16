# Removes the star and fork counters from the generated 3D calendar. They only count public
# repositories and would always show 0. Add group start tags to TARGETS to remove more parts.
import re
import sys

PATH = "profile-3d-contrib/profile-customize.svg"
TARGETS = ()  # pie and radar stay now that the token sees private repositories

svg = open(PATH, encoding="utf-8").read()
for start_tag in TARGETS:
    start = svg.find(start_tag)
    if start < 0:
        continue
    depth, pos = 0, start
    for m in re.finditer(r"<g[\s>]|</g>", svg[start:]):
        depth += -1 if m.group() == "</g>" else 1
        if depth == 0:
            pos = start + m.end()
            break
    svg = svg[:start] + svg[pos:]
# Stars and forks only count public repositories, so they would always show 0
star = svg.find('<g transform="translate(608, 802), scale(2)">')
date = svg.find('<text style="font-size: 16px;"', star)
if star >= 0 and date > star:
    svg = svg[:star] + svg[date:]

open(PATH, "w", encoding="utf-8").write(svg)
print("counters removed")
