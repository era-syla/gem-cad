import cadquery as cq

# Parameters
length = 50.0
width = 20.0
thickness = 3.0
fillet_radius = 4.0
hole_dia = 4.0
hole_pitch = 10.0
num_cols = 5
num_rows = 2

# Create the base plate with rounded corners and an array of holes
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .rarray(hole_pitch, hole_pitch, num_cols, num_rows)
    .hole(hole_dia)
)