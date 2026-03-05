import cadquery as cq

# Define parameters
tube_radius = 2.0
frame_height = 100.0
frame_width = 50.0
frame_depth = 30.0

# Create a basic frame structure
verticals = (
    cq.Workplane("XY")
    .rect(frame_width, tube_radius, forConstruction=True)
    .vertices()
    .circle(tube_radius)
    .extrude(frame_height)
)

horizontals = (
    cq.Workplane("XY")
    .workplane(offset=frame_height / 2)
    .rect(frame_width, frame_depth, forConstruction=True)
    .vertices()
    .circle(tube_radius)
    .extrude(tube_radius)
)

diagonals = (
    cq.Workplane("XY")
    .workplane(offset=frame_height / 4)
    .moveTo(frame_width / 2, frame_depth / 2)
    .lineTo(-frame_width / 2, -frame_depth / 2)
    .circle(tube_radius)
    .extrude(frame_height / 2, both=True)
)

# Combine all parts
result = verticals.union(horizontals).union(diagonals)