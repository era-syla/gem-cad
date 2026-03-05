import cadquery as cq

# Create the vertical part of the shape
vertical = cq.Workplane("XY").box(2, 1, 10)

# Create the horizontal part of the shape
horizontal = (
    cq.Workplane("XY")
    .transformed(offset=(7, 0, 9))
    .box(10, 1, 1)
)

# Create the curved end
curved_end = (
    cq.Workplane("XY")
    .transformed(offset=(17, 0, 9), rotate=(0, 90, 0))
    .circle(0.5)
    .extrude(2)
)

# Combine all parts into the final shape
result = vertical.union(horizontal).union(curved_end)