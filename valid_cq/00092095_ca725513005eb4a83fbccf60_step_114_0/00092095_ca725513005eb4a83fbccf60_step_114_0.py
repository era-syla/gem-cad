import cadquery as cq
import math

# --- Parametric Dimensions ---
pitch = 32.0            # Distance between the centers of the hole patterns
width = 32.0            # Width of the beam (diameter of the rounded ends)
thickness = 2.5         # Thickness of the part
num_patterns = 3        # Number of repeating patterns

# Hole dimensions (based on standard robotics grid patterns)
center_hole_dia = 14.0  # Diameter of the large central hole
small_hole_dia = 4.0    # Diameter of the small surrounding holes
bolt_circle_dia = 24.0  # Diameter of the circle on which small holes are arranged
num_small_holes = 8     # Number of small holes per pattern

# --- Geometry Generation ---

# Calculate total length of the stadium shape (tip-to-tip)
# Length = distance between outer centers + width (radius * 2)
total_length = (num_patterns - 1) * pitch + width

# Create the base solid (stadium/slot shape)
result = (
    cq.Workplane("XY")
    .slot2D(total_length, width)
    .extrude(thickness)
)

# Calculate the center coordinates for each pattern
# The part is centered at (0,0), so we calculate offsets relative to center
start_x = -((num_patterns - 1) * pitch) / 2.0
pattern_centers = [(start_x + i * pitch, 0) for i in range(num_patterns)]

# Cut the large central holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pattern_centers)
    .hole(center_hole_dia)
)

# Generate coordinates for all small holes
# We pre-calculate these to perform a single efficient cut operation
small_hole_points = []
bc_radius = bolt_circle_dia / 2.0

for cx, cy in pattern_centers:
    for i in range(num_small_holes):
        angle_rad = math.radians(i * (360.0 / num_small_holes))
        sx = cx + bc_radius * math.cos(angle_rad)
        sy = cy + bc_radius * math.sin(angle_rad)
        small_hole_points.append((sx, sy))

# Cut the small surrounding holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(small_hole_points)
    .hole(small_hole_dia)
)