import cadquery as cq

# --- Parameters ---
# Main U-Bracket dimensions
bracket_height = 120.0   # Length of the bracket along Z
bracket_width = 80.0     # Overall width along X
bracket_depth = 40.0     # Flange depth along Y
wall_thickness = 6.0     # Material thickness

# Main Bracket Hole Pattern
rows = 4
cols = 2
row_spacing = 25.0       # Vertical pitch
col_spacing = 50.0       # Horizontal pitch
hole_diameter = 6.5      # Clearance for M6
csk_diameter = 12.0      # Countersink diameter
csk_angle = 90.0         # Countersink angle

# Small Plate dimensions (Nut plate / Spacer)
plate_width = 18.0
plate_height = 45.0
plate_thickness = 5.0
plate_hole_spacing = 25.0

# --- Geometry Construction ---

# 1. Main U-Bracket Generation
# Define the U-profile points on the XY plane.
# Oriented with the web face at Y=0 and flanges extending in +Y.
half_w = bracket_width / 2.0
pts = [
    (half_w, 0),                                # Start: Bottom-right outer
    (half_w, bracket_depth),                    # Right flange tip outer
    (half_w - wall_thickness, bracket_depth),   # Right flange tip inner
    (half_w - wall_thickness, wall_thickness),  # Inner corner right
    (-half_w + wall_thickness, wall_thickness), # Inner corner left
    (-half_w + wall_thickness, bracket_depth),  # Left flange tip inner
    (-half_w, bracket_depth),                   # Left flange tip outer
    (-half_w, 0),                               # End: Bottom-left outer
]

# Create the base extrusion
u_bracket = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(bracket_height)
)

# Create countersunk holes on the web face
# We select the face with the minimum Y coordinate (the front face)
u_bracket = (
    u_bracket.faces("<Y").workplane()
    .rarray(col_spacing, row_spacing, cols, rows)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 2. Small Plate Generation
# Create a separate rectangular plate with 2 holes, as seen in the bottom of the image
small_plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_thickness, plate_height) # Centered box
    .faces("<Y").workplane()
    .rarray(1, plate_hole_spacing, 1, 2) # 1 column, 2 rows
    .hole(hole_diameter)
)

# Translate the small plate to position it below the main bracket
# Offset it in Z to separate it, and in X to align visually
small_plate_positioned = small_plate.translate((-bracket_width/2.0 + plate_width, 0, -plate_height - 30.0))

# Combine both parts into a single result
result = u_bracket.union(small_plate_positioned)