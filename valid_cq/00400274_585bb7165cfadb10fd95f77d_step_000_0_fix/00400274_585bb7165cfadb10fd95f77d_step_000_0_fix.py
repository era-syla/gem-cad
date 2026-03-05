import cadquery as cq

# Parameters for the arm
arm_length = 100
arm_width = 20
arm_height = 5
arm_radius = 10
mount_radius = 5

# Parameters for the central body
center_length = 50
center_width = 30
center_height = 5

# Create one arm
arm = (
    cq.Workplane("XY")
    .circle(arm_radius)
    .extrude(arm_height)
    .faces(">Z")
    .workplane()
    .center(arm_radius, 0)
    .rect(arm_length, arm_width)
    .extrude(arm_height)
    .edges("|Z")
    .fillet(2)
)

# Create a mount for the motor
mount = (
    cq.Workplane("XY")
    .circle(mount_radius)
    .extrude(arm_height)
)

# Position the mount on the arm
arm_with_mount = arm.union(mount.translate((arm_length - arm_radius * 2, 0, 0)))

# Assemble the 4 arms in a cross pattern
arms = (
    arm_with_mount
    .rotate((0, 0, 1), (0, 0, 0), 90)
    .union(arm_with_mount.rotate((0, 0, 1), (0, 0, 0), 180))
    .union(arm_with_mount.rotate((0, 0, 1), (0, 0, 0), 270))
)

# Create the central body
center = (
    cq.Workplane("XY")
    .rect(center_length, center_width)
    .extrude(center_height)
    .edges("|Z")
    .fillet(3)
)

# Assemble the drone frame with body and arms
result = arms.union(center)

result