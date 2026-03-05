import cadquery as cq

# Define parametric dimensions
length = 100.0   # Total length of the plate
width = 30.0     # Width of the plate
thickness = 2.0  # Thickness of the plate
hole_diameter = 15.0 # Diameter of the central hole

# Create the 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)  # Create the base rectangular plate
    .faces(">Z")                    # Select the top face
    .workplane()
    .hole(hole_diameter)            # Create a through-hole in the center
)