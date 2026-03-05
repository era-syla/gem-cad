import cadquery as cq

# Parameters
length = 80.0
width = 10.0
thickness = 10.0
slot_width = 3.0
hole_dia = 4.0
hole_offsets = [15.0, 35.0, 55.0]  # distances from the top face along Z

# Build the main block
result = cq.Workplane("XY").box(width, thickness, length)

# Cut the long slot (T-slot simplified as a straight slot) on the front face (-Y)
result = result.faces("<Y").workplane().rect(slot_width, length).cutThruAll()

# Drill three holes through the back face (+Y), spaced along the Z direction
for off in hole_offsets:
    # workplane on the +Y face, center(0, ...) moves along local Y which is global Z
    result = result.faces(">Y").workplane().center(0, length/2 - off).hole(hole_dia)

# 'result' now contains the final solid
result