import cadquery as cq

# Parametric dimensions
width = 50.0   # Width of the block (x-axis)
depth = 30.0   # Depth of the block (y-axis)
height = 80.0  # Height of the block (z-axis)
fillet_radius = 10.0 # Radius of the top edge fillets

# Create the basic block
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    # Select the top face edges along the Y direction (depth)
    # We select edges that are parallel to the Y axis and located at the highest Z
    .edges("|Y and >Z")
    # Apply fillet
    .fillet(fillet_radius)
)