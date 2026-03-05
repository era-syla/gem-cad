import cadquery as cq

# Parametric dimensions for the L-angle bar
length = 200.0      # Total length of the extrusion
width = 30.0        # Width of the horizontal leg
height = 12.0       # Height of the vertical leg
thickness = 2.5     # Material thickness

# Create the geometry
# We sketch the L-profile on the YZ plane and extrude it along the X axis
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                  # Outer corner origin
        (width, 0),              # End of horizontal leg (outer)
        (width, thickness),      # End of horizontal leg (inner)
        (thickness, thickness),  # Inner corner
        (thickness, height),     # End of vertical leg (inner)
        (0, height),             # End of vertical leg (outer)
        (0, 0)                   # Close the profile
    ])
    .close()
    .extrude(length)
)