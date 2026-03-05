import cadquery as cq

# Parameters
length = 200.0        # Total length of the bracket
height = 50.0         # Height of the vertical leg
width = 25.0          # Width of the horizontal leg
thickness = 4.0       # Material thickness
hole_count = 4        # Number of holes
hole_diameter = 5.0   # Diameter of the through hole
csk_diameter = 10.0   # Diameter of the countersink
csk_angle = 90.0      # Countersink angle

# Create the L-bracket base shape
# We sketch the L-profile on the YZ plane and extrude along the X axis
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                 # Outer corner at origin
        (0, height),            # Top of vertical leg
        (thickness, height),    # Inner top
        (thickness, thickness), # Inner corner
        (width, thickness),     # Inner right
        (width, 0),             # Right of horizontal leg
        (0, 0)                  # Close profile
    ])
    .close()
    .extrude(length)
)

# Calculate hole locations
# Holes are distributed evenly along the length (X)
# Holes are centered vertically on the vertical leg (Z)
pts = [
    (length * (i + 1) / (hole_count + 1), height / 2.0)
    for i in range(hole_count)
]

# Create countersunk holes on the vertical face
# We select the face with the minimum Y coordinate (the outer vertical face)
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints(pts)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)