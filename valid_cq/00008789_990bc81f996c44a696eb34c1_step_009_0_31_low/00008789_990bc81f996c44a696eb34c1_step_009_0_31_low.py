import cadquery as cq

# Parameters
width = 100.0
length = 60.0
thickness = 5.0
chamfer_size = 30.0
hole_dia = 5.0

# Create base plate with chamfer
result = (
    cq.Workplane("XY")
    .box(width, length, thickness)
    .edges("|Z")
    .edges(">X and >Y")
    .chamfer(chamfer_size)
)

# Add holes
hole_pts = [
    (-width/2 + 20, length/2 - 15),
    (-width/2 + 20, -length/2 + 15),
    (width/2 - 30, length/2 - 15),
    (width/2 - 15, -length/2 + 15)
]

result = result.faces(">Z").workplane().pushPoints(hole_pts).hole(hole_dia)