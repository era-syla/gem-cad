import cadquery as cq

# Parameters
width = 5.0
thickness = 1.0
length = 200.0
hole_width = 3.0
hole_length = 8.0
hole_spacing = 10.0
num_holes = 19

# Create the base strip
result = cq.Workplane("XY").box(width, length, thickness)

# Calculate hole positions
start_y = -length / 2 + hole_spacing
positions = [(0, start_y + i * hole_spacing) for i in range(num_holes)]

# Create the holes
result = result.faces(">Z").workplane().pushPoints(positions).rect(hole_width, hole_length).cutThruAll()