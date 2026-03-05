import cadquery as cq

# Parametric dimensions
length = 100.0      # Length of the L-profile
leg1_length = 40.0  # Height of the vertical leg
leg2_length = 30.0  # Width of the horizontal leg
thickness = 5.0     # Material thickness

# Create the L-profile shape
# We start by drawing the L-shape on a 2D plane (YZ plane) and extruding it along the X axis.
# Alternatively, we can draw on the XY plane and extrude up. Let's draw the cross-section on the YZ plane.

# Define the points for the L-shape polyline
pts = [
    (0, 0),                       # Origin corner
    (leg2_length, 0),             # Bottom right outer corner
    (leg2_length, thickness),     # Bottom right inner corner
    (thickness, thickness),       # Inner corner
    (thickness, leg1_length),     # Top inner corner
    (0, leg1_length),             # Top outer corner
    (0, 0)                        # Closing the loop
]

# Create the solid
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# If running in an environment that supports show_object, this would visualize it
# show_object(result)