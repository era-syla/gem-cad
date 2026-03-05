import cadquery as cq
import math

# --- Parameters ---
# Plate dimensions
length = 300.0
height = 120.0
thickness = 6.0
fillet_radius = 5.0

# Feature Dimensions
csk_hole_dia = 5.0
csk_head_dia = 10.0
csk_angle = 82.0

# Positions
top_row_y = (height / 2.0) - 12.0
# Irregular spacing for top row based on visual estimation:
# Center, mid-sides, far-sides
top_hole_x_positions = [-135, -70, 0, 70, 135]

# Center Feature (Pilot + 4 holes in cross pattern)
center_pos = (0, -5.0)
center_pilot_dia = 8.0
center_mount_dia = 3.5
center_mount_radius = 12.0

# Bottom Left Feature (Pilot + 8 holes in circle)
bl_pos = (-110.0, -35.0)
bl_pilot_dia = 8.0
bl_mount_dia = 3.0
bl_radius = 12.0
bl_count = 8

# Right Side Feature (Single hole)
right_hole_pos = (135.0, -10.0)

# --- Modeling ---

# 1. Create the base plate with filleted corners
result = (
    cq.Workplane("XY")
    .box(length, height, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Add Top Row Countersunk Holes
top_hole_pts = [(x, top_row_y) for x in top_hole_x_positions]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(top_hole_pts)
    .cskHole(csk_hole_dia, csk_head_dia, csk_angle)
)

# 3. Add Center Feature
# 3a. Central Pilot Hole
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([center_pos])
    .hole(center_pilot_dia)
)

# 3b. Surrounding 4 holes (Cross/+ pattern)
center_mount_pts = [
    (center_pos[0], center_pos[1] + center_mount_radius),      # Top
    (center_pos[0] + center_mount_radius, center_pos[1]),      # Right
    (center_pos[0], center_pos[1] - center_mount_radius),      # Bottom
    (center_pos[0] - center_mount_radius, center_pos[1]),      # Left
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(center_mount_pts)
    .hole(center_mount_dia)
)

# 4. Add Bottom Left Feature
# 4a. Central Pilot Hole
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([bl_pos])
    .hole(bl_pilot_dia)
)

# 4b. Surrounding 8 holes (Circular pattern)
bl_mount_pts = []
for i in range(bl_count):
    angle = math.radians(i * (360.0 / bl_count))
    px = bl_pos[0] + bl_radius * math.cos(angle)
    py = bl_pos[1] + bl_radius * math.sin(angle)
    bl_mount_pts.append((px, py))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(bl_mount_pts)
    .hole(bl_mount_dia)
)

# 5. Add Right Side Hole
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([right_hole_pos])
    .cskHole(csk_hole_dia, csk_head_dia, csk_angle)
)