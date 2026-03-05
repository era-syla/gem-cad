import cadquery as cq

# Define some parameters
arm_length = 100
arm_width = 15
center_width = 20
motor_hole_diameter = 5

# Create one arm of the quadcopter
arm = (
    cq.Workplane("XY")
    .box(arm_length, arm_width, 5)
    .faces(">Z")
    .workplane()
    .center(-arm_length/2 + center_width/2, 0)
    .circle(motor_hole_diameter/2)
    .cutThruAll()
)

# Create the center piece of the quadcopter
center = cq.Workplane("XY").box(center_width, center_width, 5)

# Union the arm and center
quad_with_one_arm = center.union(arm)

# Create the full quadcopter by rotating and copying the arm
result = quad_with_one_arm
for i in range(1, 4):
    result = result.union(arm.rotate((0, 0, 0), (0, 0, 1), i * 90))