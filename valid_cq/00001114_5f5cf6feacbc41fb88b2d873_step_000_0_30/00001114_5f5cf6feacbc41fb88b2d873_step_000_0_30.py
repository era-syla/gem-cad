import cadquery as cq

# --- Parameters ---
height = 28.0           # Total height of the part
web_thickness = 5.0     # Thickness of the connecting web (top plate)
wall_thickness = 3.0    # Thickness of the vertical walls
fillet_radius_out = 4.0
fillet_radius_in = 3.0

# Boss dimensions
center_od = 30.0
center_id = 20.0
arm_od = 22.0
arm_id = 14.0

# Geometry layout
arm_x = 55.0
arm_y = -30.0
small_hole_offset_x = 8.0
small_hole_offset_y = -12.0
small_hole_dia = 3.0

# Points
p_center = (0, 0)
p_left = (-arm_x, arm_y)
p_right = (arm_x, arm_y)

# --- Step 1: Create the Main Solid Body ---
# Left arm: loft-like approach using union of circles
left_c1 = cq.Workplane("XY").circle(center_od/2.0).extrude(height)
left_c2 = cq.Workplane("XY").center(*p_left).circle(arm_od/2.0).extrude(height)
# Connect them with a box
import math
dx = p_left[0] - p_center[0]
dy = p_left[1] - p_center[1]
angle_l = math.degrees(math.atan2(dy, dx))
dist_l = math.hypot(dx, dy)
left_bar = (
    cq.Workplane("XY")
    .center(p_center[0] + dx/2, p_center[1] + dy/2)
    .rect(dist_l, min(center_od, arm_od) * 0.8)
    .extrude(height)
    .rotate((0, 0, 0), (0, 0, 1), angle_l)
)
left_arm_solid = left_c1.union(left_c2).union(left_bar)

right_c2 = cq.Workplane("XY").center(*p_right).circle(arm_od/2.0).extrude(height)
dx2 = p_right[0] - p_center[0]
dy2 = p_right[1] - p_center[1]
angle_r = math.degrees(math.atan2(dy2, dx2))
dist_r = math.hypot(dx2, dy2)
right_bar = (
    cq.Workplane("XY")
    .center(p_center[0] + dx2/2, p_center[1] + dy2/2)
    .rect(dist_r, min(center_od, arm_od) * 0.8)
    .extrude(height)
    .rotate((0, 0, 0), (0, 0, 1), angle_r)
)
right_arm_solid = left_c1.union(right_c2).union(right_bar)

main_body = left_arm_solid.union(right_arm_solid)

# Fillet vertical edges
try:
    main_body = main_body.edges("|Z").fillet(fillet_radius_out)
except:
    pass

# --- Step 2: Create the Internal Void (Pocket) ---
pocket_height = height - web_thickness

# Void circles (smaller by wall_thickness)
r_void_center = (center_od / 2.0) - wall_thickness
r_void_arm = (arm_od / 2.0) - wall_thickness

left_void_c1 = cq.Workplane("XY").circle(r_void_center).extrude(pocket_height)
left_void_c2 = cq.Workplane("XY").center(*p_left).circle(r_void_arm).extrude(pocket_height)
left_void_bar = (
    cq.Workplane("XY")
    .center(p_center[0] + dx/2, p_center[1] + dy/2)
    .rect(dist_l, min(r_void_center, r_void_arm) * 2 * 0.8)
    .extrude(pocket_height)
    .rotate((0, 0, 0), (0, 0, 1), angle_l)
)
left_void = left_void_c1.union(left_void_c2).union(left_void_bar)

right_void_c2 = cq.Workplane("XY").center(*p_right).circle(r_void_arm).extrude(pocket_height)
right_void_bar = (
    cq.Workplane("XY")
    .center(p_center[0] + dx2/2, p_center[1] + dy2/2)
    .rect(dist_r, min(r_void_center, r_void_arm) * 2 * 0.8)
    .extrude(pocket_height)
    .rotate((0, 0, 0), (0, 0, 1), angle_r)
)
right_void = left_void_c1.union(right_void_c2).union(right_void_bar)

void_volume = left_void.union(right_void)

# Boss Protectors
boss_protectors = (
    cq.Workplane("XY")
    .circle(center_od/2.0)
    .extrude(height)
)
bp_left = cq.Workplane("XY").center(*p_left).circle(arm_od/2.0).extrude(height)
bp_right = cq.Workplane("XY").center(*p_right).circle(arm_od/2.0).extrude(height)
boss_protectors = boss_protectors.union(bp_left).union(bp_right)

cutting_tool = void_volume.cut(boss_protectors)
result = main_body.cut(cutting_tool)

# --- Step 3: Through Holes ---
bore_center = cq.Workplane("XY").circle(center_id/2.0).extrude(height * 2, both=True)
bore_left = cq.Workplane("XY").center(*p_left).circle(arm_id/2.0).extrude(height * 2, both=True)
bore_right = cq.Workplane("XY").center(*p_right).circle(arm_id/2.0).extrude(height * 2, both=True)
result = result.cut(bore_center).cut(bore_left).cut(bore_right)

# --- Step 4: Small Detail Holes ---
sh1 = cq.Workplane("XY").center(small_hole_offset_x, small_hole_offset_y).circle(small_hole_dia/2.0).extrude(height * 2, both=True)
sh2 = cq.Workplane("XY").center(-small_hole_offset_x, small_hole_offset_y).circle(small_hole_dia/2.0).extrude(height * 2, both=True)
result = result.cut(sh1).cut(sh2)
