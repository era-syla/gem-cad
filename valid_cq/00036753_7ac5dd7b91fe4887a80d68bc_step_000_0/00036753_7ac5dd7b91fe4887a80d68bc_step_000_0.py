import cadquery as cq

# --- Parametric Dimensions ---
total_height = 70.0
diameter = 40.0
radius = diameter / 2.0

# Groove parameters
groove_z_center = 40.0  # Height of the groove from the bottom
groove_width = 2.0
groove_depth = 1.0

# Top boss parameters
boss_diameter = 13.0
boss_height = 9.0
boss_offset = 11.0  # Distance from center to boss center axis
boss_hole_diameter = 7.0

# Top mounting holes parameters
mount_hole_diameter = 3.0
mount_hole_depth = 10.0
mount_hole_x = 5.0
mount_hole_y = 12.0

# --- Geometry Construction ---

# 1. Main Body with Groove (Revolve Method)
# Define the profile points on the XZ plane to revolve around Z axis.
# Points are ordered counter-clockwise starting from the origin.
p_outer = radius
p_inner = radius - groove_depth
z_g_bottom = groove_z_center - (groove_width / 2.0)
z_g_top = groove_z_center + (groove_width / 2.0)

profile_pts = [
    (0, 0),                  # Center bottom
    (p_outer, 0),            # Outer bottom edge
    (p_outer, z_g_bottom),   # Groove start
    (p_inner, z_g_bottom),   # Groove inner corner bottom
    (p_inner, z_g_top),      # Groove inner corner top
    (p_outer, z_g_top),      # Groove end
    (p_outer, total_height), # Outer top edge
    (0, total_height)        # Center top
]

# Create the base solid
result = cq.Workplane("XZ").polyline(profile_pts).close().revolve()

# 2. Mounting Holes
# Create the small blind holes on the top face of the main cylinder.
# We perform this before adding the boss to easily select the main top face.
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (mount_hole_x, mount_hole_y), 
        (mount_hole_x, -mount_hole_y)
    ])
    .circle(mount_hole_diameter / 2.0)
    .cutBlind(-mount_hole_depth)
)

# 3. Top Boss
# Add the offset cylindrical boss to the top face.
result = (
    result.faces(">Z").workplane()
    .center(-boss_offset, 0)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)

# 4. Boss Hole
# Cut the hole through the boss.
# Selecting ">Z" now grabs the top face of the newly created boss.
result = (
    result.faces(">Z").workplane()
    .circle(boss_hole_diameter / 2.0)
    .cutBlind(-(boss_height + 5.0)) # Cut through boss and slightly into the body
)