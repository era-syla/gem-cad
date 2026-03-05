import cadquery as cq
import math

# Parameters
plate_length = 120
plate_width = 40
plate_thickness = 5
hole_diameter = 20
hole_spacing = 50
apothem = (hole_diameter/2) * math.cos(math.pi/8)
tab_depth = 3
tab_length = 8

# Create base plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Cut three octagonal holes
for x in (-hole_spacing, 0, hole_spacing):
    result = result.faces(">Z").workplane().center(x, 0).polygon(8, hole_diameter).cutThruAll()

# Add rectangular tabs inside each hole
tab_configs = [
    (0,  apothem - tab_depth/2, tab_length, tab_depth),   # top tab
    (0, -apothem + tab_depth/2, tab_length, tab_depth),   # bottom tab
    ( apothem - tab_depth/2, 0, tab_depth, tab_length),   # right tab
    (-apothem + tab_depth/2, 0, tab_depth, tab_length),   # left tab
]

for x in (-hole_spacing, 0, hole_spacing):
    for dx, dy, wx, wy in tab_configs:
        tab = cq.Workplane("XY").box(wx, wy, plate_thickness).translate((x + dx, dy, 0))
        result = result.union(tab)

# Final result
result