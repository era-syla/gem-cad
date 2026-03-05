import cadquery as cq

# Define parametric dimensions
length = 100.0    # Total length of the profile
height = 60.0     # Height of the vertical leg
width = 40.0      # Width of the horizontal leg
thickness = 2.0   # Uniform thickness of the material

# Create the 3D model
# We define the L-shaped cross-section on the YZ plane and extrude it along the X axis
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                  # Outer corner (origin)
        (width, 0),              # End of horizontal leg (bottom)
        (width, thickness),      # End of horizontal leg (top)
        (thickness, thickness),  # Inner corner
        (thickness, height),     # Top of vertical leg (inner)
        (0, height),             # Top of vertical leg (outer)
        (0, 0)                   # Close the loop
    ])
    .close()
    .extrude(length)
)