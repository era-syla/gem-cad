import cadquery as cq

# Parametric dimensions for the model
length = 90.0           # Total length of the part
width_end = 32.0        # Width of the wider end sections
width_mid = 16.0        # Width of the narrower middle section
thickness = 6.0         # Thickness of the plate
end_section_len = 22.0  # Length of the wide end sections
chamfer_dist = 5.0      # Size of the chamfer at the ends
hole_diam = 5.0         # Diameter of the through holes
csk_diam = 10.0         # Diameter of the countersink
csk_angle = 90.0        # Angle of the countersink
hole_spacing = 15.0     # Distance between hole centers

# Define the points for the 2D profile (XY plane)
# Starting from bottom-left corner and moving counter-clockwise
pts = [
    (-length/2, -width_end/2),
    (-length/2 + end_section_len, -width_end/2),
    (-length/2 + end_section_len, -width_mid/2),
    (length/2 - end_section_len, -width_mid/2),
    (length/2 - end_section_len, -width_end/2),
    (length/2, -width_end/2),
    (length/2, width_end/2),
    (length/2 - end_section_len, width_end/2),
    (length/2 - end_section_len, width_mid/2),
    (-length/2 + end_section_len, width_mid/2),
    (-length/2 + end_section_len, width_end/2),
    (-length/2, width_end/2)
]

# Create the base shape
# 1. Draw the profile
# 2. Extrude to create the solid volume
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Apply chamfers to the ends
# Select edges that are:
# 1. Parallel to the Y axis (|Y)
# 2. On the top face (>Z)
# 3. At the extreme ends of the X axis (>X or <X)
result = (
    result
    .edges("|Y and >Z and (>X or <X)")
    .chamfer(chamfer_dist)
)

# Create the countersunk holes
# 1. Select the top face
# 2. Define center points for the two holes
# 3. Cut countersunk holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_spacing/2, 0), (-hole_spacing/2, 0)])
    .cskHole(hole_diam, csk_diam, csk_angle)
)