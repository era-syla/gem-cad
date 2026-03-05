import cadquery as cq
import math

# Parameters
R_p = 10           # Pivot radius
H = 8              # Thickness/height
arm_th = 8         # Arm cross-section thickness
arm_len = 62       # Arm length
boss_r = 8         # End boss radius
r_h = 4            # Hole radius

# Compute arm angle and end positions
theta_rad = math.atan2(15, 60)
theta_deg = math.degrees(theta_rad)
x_end = arm_len * math.sin(theta_rad)
y_end = -arm_len * math.cos(theta_rad)

# Pivot cylinder
result = cq.Workplane("XY").circle(R_p).extrude(H)

# Left arm
left_arm = (
    cq.Workplane("XY")
    .box(arm_th, arm_len, H, centered=(True, False, False))
    .rotate((0, 0, 0), (0, 0, 1), 180)
    .rotate((0, 0, 0), (0, 0, 1), theta_deg)
)
result = result.union(left_arm)

# Right arm
right_arm = (
    cq.Workplane("XY")
    .box(arm_th, arm_len, H, centered=(True, False, False))
    .rotate((0, 0, 0), (0, 0, 1), 180)
    .rotate((0, 0, 0), (0, 0, 1), -theta_deg)
)
result = result.union(right_arm)

# End bosses
left_boss = cq.Workplane("XY").center(x_end, y_end).circle(boss_r).extrude(H)
right_boss = cq.Workplane("XY").center(-x_end, y_end).circle(boss_r).extrude(H)
result = result.union(left_boss).union(right_boss)

# Triangular web between arms
tri_web = (
    cq.Workplane("XY")
    .polyline([(0, 0), (x_end, y_end), (-x_end, y_end)])
    .close()
    .extrude(H)
)
result = result.union(tri_web)

# Drill through holes in pivot and end bosses
hole_pts = [(0, 0), (x_end, y_end), (-x_end, y_end)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_pts)
    .circle(r_h)
    .cutThruAll()
)