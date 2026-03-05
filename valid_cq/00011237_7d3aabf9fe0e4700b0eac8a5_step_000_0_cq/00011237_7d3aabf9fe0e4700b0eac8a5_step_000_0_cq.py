import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the main box
overall_length = 80.0
overall_width = 40.0
overall_height = 20.0
wall_thickness = 2.0
floor_thickness = 2.0

# Dimensions for the bottom indentation (the "step" underneath)
bottom_step_width = 30.0  # Narrower than overall width
bottom_step_height = 5.0  # How much it sticks down

# Dimensions for the internal divider
divider_thickness = 1.5
divider_height_clearance = 0.0 # Divider flush with top? Looks slightly lower or flush. Assuming flush for simplicity.

# Dimensions for the vertical ribs/guides inside
rib_width = 1.5
rib_depth = 1.5
rib_offset_from_end = 5.0 # Distance from the short wall inner face to the rib

# --- Modeling Strategy ---
# 1. Create the main outer block.
# 2. Add the bottom step/extension.
# 3. Hollow out the main block to create the walls and floor.
# 4. Add the central divider.
# 5. Add the small vertical ribs near the corners.

# --- Geometry Construction ---

# 1. Main body block
main_body = cq.Workplane("XY").box(overall_length, overall_width, overall_height)

# 2. Bottom step
# We add this to the bottom face. 
# Since the box is centered at (0,0,0) with height `overall_height`, 
# the bottom face is at Z = -overall_height/2.
bottom_step = (
    cq.Workplane("XY")
    .workplane(offset=-overall_height/2 - bottom_step_height/2)
    .box(overall_length, bottom_step_width, bottom_step_height)
)

# Combine main body and bottom step
base_solid = main_body.union(bottom_step)

# 3. Create the interior cavity (Shelling)
# We want to remove the top face.
# The top face is at Z = +overall_height/2.
shell = base_solid.faces("+Z").shell(-wall_thickness)

# Calculate internal dimensions for placing features
inner_length = overall_length - 2 * wall_thickness
inner_width = overall_width - 2 * wall_thickness
internal_floor_z = -overall_height/2 + floor_thickness

# 4. Add the central longitudinal divider
# It runs along the X-axis.
divider = (
    cq.Workplane("XY")
    .workplane(offset=internal_floor_z + (overall_height - floor_thickness)/2)
    .box(inner_length, divider_thickness, overall_height - floor_thickness)
)

# 5. Add the vertical ribs
# There are 4 ribs, located near the corners inside.
# They seem to be attached to the long walls, guiding something inserted.
# Actually, looking closely, they are attached to the short walls (end walls) and protrude inwards along X, 
# OR they are on the long walls protruding along Y near the ends.
# Looking at the image:
# - There is a rib on the far short wall, slightly offset from the central divider.
# - Actually, it looks like pairs of ribs on the inner long walls.
# Let's look closer at the crop.
# There is a vertical rectangular feature on the inner face of the *long* wall.
# There is another one on the *central divider*.
# Wait, let's re-examine the image structure.
# It looks like a battery holder or similar.
# There is a central wall.
# On the *short* walls (ends), there are vertical ribs.
# Let's assume ribs are on the inner faces of the short walls to hold a PCB or battery contact.
# But looking at the left side, there is a rib on the long wall too?
# Let's refine the interpretation:
# It looks like slots for a vertical partition or PCB.
# There are ribs on the *inside of the long walls* and ribs on the *central divider*.
# They are aligned to create slots.
# Let's place ribs at a specific X position.

slot_position_x = -overall_length/2 + wall_thickness + 10.0 # Arbitrary position based on visuals
slot_position_x_mirror = -slot_position_x

# Ribs on the long outer walls
rib_h = overall_height - floor_thickness
rib_y_pos = (inner_width / 2) 
rib_z_center = internal_floor_z + rib_h/2

def create_rib(loc_vector):
    return (
        cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(loc_vector.x, loc_vector.y)
        .box(rib_width, rib_depth, rib_h)
    )

# The image shows ribs near the ends. Let's place them near the ends.
rib_offset = 8.0 # distance from inner short wall

# Left side ribs (negative X)
# Rib on top long wall
rib1 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(-inner_length/2 + rib_offset, inner_width/2)
        .box(rib_width, rib_depth, rib_h))

# Rib on bottom long wall
rib2 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(-inner_length/2 + rib_offset, -inner_width/2)
        .box(rib_width, rib_depth, rib_h))

# Ribs on the central divider (matching the ones on the walls)
# Rib on top side of divider
rib3 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(-inner_length/2 + rib_offset, divider_thickness/2)
        .box(rib_width, rib_depth, rib_h))

# Rib on bottom side of divider
rib4 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(-inner_length/2 + rib_offset, -divider_thickness/2)
        .box(rib_width, rib_depth, rib_h))

# Right side ribs (positive X) - Mirroring the concept
# Rib on top long wall
rib5 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(inner_length/2 - rib_offset, inner_width/2)
        .box(rib_width, rib_depth, rib_h))

# Rib on bottom long wall
rib6 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(inner_length/2 - rib_offset, -inner_width/2)
        .box(rib_width, rib_depth, rib_h))

# Rib on top side of divider
rib7 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(inner_length/2 - rib_offset, divider_thickness/2)
        .box(rib_width, rib_depth, rib_h))

# Rib on bottom side of divider
rib8 = (cq.Workplane("XY")
        .workplane(offset=rib_z_center)
        .center(inner_length/2 - rib_offset, -divider_thickness/2)
        .box(rib_width, rib_depth, rib_h))

# The image specifically shows ribs at the far end (right side of image) and near end (left side).
# The ribs on the divider seem T-shaped or just protruding perpendicular.
# In the image:
# Left side: We see a rib on the outer wall inner face, and a rib on the divider. They form a slot.
# Right side: We see the same arrangement.

# Combine all geometry
result = shell.union(divider)
result = result.union(rib1).union(rib2).union(rib3).union(rib4)
result = result.union(rib5).union(rib6).union(rib7).union(rib8)

# Add fillet/chamfer if necessary (not clearly visible, sharp edges assumed)

# Final Result
# result is already defined