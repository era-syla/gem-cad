import cadquery as cq

# Parameters
L = 60           # Base length
W = 20           # Base width
T = 5            # Base thickness
wall_thickness = 5
H = 30           # Wall height
slot_length = 30
slot_width = 5
slot_offset = 10
hole_d = 4

# Build base
result = cq.Workplane("XY").box(L, W, T).translate((0, 0, T/2))

# Add vertical wall on one short side
result = result.union(
    cq.Workplane("XY")
      .workplane(offset=T)
      .center(-L/2 + wall_thickness/2, 0)
      .box(wall_thickness, W, H)
)

# Cut slot through the top face of the base
x_slot = -L/2 + wall_thickness + slot_offset + slot_length/2
result = (
    result
    .faces(">Z")
    .workplane()
    .center(x_slot, 0)
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# Drill two holes through the vertical wall
hole_x = -L/2 + wall_thickness/2
cutters = (
    cq.Workplane("YZ")
      .workplane(offset=hole_x)
      .pushPoints([(0, H/4), (0, -H/4)])
      .circle(hole_d/2)
      .extrude(wall_thickness + T)
)
result = result.cut(cutters)