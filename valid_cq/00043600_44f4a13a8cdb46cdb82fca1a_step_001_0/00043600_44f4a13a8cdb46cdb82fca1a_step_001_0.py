import cadquery as cq

# --- Parameters ---
thickness = 2.0
width_scale = 1.0
height_scale = 1.0

# --- 1. Main Body Geometry ---
# Creating the jagged, shield-like shape using a polyline.
# Coordinates are estimated based on the proportions of the symbol.

# Top points
p_top_mid = (0, 45)
p_top_right = (45, 40)
p_top_left = (-45, 40)

# Right side spikes (Zig-zag pattern)
p_r_s1_tip = (60, 25)
p_r_s1_val = (40, 15)
p_r_s2_tip = (55, 5)
p_r_s2_val = (35, -5)
p_r_s3_tip = (50, -20)
p_r_s3_val = (12, -32)  # Connection point to stem

# Left side spikes (Mirrored X coordinates)
p_l_s3_val = (-12, -32)
p_l_s3_tip = (-50, -20)
p_l_s2_val = (-35, -5)
p_l_s2_tip = (-55, 5)
p_l_s1_val = (-40, 15)
p_l_s1_tip = (-60, 25)

# Ordered list of vertices for the polygon
pts_body = [
    p_top_mid,
    p_top_left,
    p_l_s1_tip, p_l_s1_val,
    p_l_s2_tip, p_l_s2_val,
    p_l_s3_tip, p_l_s3_val,
    p_r_s3_val, p_r_s3_tip,
    p_r_s2_val, p_r_s2_tip,
    p_r_s1_val, p_r_s1_tip,
    p_top_right
]

# Create the main solid
main_body = cq.Workplane("XY").polyline(pts_body).close().extrude(thickness)

# --- 2. Bottom Symbol Detail ---
# Consists of a connecting stem, a ring, and a bottom 'anchor' or horn shape.

# Connecting Stem
stem = (
    cq.Workplane("XY")
    .rect(24, 15)
    .extrude(thickness)
    .translate((0, -35, 0))
)

# Ring Parameters
ring_cy = -45
ring_or = 12
ring_ir = 7

# Create Ring Outer Solid
ring_solid = (
    cq.Workplane("XY")
    .moveTo(0, ring_cy)
    .circle(ring_or)
    .extrude(thickness)
)

# Create Ring Inner Cylinder (for cutting later)
ring_cut_tool = (
    cq.Workplane("XY")
    .moveTo(0, ring_cy)
    .circle(ring_ir)
    .extrude(thickness)
)

# Anchor/Horns Shape
# Modeled as a polygon attached to the bottom of the ring
anchor_pts = [
    (0, ring_cy - 5),         # Top center (hidden inside ring)
    (-6, ring_cy - 3),        # Left shoulder
    (-18, ring_cy - 14),      # Left Tip
    (-10, ring_cy - 8),       # Left valley
    (0, ring_cy - 10),        # Bottom center
    (10, ring_cy - 8),        # Right valley
    (18, ring_cy - 14),       # Right Tip
    (6, ring_cy - 3)          # Right shoulder
]

anchor = cq.Workplane("XY").polyline(anchor_pts).close().extrude(thickness)

# Combine bottom parts and cut the hole
# Note: We union first, then cut the hole to ensure the anchor doesn't block the hole
bottom_assembly = (
    stem
    .union(ring_solid)
    .union(anchor)
    .cut(ring_cut_tool)
)

# --- 3. Forehead Slot ---
# A curved arc cutout near the top of the shape.

slot_center = (0, -10)
slot_radius = 42
slot_width = 5
slot_arc_limit_h = 30
slot_arc_limit_w = 65

# Create a ring for the slot
slot_outer = (
    cq.Workplane("XY")
    .moveTo(*slot_center)
    .circle(slot_radius + slot_width/2)
    .extrude(thickness)
)
slot_inner = (
    cq.Workplane("XY")
    .moveTo(*slot_center)
    .circle(slot_radius - slot_width/2)
    .extrude(thickness)
)
slot_ring_full = slot_outer.cut(slot_inner)

# Create a bounding box to limit the ring to just the top arc segment
# Positioned at the apex of the arc
slot_limit_box = (
    cq.Workplane("XY")
    .rect(slot_arc_limit_w, slot_arc_limit_h)
    .extrude(thickness)
    .translate((0, slot_center[1] + slot_radius, 0))
)

slot_shape = slot_ring_full.intersect(slot_limit_box)

# --- 4. Final Assembly ---
result = (
    main_body
    .union(bottom_assembly)
    .cut(slot_shape)
)

# Export (Optional usage)
# cq.exporters.export(result, "blood_seal.stl")