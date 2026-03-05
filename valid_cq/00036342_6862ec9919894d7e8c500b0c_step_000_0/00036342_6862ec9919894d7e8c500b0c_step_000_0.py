import cadquery as cq

# Parametric dimensions
width = 20.0       # Width of the cross-section
depth = 20.0       # Depth of the cross-section
height = 100.0     # Height of the column
fillet_radius = 3.0 # Radius of the corner fillets

# Create the model: A rectangular prism with vertical edges filleted
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .edges("|Z")  # Select edges parallel to the Z axis (vertical edges)
    .fillet(fillet_radius)
)