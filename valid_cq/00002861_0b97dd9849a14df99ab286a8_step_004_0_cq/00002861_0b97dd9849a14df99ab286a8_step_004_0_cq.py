import cadquery as cq

# Define parameters for the shape
# These values are estimated based on the visual proportions of the image
overall_length = 100.0
left_width = 60.0    # Width at the larger end
right_width = 30.0   # Width at the smaller end
thickness = 10.0

# Notch dimensions
notch_size = 10.0    # Size of the corner cutouts (roughly square)

# Calculate key points for the polygon profile
# We will draw the main trapezoidal shape first and then cut the corners, 
# or draw the complete profile point-by-point.
# Let's draw the complete profile point-by-point for precision.

# Center the shape roughly around the origin
half_len = overall_length / 2.0
half_left = left_width / 2.0
half_right = right_width / 2.0

# Define points starting from top-left, going clockwise
# Top edge (slanted)
p1 = (-half_len, half_left - notch_size)         # Top-Left inner corner
p2 = (-half_len + notch_size, half_left - notch_size) # Top-Left notch horizontal
p3 = (-half_len + notch_size, half_left)         # Top-Left notch vertical (wait, looking at image, it's cut *into* the shape)

# Let's rethink the strategy:
# 1. Create a base trapezoid.
# 2. Cut rectangular notches out of the four corners.

# Strategy 2: Base Trapezoid + Cuts
# Create the base sketch
sketch = (
    cq.Workplane("XY")
    .moveTo(-half_len, -half_left)
    .lineTo(-half_len, half_left)
    .lineTo(half_len, half_right)
    .lineTo(half_len, -half_right)
    .close()
    .extrude(thickness)
)

# Now apply the corner cuts
# The image shows "stepped" corners.
# Left side corners (wider end)
# Top-Left notch
sketch = sketch.cut(
    cq.Workplane("XY")
    .rect(notch_size * 2, notch_size * 2) # Create a rect centered at origin
    .translate((-half_len, half_left, 0)) # Move to corner
    .extrude(thickness)
)

# Bottom-Left notch
sketch = sketch.cut(
    cq.Workplane("XY")
    .rect(notch_size * 2, notch_size * 2)
    .translate((-half_len, -half_left, 0))
    .extrude(thickness)
)

# Right side corners (narrower end)
# Top-Right notch
sketch = sketch.cut(
    cq.Workplane("XY")
    .rect(notch_size * 2, notch_size * 2)
    .translate((half_len, half_right, 0))
    .extrude(thickness)
)

# Bottom-Right notch
sketch = sketch.cut(
    cq.Workplane("XY")
    .rect(notch_size * 2, notch_size * 2)
    .translate((half_len, -half_right, 0))
    .extrude(thickness)
)

# Alternative Strategy: Polyline (Cleaner and more parametric for a single sketch)
# Let's rebuild using a single polyline definition which is more robust.

# Define vertices based on the visual features:
# It's a symmetric shape along the X-axis (if viewed from top).
# Let's define the top half points and mirror or just define all points.

# Points counter-clockwise starting from left-bottom notch inner corner
pts = [
    # Bottom Left Notch
    (-half_len + notch_size, -half_left),
    (-half_len + notch_size, -half_left + notch_size),
    (-half_len, -half_left + notch_size),
    
    # Left Edge
    (-half_len, half_left - notch_size),
    
    # Top Left Notch
    (-half_len + notch_size, half_left - notch_size),
    (-half_len + notch_size, half_left),
    
    # Top Edge (Slanted)
    (half_len - notch_size, half_right),
    
    # Top Right Notch
    (half_len - notch_size, half_right - notch_size),
    (half_len, half_right - notch_size),
    
    # Right Edge
    (half_len, -half_right + notch_size),
    
    # Bottom Right Notch
    (half_len - notch_size, -half_right + notch_size),
    (half_len - notch_size, -half_right)
]

# Create the final result using the polyline method
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)