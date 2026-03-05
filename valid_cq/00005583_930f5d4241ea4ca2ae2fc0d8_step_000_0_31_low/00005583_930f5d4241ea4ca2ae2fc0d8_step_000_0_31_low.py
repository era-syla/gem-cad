import cadquery as cq

# Parameters
outer_radius = 20.0
inner_radius = 16.0
length = 100.0
cutout_width = 15.0
hole_radius = 2.0
hole_dist_from_end = 15.0

# Base cylinder
base = cq.Workplane("XY").circle(outer_radius).extrude(length)

# Inner hole
inner = cq.Workplane("XY").circle(inner_radius).extrude(length)
result = base.cut(inner)

# Cutout along the length
cutout_box = cq.Workplane("XY").rect(outer_radius * 2, cutout_width).extrude(length).translate((outer_radius, 0, 0))
result = result.cut(cutout_box)

# Small side hole
hole = cq.Workplane("YZ").workplane(offset=0).center(length - hole_dist_from_end, 0).circle(hole_radius).extrude(outer_radius * 2, both=True)
result = result.cut(hole)
