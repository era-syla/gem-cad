import cadquery as cq
import math

# --- Parameters ---
# Overall Dimensions
plate_width = 140.0       # The dimension between the two straight edges (Y-axis)
waist_length = 150.0      # The narrowest length of the plate (X-axis, at center)
thickness = 6.0           # Plate thickness
cutout_radius = 85.0      # Radius of the concave cutouts on the sides
fillet_radius = 12.0      # Radius of the corner fillets

# Hole Configuration
hole_diameter = 4.2       # Diameter of mounting holes
hole_count = 5            # Number of holes per straight edge
hole_spacing = 40.0       # Spacing between holes
hole_margin = 10.0        # Distance from the hole center to the straight edge

# --- Geometry Calculation ---
# Calculate the center position of the cutout circles.
# We want the circle to be tangent to the waist at x = +/- waist_length/2.
# Since the cut is from the outside, the center is shifted outwards by the radius.
cutout_center_x = (waist_length / 2.0) + cutout_radius

# Calculate the precise length of the base box.
# The box corners should align with the intersection of the cutout circle and the top/bottom edges.
# Circle Equation: (x - cx)^2 + y^2 = r^2
# Solve for x at y = plate_width/2:
# x = cx - sqrt(r^2 - (w/2)^2)
intersection_offset = math.sqrt(cutout_radius**2 - (plate_width / 2.0)**2)
box_length = 2.0 * (cutout_center_x - intersection_offset)

# --- Modeling ---

# 1. Create the base rectangular plate
result = cq.Workplane("XY").box(box_length, plate_width, thickness)

# 2. Cut the side profiles
# We create cylinders positioned to cut out the concave shapes from the left and right ends.
cutter_right = (
    cq.Workplane("XY")
    .workplane(offset=-thickness)
    .moveTo(cutout_center_x, 0)
    .circle(cutout_radius)
    .extrude(thickness * 3)
)

cutter_left = (
    cq.Workplane("XY")
    .workplane(offset=-thickness)
    .moveTo(-cutout_center_x, 0)
    .circle(cutout_radius)
    .extrude(thickness * 3)
)

result = result.cut(cutter_right).cut(cutter_left)

# 3. Fillet the corners
# Select vertical edges (parallel to Z) to apply fillets to the sharp corners created by the cut.
result = result.edges("|Z").fillet(fillet_radius)

# 4. Add Mounting Holes
# Calculate hole positions
hole_y = (plate_width / 2.0) - hole_margin
hole_x_start = -((hole_count - 1) * hole_spacing) / 2.0

hole_points = []
for i in range(hole_count):
    x_pos = hole_x_start + (i * hole_spacing)
    # Add top row point
    hole_points.append((x_pos, hole_y))
    # Add bottom row point
    hole_points.append((x_pos, -hole_y))

# Drill the holes
result = result.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)