import cadquery as cq

# Parameters for the main body
body_length = 50.0
body_width = 30.0
body_height = 15.0
front_cyl_radius = 8.0
front_cyl_length = 15.0
side_pod_radius = 12.0
side_pod_offset_y = body_width / 2 + 5
side_pod_offset_x = 10.0

# Parameters for the arm
arm_length1 = 40.0
arm_length2 = 35.0
arm_radius1 = 6.0
arm_radius2 = 4.0
arm_radius3 = 2.0

# Parameters for the small floating parts
float_part_length = 15.0
float_part_width = 6.0
float_part_height = 4.0
float_part_offset_x = -30.0
float_part_offset_y = 20.0
float_part_offset_z = 10.0
float_part_spacing = 8.0

# 1. Main Body
body = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
    .edges("|Z").fillet(3.0)
)

# Front cylinder
front_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=body_length/2)
    .circle(front_cyl_radius)
    .extrude(front_cyl_length)
    .edges(">X").fillet(front_cyl_radius - 0.1)
)
body = body.union(front_cyl)

# Side pods
side_pod1 = (
    cq.Workplane("XY")
    .center(side_pod_offset_x, side_pod_offset_y)
    .cylinder(body_height, side_pod_radius)
)
side_pod1 = side_pod1.faces(">Z").circle(side_pod_radius - 3).cutBlind(-2)

side_pod2 = (
    cq.Workplane("XY")
    .center(side_pod_offset_x, -side_pod_offset_y)
    .cylinder(body_height, side_pod_radius)
)
side_pod2 = side_pod2.faces(">Z").circle(side_pod_radius - 3).cutBlind(-2)

body = body.union(side_pod1).union(side_pod2)

# Top details
top_detail = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2)
    .center(-5, 0)
    .box(20, body_width - 10, 2)
    .edges("|Z").fillet(2.0)
)
body = body.union(top_detail)

# Rear attachment point
rear_attach = (
    cq.Workplane("YZ")
    .workplane(offset=-body_length/2)
    .center(0, 0)
    .box(10, 15, body_height)
)
body = body.union(rear_attach)

# 2. Arm
arm1 = (
    cq.Workplane("YZ")
    .workplane(offset=-body_length/2 - 10)
    .circle(arm_radius1)
    .workplane(offset=-arm_length1)
    .circle(arm_radius2)
    .loft()
)

arm_joint = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(-body_length/2 - 10 - arm_length1, 0)
    .cylinder(arm_radius2*2.5, arm_radius2)
)

arm2 = (
    cq.Workplane("YZ")
    .workplane(offset=-body_length/2 - 10 - arm_length1)
    .circle(arm_radius2)
    .workplane(offset=-arm_length2)
    .circle(arm_radius3)
    .loft()
)

arm_end = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(-body_length/2 - 10 - arm_length1 - arm_length2, 0)
    .cylinder(arm_radius3*2.5, arm_radius3*1.5)
)

arm = arm1.union(arm_joint).union(arm2).union(arm_end)

# 3. Floating Parts
float1 = (
    cq.Workplane("XY")
    .center(float_part_offset_x, float_part_offset_y)
    .workplane(offset=float_part_offset_z)
    .box(float_part_length, float_part_width, float_part_height)
    .edges("|Z").fillet(1.0)
)
float1_detail = (
    cq.Workplane("YZ")
    .workplane(offset=float_part_offset_x + float_part_length/2)
    .center(float_part_offset_z, float_part_offset_y)
    .cylinder(3.0, 1.5)
)
float1 = float1.union(float1_detail)

float2 = (
    cq.Workplane("XY")
    .center(float_part_offset_x, float_part_offset_y)
    .workplane(offset=float_part_offset_z + float_part_spacing)
    .box(float_part_length, float_part_width, float_part_height)
    .edges("|Z").fillet(1.0)
)
float2_detail = (
    cq.Workplane("YZ")
    .workplane(offset=float_part_offset_x + float_part_length/2)
    .center(float_part_offset_z + float_part_spacing, float_part_offset_y)
    .cylinder(3.0, 1.5)
)
float2 = float2.union(float2_detail)

# Combine all parts
result = body.union(arm).union(float1).union(float2)

# Rotate for better alignment to match image perspective
result = result.rotate((0,0,0), (0,0,1), 45).rotate((0,0,0), (1,0,0), -15)