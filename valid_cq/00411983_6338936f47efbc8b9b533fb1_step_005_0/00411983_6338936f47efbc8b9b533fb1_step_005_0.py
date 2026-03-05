import cadquery as cq

# --- Parameters ---
# Plate dimensions
plate_length = 200.0
plate_width = 150.0
plate_thickness = 8.0
corner_radius = 5.0

# Hole specifications
hole_diameter = 5.5       # Clearance for M5 roughly
csk_diameter = 11.0       # Countersink top diameter
csk_angle = 90.0          # Countersink angle

# Hole positioning
# Distance from the plate edges to the corner-most hole center
inset_x = 15.0
inset_y = 15.0
# Spacing between the two holes in each corner pair
pair_spacing = 25.0

# --- Geometry Generation ---

# Calculate hole coordinates
# The holes are grouped in pairs at each of the 4 corners.
# The pairs are aligned along the X-axis (length).
# We define the Y coordinate (symmetric) and the two X coordinates (outer and inner).
y_loc = (plate_width / 2.0) - inset_y
x_outer = (plate_length / 2.0) - inset_x
x_inner = x_outer - pair_spacing

# Generate list of (x, y) points for all 8 holes using symmetry
hole_points = [
    (x_val * x_sign, y_loc * y_sign)
    for x_val in [x_outer, x_inner]
    for x_sign in [1, -1]
    for y_sign in [1, -1]
]

# Create the part
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)