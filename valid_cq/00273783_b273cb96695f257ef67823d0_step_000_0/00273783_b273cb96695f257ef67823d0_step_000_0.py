import cadquery as cq

# --- Dimensions & Parameters ---
# Handle dimensions
handle_length = 60.0
handle_diameter = 16.0
pommel_diameter = 22.0

# Guard dimensions
guard_width = 90.0
guard_thickness = 18.0      # Thickness in Y (depth)
guard_height_tips = 30.0    # Z height at the tips
guard_height_center = 12.0  # Z height at the center (where blade meets)
guard_vertical_width = 15.0 # Vertical thickness of the guard profile

# Blade dimensions
blade_width = 30.0
blade_thickness = 6.0
blade_length = 160.0        # Length of the straight section
blade_tip_length = 30.0     # Length of the triangular tip section

# --- Geometry Construction ---

# 1. Handle (Grip)
# Cylindrical handle extending downwards from Z=0
handle = cq.Workplane("XY").circle(handle_diameter / 2.0).extrude(-handle_length)

# 2. Pommel
# Sphere at the bottom of the handle
pommel = (
    cq.Workplane("XY")
    .workplane(offset=-handle_length)
    .sphere(pommel_diameter / 2.0)
)

# 3. Guard (Crossguard)
# Created by sketching the profile on the Front (XZ) plane and extruding in Y.
# We define coordinates for a curved "U" shape.
g_half_width = guard_width / 2.0
g_tip_z = guard_height_tips
g_mid_top_z = guard_height_center
g_mid_bot_z = 0.0
g_tip_bot_z = guard_height_tips - guard_vertical_width

guard = (
    cq.Workplane("XZ")
    .moveTo(-g_half_width, g_tip_z)
    # Top edge curve: Left tip -> Center -> Right tip
    .threePointArc((0, g_mid_top_z), (g_half_width, g_tip_z))
    # Right vertical edge
    .lineTo(g_half_width, g_tip_bot_z)
    # Bottom edge curve: Right tip bot -> Center bot -> Left tip bot
    .threePointArc((0, g_mid_bot_z), (-g_half_width, g_tip_bot_z))
    .close()
    .extrude(guard_thickness / 2.0, both=True)
)

# 4. Blade
# Created by sketching the profile on the Front (XZ) plane and extruding in Y.
# Starts slightly inside the guard for a solid connection.
blade_half_width = blade_width / 2.0
blade_start_z = guard_height_center - 2.0
blade_straight_top_z = guard_height_center + blade_length
blade_tip_z = blade_straight_top_z + blade_tip_length

blade = (
    cq.Workplane("XZ")
    .moveTo(-blade_half_width, blade_start_z)
    .lineTo(-blade_half_width, blade_straight_top_z) # Left edge
    .lineTo(0, blade_tip_z)                          # To Tip
    .lineTo(blade_half_width, blade_straight_top_z)  # Right edge
    .lineTo(blade_half_width, blade_start_z)         # Back to base
    .close()
    .extrude(blade_thickness / 2.0, both=True)
)

# --- Assembly ---
# Combine all parts into a single solid
result = handle.union(pommel).union(guard).union(blade)