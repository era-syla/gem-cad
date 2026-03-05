import cadquery as cq

# Parametric dimensions
length = 100.0       # Length of the angle iron
width = 20.0         # Width of the horizontal flange
height = 20.0        # Height of the vertical flange
thickness = 2.0      # Thickness of the material

# Create the L-profile shape
# We will draw the cross-section on the YZ plane and extrude it along the X axis
# This orientation matches the typical view in the image

result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(width, 0)        # Bottom edge
    .lineTo(width, thickness) # Bottom flange thickness
    .lineTo(thickness, thickness) # Inner corner
    .lineTo(thickness, height)    # Vertical flange inner edge
    .lineTo(0, height)       # Vertical top edge
    .close()
    .extrude(length)
)

# Optional: Add fillets to the internal corner if desired for a more realistic structural beam
# result = result.edges("|X and <Z").fillet(thickness/2) 

# Export or visualization step is handled by the 'result' variable convention