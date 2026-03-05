import cadquery as cq

# Define parametric dimensions
total_width = 40.0
total_depth = 15.0
bottom_height = 20.0
neck_height = 15.0
top_height = 45.0
neck_width = 14.0

# Calculate coordinate offsets
half_width = total_width / 2.0
half_neck = neck_width / 2.0

# Vertical Y coordinates for the profile sketch
y_bottom_top = bottom_height
y_neck_top = bottom_height + neck_height
y_total = bottom_height + neck_height + top_height

# Define the profile points (XZ plane) for the "I" shape
# Starting from bottom-left corner and moving counter-clockwise
profile_points = [
    (-half_width, 0),                 # Bottom-left corner
    (half_width, 0),                  # Bottom-right corner
    (half_width, y_bottom_top),       # Bottom section top-right
    (half_neck, y_bottom_top),        # Neck inner corner right-bottom
    (half_neck, y_neck_top),          # Neck inner corner right-top
    (half_width, y_neck_top),         # Top section bottom-right
    (half_width, y_total),            # Top-right corner
    (-half_width, y_total),           # Top-left corner
    (-half_width, y_neck_top),        # Top section bottom-left
    (-half_neck, y_neck_top),         # Neck inner corner left-top
    (-half_neck, y_bottom_top),       # Neck inner corner left-bottom
    (-half_width, y_bottom_top)       # Bottom section top-left
]

# Generate the solid model
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .extrude(total_depth)
)