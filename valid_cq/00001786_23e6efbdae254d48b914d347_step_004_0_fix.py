import cadquery as cq

# Dimensions
plate_length = 200
plate_width = 100
plate_thickness = 5

# Small hole grid parameters
small_hole_dia = 2.5
small_hole_spacing = 5
small_hole_margin = 5

# Large hole parameters (countersunk mounting holes)
large_hole_dia = 6
large_hole_positions = [
    (-80, -30), (-80, 30),
    (-20, -30), (-20, 30),
    (40, -30), (40, 30),
    (80, -30), (80, 30),
]

# Create base plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
)

# Add small holes in a grid pattern
small_holes = []
x_start = -plate_length/2 + small_hole_margin
x_end = plate_length/2 - small_hole_margin
y_start = -plate_width/2 + small_hole_margin
y_end = plate_width/2 - small_hole_margin

# Generate grid of small holes
nx = int((x_end - x_start) / small_hole_spacing) + 1
ny = int((y_end - y_start) / small_hole_spacing) + 1

small_hole_pts = []
for i in range(nx):
    for j in range(ny):
        x = x_start + i * small_hole_spacing
        y = y_start + j * small_hole_spacing
        small_hole_pts.append((x, y))

# Drill small holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(small_hole_pts)
    .hole(small_hole_dia, plate_thickness)
)

# Drill large mounting holes (countersunk style - just through holes with larger diameter)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(large_hole_positions)
    .hole(large_hole_dia, plate_thickness)
)