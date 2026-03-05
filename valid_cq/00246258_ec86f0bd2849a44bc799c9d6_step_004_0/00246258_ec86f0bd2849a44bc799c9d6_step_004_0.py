import cadquery as cq

# --- Parameter Definitions ---
# Base dimensions
base_length = 100.0
base_width = 40.0
base_height = 5.0

# Main body dimensions
body_length = 60.0
body_width = 24.0
body_wall_height = 30.0  # Height of the vertical walls
body_dome_height = 6.0   # Height of the curved top (sagitta) from the wall top

# Top boss dimensions
boss_size = 10.0
boss_height = 1.5
boss_offset_x = 15.0  # Distance from center along the length

# --- Modeling ---

# 1. Create the rectangular base
# Centered on XY plane, extruded upwards from Z=0
base = cq.Workplane("XY").box(base_length, base_width, base_height, centered=(True, True, False))

# 2. Create the main body with curved top
# We draw the profile on the YZ plane (side view) and extrude along X
# Coordinate mapping for YZ plane: horizontal=World Y, vertical=World Z
body = (
    cq.Workplane("YZ")
    .workplane(origin=(0, 0, 0))  # Ensure origin is world origin
    .moveTo(-body_width / 2, base_height)
    .lineTo(body_width / 2, base_height)
    .lineTo(body_width / 2, base_height + body_wall_height)
    # Create the dome arc: start, peak point, end
    .threePointArc(
        (0, base_height + body_wall_height + body_dome_height),  # Peak
        (-body_width / 2, base_height + body_wall_height)        # End
    )
    .close()
    .extrude(body_length / 2, both=True)  # Symmetric extrusion along X
)

# 3. Create the top boss
# We create a box that starts inside the body and protrudes out the top.
# Starting the extrusion from the top of the vertical walls ensures it's buried inside the dome.
# Final Z height desired = base + wall + dome + boss_height
current_peak_z = base_height + body_wall_height + body_dome_height
extrusion_start_z = base_height + body_wall_height
extrusion_length = (current_peak_z + boss_height) - extrusion_start_z

boss = (
    cq.Workplane("XY")
    .workplane(offset=extrusion_start_z)
    .center(boss_offset_x, 0)
    .rect(boss_size, boss_size)
    .extrude(extrusion_length)
)

# --- Final Assembly ---
result = base.union(body).union(boss)