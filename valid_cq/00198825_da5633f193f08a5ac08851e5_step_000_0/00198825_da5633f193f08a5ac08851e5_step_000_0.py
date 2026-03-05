import cadquery as cq

# --- Parameters ---
# Base dimensions
base_diameter = 80.0
base_thickness = 4.0

# Tube dimensions
tube_od = 26.0
tube_id = 20.0
tube_height = 90.0

# Vertical slot dimensions (Upper feature)
v_slot_width = 10.0
v_slot_length_total = 60.0  # Total length from top arc to bottom arc
v_slot_top_margin = 8.0     # Distance from the top rim of the tube

# Horizontal slot dimensions (Lower feature)
h_slot_width_total = 18.0
h_slot_height = 8.0
h_slot_bottom_margin = 8.0  # Distance from the top of the base

# --- Geometry Construction ---

# 1. Create the Base
# A simple cylinder on the XY plane
base = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_thickness)

# 2. Create the Tube
# A hollow pipe centered on the base. 
# We start the sketch on top of the base (offset=base_thickness).
tube = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(tube_od / 2.0)
    .circle(tube_id / 2.0)
    .extrude(tube_height)
)

# Union the base and tube into a single solid
main_body = base.union(tube)

# --- Cuts ---

# Calculate Z positions for the slots
# Vertical Slot: Calculate center Z based on top margin and length
v_slot_z_top = base_thickness + tube_height - v_slot_top_margin
v_slot_z_center = v_slot_z_top - (v_slot_length_total / 2.0)
v_slot_c2c = v_slot_length_total - v_slot_width # Center-to-center length for slot2D

# Horizontal Slot: Calculate center Z based on bottom margin and height
h_slot_z_bottom = base_thickness + h_slot_bottom_margin
h_slot_z_center = h_slot_z_bottom + (h_slot_height / 2.0)
h_slot_c2c = h_slot_width_total - h_slot_height # Center-to-center length for slot2D

# Cut Depth
# We need to cut through the front wall (thickness ~3mm) but not damage the back wall.
# Safe depth is slightly more than wall thickness.
cut_depth = (tube_od - tube_id) / 2.0 + 5.0

# Create a workplane tangent to the front of the tube
# We use the XZ plane (normal Y) offset by the tube radius to place it on the surface.
cut_plane = cq.Workplane("XZ").workplane(offset=tube_od / 2.0)

# Perform the cuts
# We use separate cut operations to keep the logic clean, though they could be chained.

# 1. Vertical Slot Cut
result = main_body.cut(
    cut_plane.center(0, v_slot_z_center)
    .slot2D(v_slot_c2c, v_slot_width, 90) # 90 degrees for vertical orientation
    .extrude(-cut_depth) # Extrude negative to cut into the object
)

# 2. Horizontal Slot Cut
# We define a new plane/center to avoid relative coordinate confusion
cut_plane_lower = cq.Workplane("XZ").workplane(offset=tube_od / 2.0)

result = result.cut(
    cut_plane_lower.center(0, h_slot_z_center)
    .slot2D(h_slot_c2c, h_slot_height, 0) # 0 degrees for horizontal orientation
    .extrude(-cut_depth)
)