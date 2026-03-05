import cadquery as cq

# Define the main body dimensions
main_length = 100
main_width = 10
main_height = 5

# Create the main body
main_body = cq.Workplane("XY").box(main_length, main_width, main_height)

# Define the arm dimensions
arm_length = 90
arm_width = 6
arm_height = 2

# Create the arm
arm = cq.Workplane("XY").box(arm_length, arm_width, arm_height)

# Position the arm on the main body
arm = arm.translate((10, 0, 5))

# Define the axle dimensions
axle_diameter = 4
axle_length = 6

# Create the axle
axle = cq.Workplane("XY").circle(axle_diameter / 2).extrude(axle_length)

# Position the axle
axle = axle.translate((95, 0, 6))

# Assemble the parts
result = main_body.union(arm).union(axle)