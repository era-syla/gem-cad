import cadquery as cq

thickness = 2.0

# U-shaped bracket
u_shape = (
    cq.Workplane("XY")
    .polyline([
        (-60, 0), (60, 0),
        (60, 20), (20, 20),
        (20, 40), (-20, 40),
        (-20, 20), (-60, 20)
    ])
    .close()
    .extrude(thickness)
    .translate((0, 60, 0))
)

# Small rectangle on the left middle
rect_left = (
    cq.Workplane("XY")
    .rect(40, 20)
    .extrude(thickness)
    .translate((-60, 20, 0))
)

# Square at bottom center
square_center = (
    cq.Workplane("XY")
    .rect(30, 30)
    .extrude(thickness)
    .translate((0, -40, 0))
)

# Taller rectangle at bottom left
rect_bottom_left = (
    cq.Workplane("XY")
    .rect(20, 40)
    .extrude(thickness)
    .translate((-40, -20, 0))
)

# Large square at bottom right
square_big = (
    cq.Workplane("XY")
    .rect(80, 80)
    .extrude(thickness)
    .translate((60, -60, 0))
)

# Combine all parts into one result
result = u_shape.union(rect_left).union(square_center).union(rect_bottom_left).union(square_big)