import cadquery as cq

# Main rectangular body
body = (
    cq.Workplane("XY")
    .box(30, 20, 60, centered=(True, True, False))
)

# Add the top cylindrical cap area - rounded top section
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=60)
    .center(0, 0)
    .box(30, 20, 15, centered=(True, True, False))
)

# Combine body with top section
result = body.union(top_cap)

# Add rounded top (cylinder on top)
top_cylinder = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(0, 75)
    .cylinder(30, 10)
    .rotate((0, 0, 0), (1, 0, 0), 90)
)

# Build the main body with rounded top
main_body = (
    cq.Workplane("XY")
    .box(30, 20, 70, centered=(True, True, False))
)

# Add cylinder on top oriented along Y axis
top_cyl = (
    cq.Workplane("XZ")
    .center(0, 75)
    .circle(10)
    .extrude(20)
)

# Simpler approach - build piece by piece
# Main tall block
main = cq.Workplane("XY").box(28, 18, 65, centered=(True, True, False))

# Top rounded section - cylinder running along Y axis at top
top_round = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(0, 70)
    .circle(10)
    .extrude(28)
    .translate((-14, 0, 0))
)

# Merge top rounded with main
result = main.union(top_round)

# Add notch/slot on the right side of the body (the vertical slot visible)
result = (
    result
    .cut(
        cq.Workplane("XY")
        .center(14, 0)
        .box(6, 8, 50, centered=(True, True, False))
        .translate((0, 0, 10))
    )
)

# Add elbow fitting on the left side (L-shaped tube fitting)
# Horizontal part going left
elbow_horiz = (
    cq.Workplane("XY")
    .center(-14, 2)
    .workplane(offset=25)
    .circle(4)
    .extrude(15)
    .rotate((0, 0, 0), (0, 0, 1), 0)
)

# Rotate to go in X direction
elbow_h = (
    cq.Workplane("YZ")
    .workplane(offset=-14)
    .center(2, 25)
    .circle(4)
    .extrude(18)
    .translate((0, 0, 0))
)

elbow_h2 = (
    cq.Workplane("XZ")
    .workplane(offset=2)
    .center(-14, 25)
    .circle(4)
    .extrude(18)
)

result = result.union(elbow_h2)

# Vertical part of elbow going down
elbow_v = (
    cq.Workplane("XY")
    .center(-28, 2)
    .workplane(offset=15)
    .circle(4)
    .extrude(12)
)

result = result.union(elbow_v)

# Small connector tip
tip = (
    cq.Workplane("XY")
    .center(-28, 2)
    .workplane(offset=15)
    .circle(5.5)
    .extrude(4)
)
result = result.union(tip)

# Small screw/button on right side
screw = (
    cq.Workplane("YZ")
    .workplane(offset=15)
    .center(0, 20)
    .circle(3)
    .extrude(3)
)
result = result.union(screw)