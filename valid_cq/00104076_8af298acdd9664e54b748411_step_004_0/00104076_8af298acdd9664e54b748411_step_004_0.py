import cadquery as cq

# Parametric dimensions
# Central Hub
hub_length = 12.0
hub_width = 12.0
hub_height = 6.0
hole_diameter = 5.0

# Left Arm (Wider)
left_arm_length = 45.0
left_arm_width = 9.0
left_arm_height = 3.0

# Right Arm (Narrower)
right_arm_length = 60.0
right_arm_width = 5.0
right_arm_height = 3.0

# 1. Create the central hub
hub = cq.Workplane("XY").box(hub_length, hub_width, hub_height)

# 2. Create the left arm
# Calculate center position: offset by half of hub length and half of arm length
left_arm_center = -(hub_length / 2 + left_arm_length / 2)
left_arm = (
    cq.Workplane("XY")
    .center(left_arm_center, 0)
    .box(left_arm_length, left_arm_width, left_arm_height)
)

# 3. Create the right arm
right_arm_center = (hub_length / 2 + right_arm_length / 2)
right_arm = (
    cq.Workplane("XY")
    .center(right_arm_center, 0)
    .box(right_arm_length, right_arm_width, right_arm_height)
)

# 4. Combine all parts into a single solid
solid = hub.union(left_arm).union(right_arm)

# 5. Create the hole through the center hub
result = (
    solid
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)