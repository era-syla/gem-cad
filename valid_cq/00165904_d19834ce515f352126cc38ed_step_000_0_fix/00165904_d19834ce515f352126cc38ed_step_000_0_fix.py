import cadquery as cq

# Parameters
length = 100
width = 40
thickness = 5
pocket_radius = 15
pocket_depth = 2

# Outline points for hexagonal shape
pts = [
    ( length/2,    0        ),
    ( length/4,  width/2    ),
    (-length/4,  width/2    ),
    (-length/2,    0        ),
    (-length/4, -width/2    ),
    ( length/4, -width/2    ),
]

# Build the base plate
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .circle(pocket_radius)
    .cutBlind(-pocket_depth)
)