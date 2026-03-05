import cadquery as cq

# Parameters
length = 200
width = 10
thickness = 5
hole_diameter = 4
hole_count = 7
edge_offset = 10

# Compute hole spacing
spacing = (length - 2 * edge_offset) / (hole_count - 1)
positions = [(edge_offset + i * spacing, 0) for i in range(hole_count)]

# Build the bar with through holes
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(positions)
    .hole(hole_diameter)
)