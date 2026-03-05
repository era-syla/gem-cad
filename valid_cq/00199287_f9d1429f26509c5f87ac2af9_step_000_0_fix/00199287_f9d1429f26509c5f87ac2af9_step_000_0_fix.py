import cadquery as cq

# Define main body profile as a hexagon with chamfered ends
points = [(0, -25), (80, -25), (90, -15), (90, 15), (80, 25), (0, 25)]

# Create the main body
body = cq.Workplane("XY").polyline(points).close().extrude(10)

# Create the cavity box that will serve both as cutout and the tray shape
# The box is 20×50×8, flush with the body's left face (x=0), centered in Y, sitting on Z=0
cavity = cq.Workplane("XY").box(20, 50, 8, centered=(False, True, False))

# Subtract the cavity from the body to create a slot
body = body.cut(cavity)

# Create the tray by translating the same box outward by 10mm in X
tray = cavity.translate((-10, 0, 0))

# Combine the body and the tray into the final result
result = body.union(tray)