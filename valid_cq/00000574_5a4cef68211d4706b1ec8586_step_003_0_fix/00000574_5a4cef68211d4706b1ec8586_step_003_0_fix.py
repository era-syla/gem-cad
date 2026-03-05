import cadquery as cq

# Dimensions
outer_radius = 30
inner_radius = 25
height = 60
flange_radius = 33
flange_height = 4
wall_thickness = 5

# Slot dimensions
slot_width = 12
slot_height = 8
slot_depth = wall_thickness + 2  # cuts through wall
slot_z = 15  # height from bottom

# Create the main cylindrical body (hollow)
outer_cylinder = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)

inner_cylinder = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)

body = outer_cylinder.cut(inner_cylinder)

# Add flange at top
flange = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .circle(flange_radius)
    .extrude(flange_height)
)

flange_inner = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .circle(inner_radius)
    .extrude(flange_height)
)

flange_ring = flange.cut(flange_inner)

# Combine body and flange
combined = body.union(flange_ring)

# Cut rectangular slots in the lower portion of the cylinder
# Two slots on opposite sides
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=slot_z)
    .center(outer_radius - slot_depth / 2, 0)
    .box(slot_depth + 4, slot_width, slot_height, centered=True)
)

slot2 = (
    cq.Workplane("XY")
    .workplane(offset=slot_z)
    .center(-(outer_radius - slot_depth / 2), 0)
    .box(slot_depth + 4, slot_width, slot_height, centered=True)
)

result = combined.cut(slot1).cut(slot2)