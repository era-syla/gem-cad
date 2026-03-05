import cadquery as cq

# ---------------------------------------------------------
# Parametric Dimensions
# ---------------------------------------------------------

# Overall dimensions
length = 500.0          # Total length of the blade
width = 140.0           # Width of the main rectangular section
thickness = 6.0         # Thickness of the material

# Geometry of the tapered/mounting end
taper_length = 90.0     # Length of the tapered section
tip_width = 80.0        # Width at the narrowest edge (the tip)

# Mounting hole parameters
hole_diameter = 5.5     # Diameter of the mounting holes
hole_offset_end = 30.0  # Distance from the tip edge to the first row of holes
hole_spacing_x = 40.0   # Distance between the two rows of holes (longitudinal)
hole_spacing_y = 50.0   # Distance between the two parallel holes (transverse)

# ---------------------------------------------------------
# 3D Modeling
# ---------------------------------------------------------

# 1. Define the 2D Profile Points
# We draw the profile on the XY plane.
# Origin (0,0) is at the bottom-left corner of the rectangular end.
# The blade extends along the positive X-axis.

y_taper_start = (width - tip_width) / 2.0

points = [
    (0, 0),                                      # Bottom-left
    (length - taper_length, 0),                  # Start of bottom taper
    (length, y_taper_start),                     # Bottom corner of tip
    (length, width - y_taper_start),             # Top corner of tip
    (length - taper_length, width),              # Start of top taper
    (0, width)                                   # Top-left
]

# 2. Create Base Solid
# Draw the polygon and extrude it to create the main plate
base_plate = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# 3. Create Mounting Holes
# The pattern is a triangle: two holes near the tip, one hole further back.

# Calculate center coordinates
y_center = width / 2.0
x_row1 = length - hole_offset_end                   # X position of the two holes
x_row2 = length - hole_offset_end - hole_spacing_x  # X position of the single hole

# Define hole centers
hole_locations = [
    (x_row1, y_center + hole_spacing_y / 2.0), # Top hole near tip
    (x_row1, y_center - hole_spacing_y / 2.0), # Bottom hole near tip
    (x_row2, y_center)                         # Center hole further back
]

# Cut the holes through the plate
result = (
    base_plate
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)