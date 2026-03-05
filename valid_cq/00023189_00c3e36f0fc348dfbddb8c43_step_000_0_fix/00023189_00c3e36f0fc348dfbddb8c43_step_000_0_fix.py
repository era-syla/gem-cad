import cadquery as cq

# Create the base L-profile
result = (
    cq.Workplane("XY")
    .box(100, 5, 5)
    .faces(">Z")
    .workplane()
    .move(5, -2.5)
    .rect(90, 5, centered=False)
    .extrude(5)
)

# Add holes in a pattern
hole_diameter = 1.5
hole_spacing = 10
x_offset = 15
y_offset = 2.5

# Function to add a pattern of holes
def add_hole_pattern(plane, num_holes):
    return (
        plane.rarray(hole_spacing, 0, num_holes, 1)
        .circle(hole_diameter / 2)
        .cutThruAll()
    )

# Create vertical holes on one face
result = result.faces(">X").workplane().transformed(offset=(0, y_offset)).move(x_offset, 0)
result = add_hole_pattern(result, 8)

# Create vertical holes on adjacent face
result = result.faces("<Y").workplane().transformed(offset=(0, y_offset)).move(x_offset, 0)
result = add_hole_pattern(result, 8)