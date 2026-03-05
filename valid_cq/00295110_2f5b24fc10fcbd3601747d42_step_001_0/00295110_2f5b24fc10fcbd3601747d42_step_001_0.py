import cadquery as cq

# Parameters for the tray dimensions
length = 150.0       # Total length of the tray
width = 50.0         # Total width of the tray
height = 20.0        # Total height of the tray
wall_thickness = 3.0 # Thickness of the walls and floor
corner_radius = 6.0  # Outer radius of the vertical corners

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, height)  # Create the base block
    .edges("|Z")                 # Select vertical edges
    .fillet(corner_radius)       # Apply rounded corners
    .faces("+Z")                 # Select the top face
    .shell(-wall_thickness)      # Hollow out the shape inwards
)