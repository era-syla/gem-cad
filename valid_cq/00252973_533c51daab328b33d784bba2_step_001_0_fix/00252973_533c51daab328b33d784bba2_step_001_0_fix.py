import cadquery as cq

# Torso
torso = cq.Workplane("XY").rect(20, 30).extrude(40)

# Neck
neck = cq.Workplane("XY").cylinder(8, 3).translate((0, 0, 44))

# Head
head = cq.Workplane("XY").sphere(10).translate((0, 0, 54))

# Left Arm
left_arm = (
    cq.Workplane("XY")
    .cylinder(30, 3)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((15, 0, 35))
)

# Right Arm
right_arm = (
    cq.Workplane("XY")
    .cylinder(30, 3)
    .rotate((0, 0, 0), (0, 1, 0), -90)
    .translate((-15, 0, 35))
)

# Left Leg
left_leg = cq.Workplane("XY").cylinder(30, 4).translate((7, 0, 15))

# Right Leg
right_leg = cq.Workplane("XY").cylinder(30, 4).translate((-7, 0, 15))

# Combine all parts
result = (
    torso
    .union(neck)
    .union(head)
    .union(left_arm)
    .union(right_arm)
    .union(left_leg)
    .union(right_leg)
)