import cadquery as cq

# --- Dimensions & Parameters ---
# Main Block
block_len = 85.0
block_width = 45.0
block_height = 60.0
chamfer_size = 6.0

# Top Cylindrical Boss
boss_dia = 38.0
boss_height = 4.0
boss_offset_x = 20.0  # Offset from center along X
boss_hole_pcd = 24.0
boss_hole_dia = 5.0
boss_cbore_dia = 9.5
boss_cbore_depth = 3.0
dimple_radius = 8.5

# Top Linear Holes (3 holes)
top_holes_x = -28.0
top_holes_spacing = 11.0
top_hole_dia = 5.0
top_hole_cbore = 9.0
top_hole_cbore_depth = 2.0

# Side Features (Front Face)
side_boss_size = 14.0
side_boss_height = 3.0
side_boss_x_left = -26.0
side_boss_x_right = 18.0
side_boss_z_top = 12.0
side_boss_z_bot = -15.0

side_hole_dia = 6.0
side_hole_cbore = 10.5
side_hole_cbore_depth = 3.5

side_mid_hole_dia = 4.0
side_mid_hole_cbore = 7.0
side_mid_z = -1.5

# --- Modeling Operations ---

# 1. Create Base Block with chamfered vertical edges
result = (
    cq.Workplane("XY")
    .box(block_len, block_width, block_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# 2. Extrude Top Cylindrical Boss
result = (
    result.faces(">Z").workplane()
    .center(boss_offset_x, 0)
    .circle(boss_dia / 2.0)
    .extrude(boss_height)
)

# 3. Create Features on Top Boss (Holes & Dimple)
# 5-hole pattern
result = (
    result.faces(">Z").workplane()
    .center(boss_offset_x, 0)
    .polarArray(boss_hole_pcd / 2.0, 0, 360, 5)
    .cboreHole(boss_hole_dia, boss_cbore_dia, boss_cbore_depth)
)

# Central Spherical Dimple
# We create a sphere and cut it from the main body.
# Center Z of sphere is at the top surface of the boss.
sphere_z = (block_height / 2.0) + boss_height
sphere_tool = (
    cq.Workplane("XY")
    .sphere(dimple_radius)
    .translate((boss_offset_x, 0, sphere_z))
)
result = result.cut(sphere_tool)

# 4. Create Linear Holes on the Top Shelf
# Target the main block top face (Z = block_height / 2)
result = (
    result.workplane(offset=block_height / 2.0) # Absolute Z plane
    .center(top_holes_x, 0)
    .pushPoints([(0, top_holes_spacing), (0, 0), (0, -top_holes_spacing)])
    .cboreHole(top_hole_dia, top_hole_cbore, top_hole_cbore_depth)
)

# 5. Create Side Square Bosses
# Define positions on the side face (XZ plane looking from -Y)
boss_locations = [
    (side_boss_x_left, side_boss_z_top),
    (side_boss_x_left, side_boss_z_bot),
    (side_boss_x_right, side_boss_z_top),
    (side_boss_x_right, side_boss_z_bot),
]

# Extrude the square bosses from the front face (<Y)
result = (
    result.faces("<Y").workplane()
    .pushPoints(boss_locations)
    .rect(side_boss_size, side_boss_size)
    .extrude(side_boss_height)
)

# 6. Create Holes through Side Bosses
# Select the new outermost faces (<Y) and drill holes
result = (
    result.faces("<Y").workplane()
    .pushPoints(boss_locations)
    .cboreHole(side_hole_dia, side_hole_cbore, side_hole_cbore_depth)
)

# 7. Create Small Holes between Side Bosses
# These holes are on the recessed surface (between bosses).
# We select the outer face and offset the workplane back to the base surface level.
mid_hole_locations = [
    (side_boss_x_left, side_mid_z),
    (side_boss_x_right, side_mid_z),
]

result = (
    result.faces("<Y").workplane()
    .workplane(offset=-side_boss_height) # Offset back to main face
    .pushPoints(mid_hole_locations)
    .cboreHole(side_mid_hole_dia, side_mid_hole_cbore, 2.0)
)

# 8. Create Rectangular Recess/Label area between bottom bosses
# Position centered between the bottom two bosses
recess_center_x = (side_boss_x_left + side_boss_x_right) / 2.0
recess_width = (side_boss_x_right - side_boss_x_left) - side_boss_size - 4.0
recess_height = side_boss_size - 4.0

result = (
    result.faces("<Y").workplane(offset=-side_boss_height) # On base surface
    .center(recess_center_x, side_boss_z_bot)
    .rect(recess_width, recess_height)
    .cutBlind(-1.0) # Shallow cut into the body
)