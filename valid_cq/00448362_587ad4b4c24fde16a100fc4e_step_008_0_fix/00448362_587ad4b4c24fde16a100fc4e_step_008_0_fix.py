import cadquery as cq

thk = 5

# Define 2D outline of the bracket
pts = [
    (0, 0),
    (30, 0),
    (40, 0),
    (40, 8),
    (30, 8),
    (30, 45),
    (43, 55),
    (10, 90),
    (0, 90)
]

# Extrude the profile to a 3D solid
base = cq.Workplane("XY").polyline(pts).close().extrude(thk)

# Create holes on the front face
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(20, 30)])
    .hole(10)
    .pushPoints([(45, 45)])
    .hole(20)
)