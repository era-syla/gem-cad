import cadquery as cq

# --- Parametric Dimensions ---
# Vertical Plate (The tall central piece)
vp_height = 120.0
vp_width = 30.0
vp_thick = 6.0

# Horizontal Plate (The cross piece)
hp_length = 140.0
hp_width = 30.0
hp_thick = 6.0
hp_z_offset = 15.0  # Vertical shift from center

# Rods
rod_diameter = 2.5
rod_length = 130.0
rebar_x_offset = 35.0  # Distance of the threaded rod from the center

# --- Modeling ---

# 1. Create the Vertical Plate
# Oriented with thickness along X, width along Y, height along Z
vertical_plate = cq.Workplane("XY").box(vp_thick, vp_width, vp_height)

# 2. Create the Horizontal Plate
# Oriented with length along X, width along Y, thickness along Z
# Shifted vertically to create the intersection shown
horizontal_plate = (
    cq.Workplane("XY")
    .workplane(offset=hp_z_offset)
    .box(hp_length, hp_width, hp_thick)
)

# 3. Create the Smooth Rod
# Located on the face of the vertical plate (+X face)
# Calculated position: half plate thickness + half rod diameter
smooth_rod_pos_x = (vp_thick / 2.0) + (rod_diameter / 2.0)

smooth_rod = (
    cq.Workplane("XY")
    .center(smooth_rod_pos_x, 0)
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
    .translate((0, 0, -rod_length / 2.0))  # Center rod vertically
)

# 4. Create the Threaded Rod / Rebar
# Located further along the X axis, passing through the horizontal plate
rebar_rod = (
    cq.Workplane("XY")
    .center(rebar_x_offset, 0)
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
    .translate((0, 0, -rod_length / 2.0))  # Center rod vertically
)

# --- Assembly ---
# Combine all geometries into a single solid
result = (
    vertical_plate
    .union(horizontal_plate)
    .union(smooth_rod)
    .union(rebar_rod)
)