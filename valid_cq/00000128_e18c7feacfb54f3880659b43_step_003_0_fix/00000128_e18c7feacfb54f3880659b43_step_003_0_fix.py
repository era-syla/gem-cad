import cadquery as cq

# Parameters
outer_radius = 40
outer_thickness = 12
rim_width = 6
rim_depth = 8
inner_recess_radius = outer_radius - rim_width
tube_radius = 10
tube_wall = 2
tube_length = 14
nozzle_radius = 8
nozzle_length = 10

# Tube center positions (4 tubes arranged in 2x2 pattern)
tube_positions = [
    (-10, 8),
    (10, 8),
    (-10, -8),
    (10, -8),
]

# Build the main disc body
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_thickness)
)

# Add rim/flange on the back face
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(outer_radius + 3)
    .extrude(3)
)

# Cut the inner recess on the front face
result = (
    result
    .faces("<Z")
    .workplane()
    .circle(inner_recess_radius)
    .cutBlind(-5)
)

# Add the 4 tubes protruding from the front face
for (tx, ty) in tube_positions:
    result = (
        result
        .faces("<Z")
        .workplane()
        .center(tx, ty)
        .circle(tube_radius)
        .extrude(tube_length)
    )

# Cut through-holes in all 4 tubes
for (tx, ty) in tube_positions:
    result = (
        result
        .faces("<Z")
        .workplane()
        .center(tx, ty)
        .circle(tube_radius - tube_wall)
        .cutThruAll()
    )

# Add a single nozzle/connector on the side (top)
result = (
    result
    .faces(">Y")
    .workplane()
    .circle(nozzle_radius)
    .extrude(nozzle_length)
)

# Cut through the nozzle
result = (
    result
    .faces(">Y")
    .workplane()
    .circle(nozzle_radius - tube_wall)
    .cutBlind(-nozzle_length)
)