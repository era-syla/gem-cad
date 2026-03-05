import cadquery as cq

# Parameter definitions
length = 120.0
width = 40.0
height = 40.0

# Section dimensions
shelf_length = 50.0
shelf_height = 20.0
mid_flat_length = 20.0
right_flat_length = 10.0

# Calculated dimensions for the V-groove
groove_start_x = shelf_length + mid_flat_length
groove_end_x = length - right_flat_length
groove_center_x = (groove_start_x + groove_end_x) / 2.0
groove_bottom_height = 20.0  # Bottom of V-groove aligns with shelf height

# Define profile points in XZ plane (Side View)
# Ordered counter-clockwise starting from origin
profile_points = [
    (0, 0),                                     # Bottom Left
    (length, 0),                                # Bottom Right
    (length, height),                           # Top Right
    (groove_end_x, height),                     # Top Right Flat End
    (groove_center_x, groove_bottom_height),    # V-Groove Bottom
    (groove_start_x, height),                   # V-Groove Start / Mid Flat End
    (shelf_length, height),                     # Mid Flat Start
    (shelf_length, shelf_height),               # Step Down Bottom
    (0, shelf_height)                           # Shelf Left End
]

# Generate the 3D model
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .extrude(width)
)