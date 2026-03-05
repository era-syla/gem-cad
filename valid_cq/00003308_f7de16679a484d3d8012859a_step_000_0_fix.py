import cadquery as cq

# Create a triangular prism (right triangle cross-section extruded)
# The shape appears to be a right-angle triangle bracket/wedge

width = 80   # depth of the prism
height = 60  # height of the triangle
base = 70    # base of the triangle

# Create the triangular profile as a 2D shape
# Right triangle with vertices at (0,0), (base,0), (0,height)
points = [
    (0, 0),
    (base, 0),
    (0, height),
]

result = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (base, 0), (0, height)])
    .close()
    .extrude(width)
)

# Add small chamfers to the edges for a more realistic look
result = result.edges("|Y").chamfer(1.5)