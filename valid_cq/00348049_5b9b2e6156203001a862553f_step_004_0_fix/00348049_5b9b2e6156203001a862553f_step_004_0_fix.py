import cadquery as cq

# Parameters
length = 100.0
width = 40.0
thickness = 5.0
chamfer = 10.0

# Define the 2D profile with chamfered short ends
pts = [
    (-length/2 + chamfer, -width/2),
    ( length/2 - chamfer, -width/2),
    ( length/2,         -width/2 + chamfer),
    ( length/2,          width/2 - chamfer),
    ( length/2 - chamfer, width/2),
    (-length/2 + chamfer, width/2),
    (-length/2,          width/2 - chamfer),
    (-length/2,         -width/2 + chamfer)
]

# Build the part
result = cq.Workplane("XY").polyline(pts).close().extrude(thickness)