import cadquery as cq

# Parametric dimensions
height = 100.0  # Height of the block
width = 100.0   # Width of the block (face with hole)
depth = 50.0    # Thickness of the block
hole_diameter = 40.0  # Diameter of the through hole

# Create the main block
# We create a box centered on X and Y, sitting on Z=0 or centered on Z.
# Centering on all axes is usually easiest for symmetric features.
result = (
    cq.Workplane("XY")
    .box(width, height, depth)
    .faces(">Z")  # Select the top face (or front face depending on orientation preference)
    .workplane()
    .hole(hole_diameter) # Create a hole through the entire part
)

# Alternatively, if the hole needs to be along a specific axis relative to the view:
# The image shows a block where the hole is on the "front" face.
# Let's orient it such that the face with the hole is in the XZ plane or XY plane.
# The code above uses the Z-axis for the hole direction, which matches the standard "hole" operation.