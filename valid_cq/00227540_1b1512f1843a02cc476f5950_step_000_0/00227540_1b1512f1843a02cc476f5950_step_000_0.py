import cadquery as cq

# Parametric dimensions for the model
length = 100.0
width = 40.0
height_max = 60.0
height_left_wall = 30.0
height_right_wall = 45.0
height_notch_bottom = 35.0

# X-coordinates for the profile transitions
x_slope_top = 40.0      # End of the left main slope
x_flat_end = 55.0       # End of the top flat section / Start of V-notch
x_notch_bottom = 70.0   # Horizontal position of the V-notch bottom
x_notch_end = 85.0      # End of the V-notch / Start of right flat section

# Define the profile points counter-clockwise starting from origin (0,0)
# The profile is drawn on the XY plane (Front View equivalent)
pts = [
    (0, 0),                              # Bottom-Left
    (length, 0),                         # Bottom-Right
    (length, height_right_wall),         # Top-Right Wall Top
    (x_notch_end, height_right_wall),    # Right Flat End
    (x_notch_bottom, height_notch_bottom), # Bottom of V-Notch
    (x_flat_end, height_max),            # Top Flat End / V-Notch Start
    (x_slope_top, height_max),           # Top Flat Start / Slope Top
    (0, height_left_wall)                # Left Wall Top
]

# Generate the 3D model by creating the profile and extruding it
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(width)
)