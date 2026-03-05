import cadquery as cq

# Parameters
plate_length = 120.0  # Overall length of the plate (X-axis)
plate_width = 80.0    # Overall width of the plate (Y-axis)
plate_thickness = 5.0 # Thickness of the plate (Z-axis)

# Hole Parameters
hole_diameter = 4.5
csk_diameter = 8.0    # Countersink diameter
csk_angle = 90.0      # Countersink angle

# Hole Pattern Layout
# Based on visual inspection, there is symmetry and grouped holes.
# Group 1: Outer corners
x_outer = 50.0 # Distance from center
y_outer = 30.0 # Distance from center

# Group 2: Inner corners (closer to center in X)
x_inner = 35.0
y_inner = 30.0

# Group 3: Mid-width sets (offset in Y)
# There are two rows slightly inboard from the edge
x_mid = 15.0
y_mid_outer = 25.0
y_mid_inner = 10.0 # This doesn't look quite right, let's re-evaluate the pattern.

# Re-evaluating the pattern:
# It looks like a standard mounting plate, perhaps for a V-slot gantry or stepper motor mount.
# Let's define the coordinates explicitly based on typical symmetries.

# List of (x, y) coordinates relative to the center
# 1. The four outermost corners
pts_outer_corners = [
    (50, 30), (50, -30), (-50, 30), (-50, -30)
]

# 2. The four inner corners (aligned in Y with outer, but closer in X)
pts_inner_corners = [
    (30, 30), (30, -30), (-30, 30), (-30, -30)
]

# 3. The inner group of 8 holes
# These look like they might be for wheel mounts (eccentric spacers usually).
# Top row inner
pts_top_inner = [
    (20, 15), (-20, 15)
]
# Bottom row inner
pts_bottom_inner = [
    (20, -15), (-20, -15)
]
# Top row outer (within the inner cluster)
pts_top_outer = [
    (35, 15), (-35, 15)
]
# Bottom row outer (within the inner cluster)
pts_bottom_outer = [
    (35, -15), (-35, -15)
]

# Let's simplify the coordinate generation.
# Visually:
# Row 1 (Top, Y~30): x at +/- 30, +/- 50 (4 holes)
# Row 2 (Top-Mid, Y~15): x at +/- 20, +/- 35 (4 holes)
# Row 3 (Bottom-Mid, Y~-15): x at +/- 20, +/- 35 (4 holes)
# Row 4 (Bottom, Y~-30): x at +/- 30, +/- 50 (4 holes)

hole_locations = [
    # Top Row
    (50, 30), (30, 30), (-30, 30), (-50, 30),
    # Top-Mid Row
    (35, 15), (20, 15), (-20, 15), (-35, 15),
    # Bottom-Mid Row
    (35, -15), (20, -15), (-20, -15), (-35, -15),
    # Bottom Row
    (50, -30), (30, -30), (-30, -30), (-50, -30)
]

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)