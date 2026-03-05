import cadquery as cq

# --- Parametric Dimensions ---
# Left section (Fins)
fin_width = 25.0
fin_height = 40.0
fin_thick = 2.0
fin_gap = 12.0
num_fins = 4

# Middle section (Carriage)
mid_plate_w = 40.0
mid_plate_l = 30.0

# Right section (Rails)
rail_len = 100.0
rail_height = 45.0
rail_thick = 2.0
rail_y_offset = -15.0

# Top strips
strip_height = 6.0
strip_spacing = 8.0

# Wedges
wedge_len = 60.0
wedge_height = 25.0

# --- Geometry Construction ---

# 1. Left Group: Vertical Fins
# Base shape for the fin
fin_shape = cq.Workplane("YZ").rect(fin_width, fin_height).extrude(fin_thick)

# Create the array of fins
left_group = fin_shape
for i in range(1, num_fins):
    # Shift along X axis
    offset_fin = fin_shape.translate((i * (fin_thick + fin_gap), 0, 0))
    left_group = left_group.union(offset_fin)

# Add a horizontal guide rail running through/near the fins
guide_rail = cq.Workplane("XY").rect(num_fins * (fin_thick + fin_gap) + 20, 5).extrude(2)
guide_rail = guide_rail.translate((30, 0, -fin_height/2 + 5))
left_group = left_group.union(guide_rail)


# 2. Middle Group: Carriage Assembly
# Located after the fins
mid_start_x = num_fins * (fin_thick + fin_gap) + 10
mid_base = cq.Workplane("XY").rect(mid_plate_l, mid_plate_w).extrude(2)
mid_base = mid_base.translate((mid_start_x + mid_plate_l/2, 0, 0))

# Add small vertical tabs to the middle assembly
tab = cq.Workplane("YZ").rect(mid_plate_w * 0.8, 10).extrude(2)
tab1 = tab.translate((mid_start_x + 10, 0, 8))
tab2 = tab.translate((mid_start_x + 20, 0, 8))

mid_group = mid_base.union(tab1).union(tab2)


# 3. Right Group: Long Rails
# Located after the middle section
rail_start_x = mid_start_x + mid_plate_l + 10

# Main rail plate
rail1 = cq.Workplane("XZ").rect(rail_len, rail_height).extrude(rail_thick)
rail1 = rail1.translate((rail_start_x + rail_len/2, rail_y_offset, 0))

# Secondary rail plate (behind)
rail2 = cq.Workplane("XZ").rect(rail_len, rail_height).extrude(rail_thick)
rail2 = rail2.translate((rail_start_x + rail_len/2, rail_y_offset - 5, 0))

right_group = rail1.union(rail2)


# 4. Top Group: Thin Strips
# Located above the right rails
strips_group = cq.Workplane("XZ") # Placeholder

for i in range(3):
    strip = cq.Workplane("XZ").rect(rail_len, strip_height).extrude(rail_thick)
    z_pos = rail_height/2 + 10 + (i * (strip_height + strip_spacing))
    strip = strip.translate((rail_start_x + rail_len/2, rail_y_offset, z_pos))
    
    if i == 0:
        strips_group = strip
    else:
        strips_group = strips_group.union(strip)


# 5. Far Right Group: Wedges
# Triangular ramps
wedge_start_x = rail_start_x + rail_len + 15

# Define triangle points (ramp up to the right)
pts = [(0, 0), (wedge_len, wedge_height), (wedge_len, 0)]
wedge_shape = cq.Workplane("XZ").polyline(pts).close().extrude(rail_thick)

# Lower wedge
wedge1 = wedge_shape.translate((wedge_start_x, rail_y_offset, -10))
# Upper wedge
wedge2 = wedge_shape.translate((wedge_start_x, rail_y_offset, 20))

wedges_group = wedge1.union(wedge2)


# --- Final Assembly ---
result = left_group.union(mid_group).union(right_group).union(strips_group).union(wedges_group)