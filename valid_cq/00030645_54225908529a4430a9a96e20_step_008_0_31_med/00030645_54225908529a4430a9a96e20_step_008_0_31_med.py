import cadquery as cq

# Parameters
length = 150.0
width = 5.0
height = 8.0
hole_diameter = 1.2
pitch_x = 2.0
pitch_y = 2.0
num_holes = int(length / pitch_x) - 1

# Create base block
base = cq.Workplane("XY").box(length, width, height)

# Add two rows of holes on the top face
result = (
    base.faces(">Z")
    .workplane()
    .rarray(pitch_x, pitch_y, num_holes, 2)
    .hole(hole_diameter, depth=4.0)
)