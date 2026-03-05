import cadquery as cq
import math

# Main dimensions
main_radius = 30
main_height = 35
fin_count = 12
fin_height = 2.5
fin_depth = 4
front_face_radius = 28
back_stub_radius = 8
back_stub_height = 8
front_stub_radius = 6
front_stub_height = 5

# Build main cylinder body
result = cq.Workplane("XY").cylinder(main_height, main_radius)

# Add cooling fins (rings around the cylinder)
fin_spacing = main_height / (fin_count + 1)
for i in range(fin_count):
    z_pos = -main_height/2 + fin_spacing * (i + 1)
    fin = (cq.Workplane("XY")
           .workplane(offset=z_pos)
           .circle(main_radius + fin_depth)
           .circle(main_radius)
           .extrude(fin_height/2, both=True))
    result = result.union(fin)

# Add back stub (connector on the right/back side - along Z axis top)
back_stub = (cq.Workplane("XY")
             .workplane(offset=main_height/2)
             .circle(back_stub_radius)
             .extrude(back_stub_height))
result = result.union(back_stub)

# Add front stub (small protrusion on front/bottom)
front_stub = (cq.Workplane("XY")
              .workplane(offset=-main_height/2)
              .circle(front_stub_radius)
              .extrude(front_stub_height))
result = result.union(front_stub)

# Now add the front face flat area - the front face has a flat ring
# The front face shows holes arranged in a circle

# Add a flat disc on the front face
front_disc = (cq.Workplane("XY")
              .workplane(offset=-(main_height/2 + front_stub_height))
              .circle(front_face_radius)
              .extrude(3))
result = result.union(front_disc)

# Drill holes in the front face - arranged in two circles
# Outer ring: 8 holes
outer_hole_radius = 18
outer_hole_dia = 5
outer_hole_count = 8

for i in range(outer_hole_count):
    angle = i * 360.0 / outer_hole_count
    x = outer_hole_radius * math.cos(math.radians(angle))
    y = outer_hole_radius * math.sin(math.radians(angle))
    hole = (cq.Workplane("XY")
            .workplane(offset=-(main_height/2 + front_stub_height + 3))
            .center(x, y)
            .circle(outer_hole_dia/2)
            .extrude(10))
    result = result.cut(hole)

# Inner ring: 4 holes (or small slots)
inner_hole_radius = 9
inner_hole_dia = 4
inner_hole_count = 4

for i in range(inner_hole_count):
    angle = i * 360.0 / inner_hole_count + 45
    x = inner_hole_radius * math.cos(math.radians(angle))
    y = inner_hole_radius * math.sin(math.radians(angle))
    hole = (cq.Workplane("XY")
            .workplane(offset=-(main_height/2 + front_stub_height + 3))
            .center(x, y)
            .circle(inner_hole_dia/2)
            .extrude(10))
    result = result.cut(hole)

# Center hole
center_hole = (cq.Workplane("XY")
               .workplane(offset=-(main_height/2 + front_stub_height + 3))
               .circle(3)
               .extrude(12))
result = result.cut(center_hole)

# Small slot at bottom of front face
slot = (cq.Workplane("XY")
        .workplane(offset=-(main_height/2 + front_stub_height + 3))
        .center(0, -front_face_radius + 4)
        .rect(6, 3)
        .extrude(5))
result = result.cut(slot)