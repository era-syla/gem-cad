import cadquery as cq

# Parameters
body_length = 50.0
body_width = 30.0
body_height = 10.0
arm_length = 60.0
arm_radius_base = 5.0
arm_radius_tip = 2.0
shoulder_radius = 8.0
shoulder_height = 12.0

# Body
body = cq.Workplane("XY").box(body_length, body_width, body_height)

# Shoulder
shoulder = cq.Workplane("XY").center(body_length / 2, 0).cylinder(shoulder_height, shoulder_radius)
body = body.union(shoulder)

# Arm
arm = cq.Workplane("YZ").center(0, body_height / 2).circle(arm_radius_base).workplane(offset=arm_length).circle(arm_radius_tip).loft(combine=False)
arm = arm.translate((body_length / 2 + shoulder_radius, 0, body_height / 2))
body = body.union(arm)

# Details
head_radius = 6.0
head = cq.Workplane("XY").center(-body_length / 2, 0).sphere(head_radius)
body = body.union(head)

# Extra details
detail1 = cq.Workplane("XY").center(0, body_width / 2 + 5).box(10, 10, body_height)
detail2 = cq.Workplane("XY").center(0, -body_width / 2 - 5).box(10, 10, body_height)
body = body.union(detail1).union(detail2)

# Floating elements
float1 = cq.Workplane("XY").center(-40, 30).box(15, 8, 5)
float2 = cq.Workplane("XY").center(-40, 20).box(15, 8, 5)

result = body.union(float1).union(float2)