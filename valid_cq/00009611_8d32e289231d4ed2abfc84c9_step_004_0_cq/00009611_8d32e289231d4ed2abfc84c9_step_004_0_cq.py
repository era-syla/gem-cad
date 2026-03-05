import cadquery as cq

# Parameters for the plate
width = 100.0   # Width of the plate (X direction)
height = 150.0  # Height of the plate (Y direction)
thickness = 5.0 # Thickness of the plate (Z direction)
fillet_radius = 5.0 # Radius for corner fillets

# Create the base plate centered on the XY plane
result = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .edges("|Z")  # Select vertical edges (parallel to Z axis)
    .fillet(fillet_radius)
)