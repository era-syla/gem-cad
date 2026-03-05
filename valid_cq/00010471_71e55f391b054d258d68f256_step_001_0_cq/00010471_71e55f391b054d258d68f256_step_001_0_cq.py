import cadquery as cq

# Parametric dimensions
length = 100.0       # Total length of the angle bar
width = 20.0         # Width of the horizontal flange
height = 20.0        # Height of the vertical flange
thickness = 2.0      # Thickness of the material

# Create the L-profile
# We will draw the cross-section on the YZ plane and extrude along X
# The profile looks like an 'L' shape.

# Define points for the L-shape cross-section
# Starting from the inner corner (0,0) conceptually, but let's center it or align it logically.
# Let's align the bottom-left corner of the bounding box at (0,0) for simplicity in drawing.

result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(width, 0)                # Bottom edge
    .lineTo(width, thickness)        # Outer vertical edge of bottom flange
    .lineTo(thickness, thickness)    # Inner horizontal edge
    .lineTo(thickness, height)       # Inner vertical edge
    .lineTo(0, height)               # Top edge
    .close()                         # Closing the loop back to (0,0) along the outer vertical edge
    .extrude(length)
)

# Optional: Rotate to match the isometric view in the image better (Extruded along X)
# The image shows the length extending towards the upper left.
# The default extrude(length) on YZ creates it along positive X.
# This orientation is generally acceptable.