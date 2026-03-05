import cadquery as cq

# Parametric dimensions
body_length = 70
body_width = 50
body_height = 25
fillet_radius = 10

# Main Base / Shoulder Body
body = cq.Workplane("XY").box(body_length, body_width, body_height).edges("|Z").fillet(fillet_radius)

# Rear attachment (ball joint and cylindrical tail)
ball = cq.Workplane("XY").center(-45, 0).sphere(12)
tail = cq.Workplane("YZ").workplane(offset=-45).circle(8).extrude(15)

# Side Pod with circular recess
side_pod = cq.Workplane("XY").center(10, -30).box(40, 25, 20).edges("|Z").fillet(8)
recess = cq.Workplane("XY").center(10, -30).workplane(offset=5).cylinder(20, 6)
side_pod = side_pod.cut(recess)

# Shoulder Joint
shoulder_joint = cq.Workplane("XY").center(35, 0).cylinder(25, 12)

# Upper Arm (tapered loft)
upper_arm = cq.Workplane("YZ").workplane(offset=35).circle(11).workplane(offset=80).circle(7).loft()

# Elbow Joint
elbow_joint = cq.Workplane("XY").center(115, 0).cylinder(18, 8)

# Lower Arm (tapered loft)
lower_arm = cq.Workplane("YZ").workplane(offset=115).circle(6.5).workplane(offset=90).circle(3.5).loft()

# Wrist Joint
wrist = cq.Workplane("XY").center(205, 0).cylinder(10, 4)

# Floating components (representing the separated parts in the top left)
float_x = -30
float_y = 80
f1 = cq.Workplane("XY").center(float_x, float_y).workplane(offset=15).box(30, 12, 10).edges("|Z").fillet(4)
f2 = cq.Workplane("XY").center(float_x, float_y).workplane(offset=30).box(30, 12, 10).edges("|Z").fillet(4)
pin = cq.Workplane("XY").center(float_x + 10, float_y + 6).workplane(offset=22.5).cylinder(25, 2)

# Combine all components into the final result
result = (
    body
    .union(ball)
    .union(tail)
    .union(side_pod)
    .union(shoulder_joint)
    .union(upper_arm)
    .union(elbow_joint)
    .union(lower_arm)
    .union(wrist)
    .union(f1)
    .union(f2)
    .union(pin)
)