import cadquery as cq

# Define parametric dimensions for the object
total_length = 60.0
total_height = 40.0
thickness = 15.0

# Feature specific dimensions
back_top_flat_length = 15.0
notch_bottom_x = 30.0
notch_bottom_y = 20.0
front_peak_x = 15.0
front_peak_y = 30.0

# Define the profile vertices on the XZ plane
# Starting from the bottom-left corner and proceeding counter-clockwise
profile_points = [
    (0, 0),                                      # Bottom-left corner
    (total_length, 0),                           # Bottom-right corner
    (total_length, total_height),                # Top-right corner
    (total_length - back_top_flat_length, total_height), # Start of the back slope
    (notch_bottom_x, notch_bottom_y),            # Bottom vertex of the V-notch
    (front_peak_x, front_peak_y)                 # Top vertex of the front hook
]

# Generate the 3D solid
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .extrude(thickness)
)