import cadquery as cq

# Define parametric dimensions
length = 50.0  # Length of the box
width = 50.0   # Width of the box
height = 10.0  # Height (thickness) of the box
fillet_radius = 2.0 # Radius for the edge fillets

# Create the basic block
result = cq.Workplane("XY").box(length, width, height)

# Apply fillets to all edges
# This creates the rounded corners and rounded top/bottom edges visible in the image
result = result.edges().fillet(fillet_radius)
