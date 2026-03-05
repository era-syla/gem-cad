import cadquery as cq
import math

# Parameters for a standard 2020 T-Slot Aluminum Profile
length = 400.0      # Length of the extrusion
width = 20.0        # Width/Height of the profile
corner_radius = 1.5 # Radius of the outer corners
center_hole_dia = 5.0 # Diameter of the central hole

# T-Slot dimensions (approximate for standard 2020 profile)
slot_opening = 6.2  # Width of the slot opening
slot_depth = 6.0    # Total depth of the slot
slot_inner_w = 9.0  # Width of the inner cavity
lip_thickness = 1.5 # Thickness of the retaining lip

# Helper variables
half_width = width / 2.0

# 1. Initialize Sketch
# Start with the main square body and fillet the corners
sketch = (
    cq.Sketch()
    .rect(width, width)
    .vertices()
    .fillet(corner_radius)
)

# 2. Define the T-Slot Cutout Shape
# Coordinates for the slot on the top face (Y+), centered on X
# The shape traces the void to be removed
slot_points = [
    (slot_opening / 2, half_width),
    (slot_opening / 2, half_width - lip_thickness),
    (slot_inner_w / 2, half_width - lip_thickness),
    (slot_inner_w / 2, half_width - slot_depth),
    (-slot_inner_w / 2, half_width - slot_depth),
    (-slot_inner_w / 2, half_width - lip_thickness),
    (-slot_opening / 2, half_width - lip_thickness),
    (-slot_opening / 2, half_width)
]

# 3. Apply Cuts for all 4 sides
# We rotate the slot points 90 degrees 4 times and subtract ('s' mode) from the sketch
for i in range(4):
    angle_rad = math.radians(i * 90)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    rotated_points = []
    for x, y in slot_points:
        # 2D Rotation transformation
        rx = x * cos_a - y * sin_a
        ry = x * sin_a + y * cos_a
        rotated_points.append((rx, ry))
    
    sketch = sketch.polygon(rotated_points, mode='s')

# 4. Cut the Central Hole
sketch = sketch.circle(center_hole_dia / 2, mode='s')

# 5. Extrude to create the 3D object
result = cq.Workplane("XY").placeSketch(sketch).extrude(length)