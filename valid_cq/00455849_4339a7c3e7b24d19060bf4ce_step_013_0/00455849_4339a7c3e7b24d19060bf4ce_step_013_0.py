import cadquery as cq

# --- Parametric Dimensions ---
rod_dia = 6.0             # Diameter of the rods
rod_len_long = 300.0      # Length of the top and bottom rods
rod_len_short = 120.0     # Length of the middle rod
rod_spacing = 25.0        # Center-to-center spacing between rods

nut_hex_dia = 12.0        # Circumscribed diameter of the hex nut
nut_thickness = 8.0       # Thickness of the nut
nut_pos_ratio = 0.5       # Position of the nut along the rod (0.0 to 1.0)

# --- Geometry Construction ---

# 1. Top Rod (Long)
# Created on YZ plane and extruded along X axis
# Translated in +Y direction
top_rod = (
    cq.Workplane("YZ")
    .circle(rod_dia / 2.0)
    .extrude(rod_len_long)
    .translate((0, rod_spacing, 0))
)

# 2. Middle Rod (Short)
# Centered longitudinally relative to the long rods
# Located at Y = 0
start_offset_short = (rod_len_long - rod_len_short) / 2.0
middle_rod = (
    cq.Workplane("YZ")
    .workplane(offset=start_offset_short)
    .circle(rod_dia / 2.0)
    .extrude(rod_len_short)
)

# 3. Bottom Rod (Long with Nut)
# Located at Y = -rod_spacing

# Base cylinder
bottom_rod_shaft = (
    cq.Workplane("YZ")
    .circle(rod_dia / 2.0)
    .extrude(rod_len_long)
)

# Hex Nut Feature
# Positioned based on ratio along the rod length
nut_x_loc = rod_len_long * nut_pos_ratio
nut_feature = (
    cq.Workplane("YZ")
    .workplane(offset=nut_x_loc - nut_thickness / 2.0)
    .polygon(6, nut_hex_dia)
    .extrude(nut_thickness)
)

# Combine shaft and nut, then position
bottom_rod = bottom_rod_shaft.union(nut_feature).translate((0, -rod_spacing, 0))

# --- Final Result ---
# Combine all three disjoint solids into one compound object
result = top_rod.union(middle_rod).union(bottom_rod)