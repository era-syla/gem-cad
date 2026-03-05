import cadquery as cq

# Dimensions
outer_radius = 30
inner_radius = 25
height = 60
wall_thickness = outer_radius - inner_radius

# Flange dimensions
flange_radius = 34
flange_thickness = 4

# Slot dimensions
slot_width = 14
slot_height = 8
slot_depth = wall_thickness + 2  # through the wall
slot_y_offset = outer_radius - 1  # position at the surface

# Create the main cylinder (hollow)
result = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
)

# Hollow out the cylinder
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-height)
)

# Add flange at the top
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(flange_radius)
    .circle(inner_radius)
    .extrude(flange_thickness)
)

# Cut rectangular slots near the bottom
# Two slots on opposite sides
slot_z_position = -height / 2 + slot_height / 2 + 8  # near bottom

# Slot 1 - front
result = (
    result
    .workplane(offset=slot_z_position)
    .center(0, 0)
    .transformed(offset=cq.Vector(0, 0, 0))
)

# Use box cuts for slots
# Slot 1
slot1 = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, slot_y_offset, slot_z_position))
    .box(slot_width, slot_depth * 2, slot_height)
)

result = result.cut(slot1)

# Slot 2 - rotated 90 degrees
slot2 = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(slot_y_offset, 0, slot_z_position))
    .box(slot_depth * 2, slot_width, slot_height)
)

result = result.cut(slot2)

# Add fillets to the top flange edge
result = (
    result
    .faces(">Z")
    .edges("%Circle")
    .fillet(1.0)
)