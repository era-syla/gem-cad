import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the box
width = 70.0    # Width of the box
height = 40.0   # Height of the box
vertical_radius = 10.0 # Radius for the vertical corner fillets
bottom_radius = 3.0   # Radius for the bottom edge fillets

# Create the base box
result = cq.Workplane("XY").box(length, width, height)

# Fillet the vertical edges
# We select edges that are parallel to the Z axis
result = result.edges("|Z").fillet(vertical_radius)

# Fillet the bottom edges
# We select the bottom face, then get its outer wire/edges
# Alternatively, select edges that are on the bottom plane (Z = -height/2)
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, -height/2))).fillet(bottom_radius)

# Note: The top edges appear sharp in the image, so no fillet is applied there.