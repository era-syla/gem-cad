import cadquery as cq

# Define parametric dimensions
length = 100.0
height = 20.0
thickness = 10.0
groove_height = 6.0
groove_depth = 3.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the base rectangular prism
    .box(length, thickness, height)
    # Select the front/side face (positive Y direction)
    .faces(">Y")
    .workplane()
    # Create a rectangular profile for the groove
    # Width is set slightly larger than length to ensure clean cuts at the ends
    .rect(length * 1.1, groove_height)
    # Cut the groove into the solid
    .cutBlind(-groove_depth)
)