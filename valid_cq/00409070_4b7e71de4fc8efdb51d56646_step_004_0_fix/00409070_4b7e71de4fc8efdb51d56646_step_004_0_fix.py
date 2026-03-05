import cadquery as cq

# Parameters
base_length = 120
base_width = 20
base_thickness = 5
wall_height = 30
wall_thickness = 5
wall_offset = 40
hole_diameter = 6
slot_length = 20
slot_width = 10
rib_height = 10
rib_thickness = 5
rib_width = 15
rib_positions = [-40, 0, 40]

# Build base plate
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Add vertical side walls
for x in (-wall_offset, wall_offset):
    result = result.union(
        cq.Workplane("XY")
          .workplane(offset=base_thickness)
          .center(x, 0)
          .rect(wall_thickness, base_width)
          .extrude(wall_height)
    )

# Cut central rectangular slot through the base
result = result.faces(">Z").workplane().center(0, 0).rect(slot_length, slot_width).cutBlind(-base_thickness)

# Drill holes through the side walls
for x in (-wall_offset, wall_offset):
    result = result.cut(
        cq.Workplane("XY")
          .center(x, 0)
          .circle(hole_diameter/2)
          .extrude(wall_height + base_thickness)
    )

# Add reinforcing ribs on underside of base
result = result.faces("<Z").workplane().pushPoints([(x, 0) for x in rib_positions]) \
    .rect(rib_width, rib_thickness).extrude(-rib_height)