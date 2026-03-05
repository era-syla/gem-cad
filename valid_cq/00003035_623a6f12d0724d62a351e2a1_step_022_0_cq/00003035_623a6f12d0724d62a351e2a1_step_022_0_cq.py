import cadquery as cq

# Parametric variables
length = 80.0     # Total length of the plate
width = 40.0      # Total width of the plate
thickness = 4.0   # Thickness of the plate
fillet_radius = 5.0 # Radius for the corner fillets

# Hole parameters
hole_diameter = 3.5      # Diameter of the through-hole
csk_diameter = 6.0       # Diameter of the countersink top
csk_angle = 90.0         # Angle of the countersink cone

# Hole layout coordinates (based on visual estimation relative to center)
# The pattern consists of:
# 1. A single hole on the right side.
# 2. A central column of 3 holes.
# 3. A left column of 3 holes (making a grid on the left).
# Let's define positions relative to the center (0,0).

# Right single hole
hole_right_pos = [(25, 0)]

# Center column (slightly offset to the left)
center_col_x = -5.0
hole_center_col_pos = [
    (center_col_x, 10), 
    (center_col_x, 0), 
    (center_col_x, -10)
]

# Left column
left_col_x = -20.0
hole_left_col_pos = [
    (left_col_x, 10), 
    (left_col_x, 0), 
    (left_col_x, -10)
]

# Combine all hole positions
all_hole_locations = hole_right_pos + hole_center_col_pos + hole_left_col_pos

# Create the base plate
base = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Create the countersunk holes
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(all_hole_locations)
    .cskHole(hole_diameter, csk_diameter, csk_angle, depth=None)
)