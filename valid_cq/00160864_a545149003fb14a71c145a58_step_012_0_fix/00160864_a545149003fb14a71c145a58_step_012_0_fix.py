import cadquery as cq

# Create the rectangular block with a small top protrusion and two holes
plate = (
    cq.Workplane("XY")
    .rect(10, 5)            # main block footprint: width 10, depth 5
    .extrude(50)            # main block height 50
    .faces(">Z")            # top face of the main block
    .workplane()
    .rect(10, 5)            # same footprint for the small protrusion
    .extrude(5)             # protrusion height 5
    .faces("<Y")            # front face of the combined shape
    .workplane()
    .pushPoints([(0, 15), (0, -15)])  # positions for the two holes along Z
    .hole(3)                # drill holes of diameter 3 through the thickness
)

# Create the separate cylinder (pin)
cylinder = (
    cq.Workplane("XY")
    .center(20, 0)          # move it 20 mm over in X so it does not intersect the plate
    .circle(5)              # radius 5
    .extrude(100)           # height 100
)

# Combine both solids into a single result
result = plate.union(cylinder)