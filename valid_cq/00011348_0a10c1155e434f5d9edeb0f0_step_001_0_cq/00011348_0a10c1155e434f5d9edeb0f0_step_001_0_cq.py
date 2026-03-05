import cadquery as cq

# Parametric dimensions
width = 50.0   # Width of the box
depth = 50.0   # Depth of the box
height = 80.0  # Height of the box
fillet_radius = 5.0 # Radius of the vertical edge fillets

# Create the base box
result = cq.Workplane("XY").box(width, depth, height)

# Select the vertical edges (parallel to Z axis) and apply a fillet
result = result.edges("|Z").fillet(fillet_radius)

# The result is now contained in the 'result' variable