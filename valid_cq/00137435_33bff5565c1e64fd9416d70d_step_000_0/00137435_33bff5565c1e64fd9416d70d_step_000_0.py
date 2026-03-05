import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 150.0        # Length of the tube
width = 50.0          # Outer width of the rectangular profile
height = 80.0         # Outer height of the rectangular profile
wall_thickness = 4.0  # Thickness of the tube walls
fillet_radius = 5.0   # Radius of the outer corners

# Create the rectangular hollow tube
result = (
    cq.Workplane("XY")
    # Create the base solid block
    .box(length, width, height)
    # Select the edges running along the length (parallel to X axis)
    .edges("|X")
    # Apply fillets to the outer corners
    .fillet(fillet_radius)
    # Select the end faces (perpendicular to X axis)
    .faces("|X")
    # Shell the solid inwards to create the hollow tube, removing the selected end faces
    .shell(-wall_thickness)
)