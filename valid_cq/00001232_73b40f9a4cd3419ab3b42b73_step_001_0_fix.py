import cadquery as cq

# Dimensions
outer_width = 120
outer_depth = 100
wall_thickness = 3
base_thickness = 4
inner_height = 20
total_height = base_thickness + inner_height

# Slot dimensions on the right wall
slot_width = 12
slot_height = 6
slot_depth = wall_thickness + 2

# Create the outer box
outer_box = (
    cq.Workplane("XY")
    .box(outer_width, outer_depth, total_height)
)

# Create inner cavity to hollow out the box (leaving base and walls)
inner_width = outer_width - 2 * wall_thickness
inner_depth = outer_depth - 2 * wall_thickness
inner_cavity_height = inner_height + 1  # extra to ensure clean cut through top

inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness / 2)
    .box(inner_width, inner_depth, inner_cavity_height + base_thickness)
    .translate((0, 0, (inner_cavity_height) / 2))
)

# Hollow out the box
tray = outer_box.cut(
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .box(inner_width, inner_depth, inner_height + 1)
    .translate((0, 0, base_thickness / 2 + inner_height / 2))
)

# Add slot cutout on the right wall (front-right area)
# Right wall is at x = outer_width/2
slot_x = outer_width / 2 - wall_thickness / 2
slot_y = outer_depth / 4  # positioned toward front on right side
slot_z = base_thickness + inner_height / 2

slot_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-slot_x - 1)
    .center(slot_y, slot_z)
    .rect(slot_width, slot_height)
    .extrude(wall_thickness + 2)
)

result = tray.cut(
    cq.Workplane("XY")
    .workplane(offset=slot_z - slot_height / 2)
    .center(outer_width / 2 - wall_thickness / 2, slot_y)
    .rect(wall_thickness + 2, slot_width)
    .extrude(slot_height)
)

# Re-do more carefully
# Build tray as shell open on top
result = (
    cq.Workplane("XY")
    .box(outer_width, outer_depth, total_height)
    .faces(">Z")
    .shell(-wall_thickness, kind="intersection")
)

# Cut the slot on the right side wall
# Right wall center at x = outer_width/2 - wall_thickness/2
# Slot: small rectangular cutout
slot_cutter = (
    cq.Workplane("XY")
    .center(outer_width / 2 - wall_thickness / 2, outer_depth / 4)
    .workplane(offset=base_thickness + 4)
    .rect(wall_thickness + 4, slot_width)
    .extrude(slot_height)
)

result = result.cut(slot_cutter)