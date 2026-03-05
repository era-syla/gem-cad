import cadquery as cq

# ==========================================
# Parametric Dimensions
# ==========================================
# Base Plate
plate_length = 300.0
plate_width = 200.0
plate_thickness = 3.0
corner_radius = 4.0

# Feature Clusters (4 quadrants)
cluster_offset_x = 75.0  # Distance from center X
cluster_offset_y = 50.0  # Distance from center Y

# Connector Slots
slot_length = 70.0
slot_width = 5.0

# Tab Cutouts (Small rectangular openings)
tab_length = 15.0
tab_width = 10.0
tab_offset_y = 20.0  # Offset from slot center towards plate center

# Edge Notch (Right side)
notch_depth = 12.0
notch_length = 35.0
notch_y_pos = -30.0  # Offset from center Y along the edge

# Holes
hole_diameter = 4.0
hole_points = []

# ==========================================
# 3D Modeling Process
# ==========================================

# 1. Create Base Plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Fillet Corners
result = result.edges("|Z").fillet(corner_radius)

# 3. Create Edge Notch
# Tool to cut the notch on the +X edge
notch_tool = (
    cq.Workplane("XY")
    .moveTo(plate_length / 2, notch_y_pos)
    .rect(notch_depth * 2, notch_length)  # Width doubled to ensure clean edge cut
    .extrude(plate_thickness * 2)
    .translate((0, 0, -plate_thickness))
)
result = result.cut(notch_tool)

# 4. Generate Feature Clusters
# We iterate through the four quadrants to place slots and tab cutouts
quadrants = [
    (1, 1),   # Top-Right
    (-1, 1),  # Top-Left
    (-1, -1), # Bottom-Left
    (1, -1)   # Bottom-Right
]

for qx, qy in quadrants:
    # Center of the cluster
    cx = qx * cluster_offset_x
    cy = qy * cluster_offset_y
    
    # A. Cut Main Connector Slot
    result = (
        result.faces(">Z")
        .workplane()
        .moveTo(cx, cy)
        .rect(slot_length, slot_width)
        .cutThruAll()
    )
    
    # B. Cut Tab Cutout
    # Positioned "inward" towards the X-axis (center of plate)
    # If qy is positive (top), we subtract offset. If qy is negative (bottom), we add offset.
    inner_dir = -1 if qy > 0 else 1
    tx = cx
    ty = cy + (inner_dir * tab_offset_y)
    
    result = (
        result.faces(">Z")
        .workplane()
        .moveTo(tx, ty)
        .rect(tab_length, tab_width)
        .cutThruAll()
    )
    
    # C. Collect Hole Points for this cluster
    # Flanking holes (ends of slot)
    hole_points.append((cx - slot_length/2 - 8, cy))
    hole_points.append((cx + slot_length/2 + 8, cy))
    
    # Hole near the tab cutout (inward side)
    hole_points.append((cx, cy + (inner_dir * (tab_offset_y + 15))))
    
    # Hole on the outer side of the slot
    hole_points.append((cx, cy - (inner_dir * 15)))

# 5. Add Global Mounting Holes
# Perimeter Corners
px = plate_length / 2 - 10
py = plate_width / 2 - 10
hole_points.extend([
    (px, py), (-px, py), (-px, -py), (px, -py)
])

# Mid-edge holes
hole_points.extend([
    (0, py), (0, -py)
])

# Center holes
hole_points.extend([
    (0, 0),
    (-plate_length/4, 0),
    (plate_length/4, 0)
])

# 6. Drill All Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)