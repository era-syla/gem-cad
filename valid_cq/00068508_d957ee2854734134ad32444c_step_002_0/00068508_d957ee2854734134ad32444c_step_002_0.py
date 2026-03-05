import cadquery as cq

# --- Parametric Dimensions ---
plate_length = 140.0
plate_width = 45.0
plate_thickness = 3.0
corner_fillet = 4.0

# Center holes parameters
center_hole_diam = 9.0
num_center_holes = 4
center_hole_spacing = 30.0  # Pitch between holes

# Corner holes parameters
corner_hole_diam = 5.0
margin_x = 6.0  # Distance from side edge
margin_y = 6.0  # Distance from top/bottom edge

# --- Geometry Construction ---

# 1. Create the base plate centered at the origin
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Apply fillets to the vertical corners
result = result.edges("|Z").fillet(corner_fillet)

# 3. Create the central row of larger holes
# Calculate positions centered along the X-axis
center_points = []
total_span = (num_center_holes - 1) * center_hole_spacing
start_x = -total_span / 2.0

for i in range(num_center_holes):
    center_points.append((start_x + i * center_hole_spacing, 0))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(center_points)
    .hole(center_hole_diam)
)

# 4. Create the smaller corner holes
# Determine coordinates based on dimensions and margins
dx = (plate_length / 2.0) - margin_x
dy = (plate_width / 2.0) - margin_y

corner_points = [
    (dx, dy),
    (dx, -dy),
    (-dx, dy),
    (-dx, -dy)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(corner_points)
    .hole(corner_hole_diam)
)