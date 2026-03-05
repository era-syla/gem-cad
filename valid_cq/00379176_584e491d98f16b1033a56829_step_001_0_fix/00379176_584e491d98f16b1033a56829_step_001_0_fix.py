import cadquery as cq

thickness = 20

# Body profile points (XY plane)
body_pts = [
    (0, 0),
    (30, -20),
    (60, -6),
    (40, -2),
    (80, 40),
    (60, 75),
    (20, 80),
    (0, 100),
    (-20, 80),
    (-60, 75),
    (-80, 40),
    (-40, -2),
    (-60, -6),
    (-30, -20),
]

# Create the body by extruding the outline
result = cq.Workplane("XY").polyline(body_pts).close().extrude(thickness)

# Neck parameters
neck_length = 120
neck_width = 20
neck_start = 100  # X offset where neck begins

# Create the neck
neck = (
    cq.Workplane("XY")
    .transformed(offset=(0, neck_start + neck_length / 2, 0))
    .rect(neck_width, neck_length)
    .extrude(thickness)
)
result = result.union(neck)

# Scroll: cylinder at end of neck, axis along X
scroll_radius = 12
scroll = (
    cq.Workplane("YZ", origin=(neck_start + neck_length, 0, thickness / 2))
    .circle(scroll_radius)
    .extrude(20)
)
result = result.union(scroll)

# Cut simple f-holes (two holes, one on each side)
for y in [15, -15]:
    # upper slanted part
    result = (
        result.faces(">Z")
        .workplane()
        .transformed(offset=(40, y, 0), rotate=(0, 0, 30))
        .rect(2, 15)
        .cutBlind(-thickness)
    )
    # lower slanted part
    result = (
        result.faces(">Z")
        .workplane()
        .transformed(offset=(80, y, 0), rotate=(0, 0, -30))
        .rect(2, 15)
        .cutBlind(-thickness)
    )