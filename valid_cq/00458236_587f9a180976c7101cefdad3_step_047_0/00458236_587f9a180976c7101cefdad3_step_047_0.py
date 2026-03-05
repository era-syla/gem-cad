import cadquery as cq

# Parametric dimensions for a standard 2020 aluminum extrusion profile
length = 400.0          # Total length of the extrusion
profile_size = 20.0     # Width/Height of the profile
fillet_radius = 1.0     # Radius of the outer corners
center_hole_dia = 5.0   # Diameter of the central hole

# T-Slot dimensions
slot_opening = 6.0      # Width of the slot opening
slot_depth_neck = 1.8   # Depth of the narrow opening part
slot_width_inner = 10.0 # Width of the inner cavity
slot_depth_inner = 4.0  # Depth of the inner cavity

# Define the coordinates for a single T-slot cutout (top side)
# Coordinates are relative to the profile center (0,0)
half_size = profile_size / 2.0
half_open = slot_opening / 2.0
half_inner = slot_width_inner / 2.0

# Points tracing the void of the T-slot
slot_points = [
    (half_open, half_size),
    (half_open, half_size - slot_depth_neck),
    (half_inner, half_size - slot_depth_neck),
    (half_inner, half_size - slot_depth_neck - slot_depth_inner),
    (-half_inner, half_size - slot_depth_neck - slot_depth_inner),
    (-half_inner, half_size - slot_depth_neck),
    (-half_open, half_size - slot_depth_neck),
    (-half_open, half_size)
]

# Create the 2D profile sketch
sketch = cq.Sketch()

# 1. Base square with rounded corners
sketch = sketch.rect(profile_size, profile_size)
sketch = sketch.vertices().fillet(fillet_radius)

# 2. Subtract the center hole
sketch = sketch.circle(center_hole_dia / 2.0, mode='s')

# 3. Subtract the T-slots on all 4 sides
current_points = slot_points
for _ in range(4):
    sketch = sketch.polygon(current_points, mode='s')
    # Rotate points 90 degrees counter-clockwise for the next side: (x, y) -> (-y, x)
    current_points = [(-y, x) for x, y in current_points]

# Extrude the sketch to create the 3D solid
result = cq.Workplane("XY").placeSketch(sketch).extrude(length)