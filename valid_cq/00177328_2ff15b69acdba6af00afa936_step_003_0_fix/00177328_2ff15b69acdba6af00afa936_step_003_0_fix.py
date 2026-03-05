import cadquery as cq

# Plate parameters
thickness = 2.0
plate_outline = [
    (0, 0),
    (60, 0),
    (65, 10),
    (60, 30),
    (0, 30),
    (10, 15),
]

# Build the plate
plate = (
    cq.Workplane("XY")
    .polyline(plate_outline)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .hole(6.0)
)

# Build the twisted sheet by lofting between two rectangles
twisted = (
    cq.Workplane("XY")
    .rect(20.0, 30.0)                       # bottom profile at z=0
    .workplane(offset=40.0)                 # move to z=40
    .transformed(rotate=(0, 0, 60))         # rotate top profile by 60° around Z
    .rect(40.0, 30.0)                       # top profile
    .loft()                                 # loft between the two profiles
    .translate((80, 0, 0))                  # move it aside so it doesn't intersect the plate
)

# Combine into a single result
result = plate.union(twisted)