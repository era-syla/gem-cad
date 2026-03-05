import cadquery as cq

# Main body dimensions
body_length = 50
body_width = 20
body_height = 25

# Create the main rectangular body
main_body = (
    cq.Workplane("XY")
    .box(body_length, body_width, body_height)
)

# Create the two upright posts/towers on top
# Left tower
left_tower = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-12, 0, body_height/2))
    .box(14, body_width, 15)
)

# Right tower
right_tower = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(12, 0, body_height/2))
    .box(14, body_width, 15)
)

# Combine main body with towers
body = main_body.union(left_tower).union(right_tower)

# Add rounded tops to towers - use cylinder on top of each tower
left_top = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(-12, body_height/2 + 15, 0))
    .cylinder(body_width, 7)
)

right_top = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(12, body_height/2 + 15, 0))
    .cylinder(body_width, 7)
)

body = body.union(left_top).union(right_top)

# Cut U-groove in left tower
left_groove = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-12, 0, body_height/2 + 8))
    .cylinder(20, 5)
)

# Cut U-groove in right tower
right_groove = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(12, 0, body_height/2 + 8))
    .cylinder(20, 5)
)

body = body.cut(left_groove).cut(right_groove)

# Add horizontal cylinder (pin/shaft) sticking out from left side
shaft = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, body_height/2 - 5, -body_length/2 - 8))
    .cylinder(16, 5)
)

body = body.union(shaft)

# Add mounting base/flange on the right side bottom
flange = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(body_length/2 + 5, 0, -body_height/2 + 4))
    .box(10, body_width + 10, 8)
)

body = body.union(flange)

# Cut slot in the bottom center of main body for mounting
slot = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, -body_height/2 + 3))
    .box(8, 8, 10)
)

body = body.cut(slot)

result = body