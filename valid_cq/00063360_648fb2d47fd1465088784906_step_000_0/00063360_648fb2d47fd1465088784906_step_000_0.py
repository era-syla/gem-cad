import cadquery as cq

# Parametric dimensions for the L-bracket
height = 120.0        # Height of the vertical leg
width = 80.0          # Width of the bracket (extrusion depth)
leg_length = 35.0     # Length of the horizontal leg
thickness = 4.0       # Uniform thickness of the material

# Create the L-shape profile on the YZ plane (Side view)
# Local coordinates: X corresponds to Global Y, Y corresponds to Global Z
profile_points = [
    (0, 0),                      # Outer corner origin
    (leg_length, 0),             # End of horizontal leg (outer)
    (leg_length, thickness),     # End of horizontal leg (inner)
    (thickness, thickness),      # Inner corner
    (thickness, height),         # Top of vertical leg (inner)
    (0, height),                 # Top of vertical leg (outer)
    (0, 0)                       # Close the loop
]

# Generate the 3D model by sketching the profile and extruding it
result = (
    cq.Workplane("YZ")
    .polyline(profile_points)
    .close()
    .extrude(width)
)