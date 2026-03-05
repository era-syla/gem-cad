import cadquery as cq
import math

# --- Parameters ---
plate_length = 130.0
plate_width = 80.0
plate_thickness = 10.0

# Semi-circular cutout on the right
cutout_radius = 20.0

# Small hole pattern parameters
bolt_circle_radius = 32.0
small_hole_diameter = 6.0
small_hole_count = 5

# Large hole on the left
large_hole_diameter = 16.0
large_hole_edge_offset = 20.0

# --- Modeling ---

# 1. Create Base Plate
# We create a box centered at the origin, then translate it so the right edge 
# lies on the Y-axis (X=0). This makes positioning the cutout easier.
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)
result = result.translate((-plate_length / 2.0, 0, 0))

# 2. Main Semi-Circular Cutout
# Since the right edge is at X=0, we draw a circle at (0,0) and cut through.
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, 0)
    .circle(cutout_radius)
    .cutThruAll()
)

# 3. Small Holes Pattern
# Calculate coordinates for the holes arranged in a semi-circle (180 degrees)
# The plate is on the -X side, so angles run from 90 (top) to 270 (bottom).
# Angles: 90, 135, 180, 225, 270
hole_points = []
start_angle = 90
end_angle = 270
angle_step = (end_angle - start_angle) / (small_hole_count - 1)

for i in range(small_hole_count):
    angle_deg = start_angle + i * angle_step
    angle_rad = math.radians(angle_deg)
    # Convert polar to cartesian
    hx = bolt_circle_radius * math.cos(angle_rad)
    hy = bolt_circle_radius * math.sin(angle_rad)
    hole_points.append((hx, hy))

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(small_hole_diameter)
)

# 4. Single Large Hole
# Located near the far left edge of the plate.
# The far left edge is at x = -plate_length.
large_hole_x = -plate_length + large_hole_edge_offset
large_hole_y = 0

result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(large_hole_x, large_hole_y)
    .hole(large_hole_diameter)
)