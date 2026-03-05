import cadquery as cq

# Parametric dimensions for the L-profile
height = 80.0       # Height of the vertical leg
width = 40.0        # Width of the horizontal leg
thickness = 2.0     # Thickness of the material
length = 120.0      # Extrusion length

# Create the L-shaped profile on the XZ plane and extrude along the Y axis
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(width, 0)               # Bottom horizontal edge
    .lineTo(width, thickness)       # Right edge thickness
    .lineTo(thickness, thickness)   # Top of horizontal leg
    .lineTo(thickness, height)      # Inner vertical face
    .lineTo(0, height)              # Top edge thickness
    .close()                        # Closes back to (0,0)
    .extrude(length)
)