import cadquery as cq

# Parametric dimensions
length = 100.0      # Total length of the block
width = 30.0        # Total width of the block
height = 40.0       # Total height of the block
wall_thickness = 4.0  # Thickness of the side walls
floor_thickness = 5.0 # Thickness of the bottom floor

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, height)  # Create base block centered at origin
    .faces(">Z")                 # Select the top face
    .workplane()                 # Create a new workplane on the top face
    .rect(length - 2 * wall_thickness, width - 2 * wall_thickness) # Sketch the pocket profile
    .cutBlind(-(height - floor_thickness)) # Cut the pocket downwards
)