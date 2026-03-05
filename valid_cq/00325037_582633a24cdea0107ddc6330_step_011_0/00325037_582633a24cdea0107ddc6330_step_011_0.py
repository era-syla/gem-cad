import cadquery as cq

# --- Parameters ---
length = 200.0
height = 100.0
thickness = 3.0

# Edge / Finger Joint Parameters
# The pattern consists of alternating notches and tabs.
# We assume the corners are notches (cutouts).
n_tabs_horizontal = 3  # Number of tabs along top/bottom edges
n_tabs_vertical = 3    # Number of tabs along left/right edges
notch_depth = 3.0      # Depth of the edge cuts (usually material thickness)

# Slot Parameters
slot_width = 3.0
slot_height = 15.0
slot_margin_x = 15.0   # Distance from the vertical edge to slot center

# Hole Parameters
hole_diameter = 3.2
hole_spacing = 10.0    # Spacing between holes in the 2x2 grid
hole_group_margin_x = 35.0  # X distance from edge to grid center
hole_group_margin_y = 25.0  # Y distance from bottom edge to grid center

# --- Helper Logic ---

def get_pattern_geometry(total_length, n_tabs):
    """
    Calculates segment length and center positions for notches and tabs.
    Assumes a pattern: Notch-Tab-Notch...-Tab-Notch.
    Total segments = 2 * n_tabs + 1.
    Returns: segment_length, list_of_notch_centers, list_of_tab_centers
    """
    n_segments = 2 * n_tabs + 1
    seg_len = total_length / n_segments
    
    # Notches are at indices 0, 2, 4...
    notch_centers = [
        -total_length/2.0 + (i + 0.5) * seg_len 
        for i in range(0, n_segments, 2)
    ]
    
    # Tabs are at indices 1, 3, 5...
    tab_centers = [
        -total_length/2.0 + (i + 0.5) * seg_len 
        for i in range(1, n_segments, 2)
    ]
    
    return seg_len, notch_centers, tab_centers

# --- Model Generation ---

# 1. Base Plate
result = cq.Workplane("XY").box(length, height, thickness)

# 2. Horizontal Edge Notches (Top and Bottom)
seg_len_h, notches_h, tabs_h = get_pattern_geometry(length, n_tabs_horizontal)

for x in notches_h:
    # Cut Top
    result = result.cut(
        cq.Workplane("XY")
        .center(x, height/2.0)
        .box(seg_len_h, notch_depth * 2, thickness)
    )
    # Cut Bottom
    result = result.cut(
        cq.Workplane("XY")
        .center(x, -height/2.0)
        .box(seg_len_h, notch_depth * 2, thickness)
    )

# 3. Vertical Edge Notches (Left and Right)
seg_len_v, notches_v, tabs_v = get_pattern_geometry(height, n_tabs_vertical)

for y in notches_v:
    # Cut Right
    result = result.cut(
        cq.Workplane("XY")
        .center(length/2.0, y)
        .box(notch_depth * 2, seg_len_v, thickness)
    )
    # Cut Left
    result = result.cut(
        cq.Workplane("XY")
        .center(-length/2.0, y)
        .box(notch_depth * 2, seg_len_v, thickness)
    )

# 4. Vertical Slots
# Slots are positioned vertically aligned with the solid 'tabs' of the side edges.
# Left side slots
left_slot_points = [(-length/2.0 + slot_margin_x, y) for y in tabs_v]
# Right side slots
right_slot_points = [(length/2.0 - slot_margin_x, y) for y in tabs_v]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(left_slot_points + right_slot_points)
    .rect(slot_width, slot_height)
    .cutThruAll()
)

# 5. Mounting Holes (2x2 Grids)
def get_grid_points(cx, cy, spacing):
    offsets = [-spacing/2.0, spacing/2.0]
    return [(cx + dx, cy + dy) for dx in offsets for dy in offsets]

# Bottom Left Group
bl_center_x = -length/2.0 + hole_group_margin_x
bl_center_y = -height/2.0 + hole_group_margin_y
bl_points = get_grid_points(bl_center_x, bl_center_y, hole_spacing)

# Bottom Right Group
br_center_x = length/2.0 - hole_group_margin_x
br_center_y = -height/2.0 + hole_group_margin_y
br_points = get_grid_points(br_center_x, br_center_y, hole_spacing)

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(bl_points + br_points)
    .circle(hole_diameter/2.0)
    .cutThruAll()
)