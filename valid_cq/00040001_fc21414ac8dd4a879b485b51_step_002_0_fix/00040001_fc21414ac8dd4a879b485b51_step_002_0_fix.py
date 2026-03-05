import cadquery as cq
import math

# Parameters
arm_thickness = 3.0
arm_width = 8.0
arm_length_left = 50.0
arm_length_right = 60.0
boss_radius = 3.0
boss_height = 2.0
fin_length = 30.0
fin_thickness = 4.0
fin_height = 15.0
angle_deg = 50.0
angle_rad = math.radians(angle_deg)

# Left arm
arm1 = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 0, angle_deg))
    .rect(arm_length_left, arm_width, centered=(False, True))
    .extrude(arm_thickness)
)

# Right arm
arm2 = (
    cq.Workplane("XY")
    .rect(arm_length_right, arm_width, centered=(False, True))
    .extrude(arm_thickness)
)

# Combine arms
result = arm1.union(arm2)

# Add end bosses
# Right boss
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(arm_length_right, 0)])
    .circle(boss_radius)
    .extrude(boss_height)
)
# Left boss
x_l = arm_length_left * math.cos(angle_rad)
y_l = arm_length_left * math.sin(angle_rad)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x_l, y_l)])
    .circle(boss_radius)
    .extrude(boss_height)
)

# Add central fin on the horizontal arm
x_f = arm_length_right / 2
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x_f, 0)])
    .rect(fin_length, fin_thickness, centered=(True, True))
    .extrude(fin_height)
)

# Add embossed text on left arm
t_dist = arm_length_left * 0.2
x_t = (arm_length_left - t_dist) * math.cos(angle_rad)
y_t = (arm_length_left - t_dist) * math.sin(angle_rad)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x_t, y_t)])
    .text("50/60", 2.0, 1.0)
)

# Add embossed text on right arm
x_t2 = arm_length_right * 0.2
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(x_t2, 0)])
    .text("20°", 2.0, 1.0)
)