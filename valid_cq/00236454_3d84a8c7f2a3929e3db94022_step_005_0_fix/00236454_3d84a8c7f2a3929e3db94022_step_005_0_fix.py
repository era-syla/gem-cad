import cadquery as cq
import math

# Parameters
Rinner = 15
Tband = 5
Router = Rinner + Tband
W = 10
Tplate = 3
Plate_length = 12
hole_dia = 3
cb_dia = 6
cb_depth = 2
hrib = 2
rib_length = 5

# Build the C-shaped band
outer = cq.Workplane("XY").circle(Router).extrude(W)
inner = cq.Workplane("XY").circle(Rinner).extrude(W)
band = outer.cut(inner)
# Cut open the right half
open_cut = cq.Workplane("XY").box(Router + 1, 2 * Router + 1, W).translate(((Router + 1) / 2, 0, W / 2))
band = band.cut(open_cut)

# Add internal ribs
for angle_deg in [250, 290]:
    rad = math.radians(angle_deg)
    x = (Rinner + hrib / 2) * math.cos(rad)
    y = (Rinner + hrib / 2) * math.sin(rad)
    rib = cq.Workplane("XY").box(hrib, rib_length, W).translate((x, y, W / 2))
    band = band.union(rib)

# Top mounting plate with counterbored hole
plate_top = (
    cq.Workplane("XY")
    .rect(Tplate, Plate_length)
    .extrude(W)
    .translate((Router + Tplate / 2, Router, 0))
)
plate_top = plate_top.faces(">X").workplane().center(0, 0).cboreHole(hole_dia, cb_dia, cb_depth)

# Bottom mounting plate with counterbored hole
plate_bot = (
    cq.Workplane("XY")
    .rect(Tplate, Plate_length)
    .extrude(W)
    .translate((Router + Tplate / 2, -Router, 0))
)
plate_bot = plate_bot.faces(">X").workplane().center(0, 0).cboreHole(hole_dia, cb_dia, cb_depth)

# Combine all parts
result = band.union(plate_top).union(plate_bot)