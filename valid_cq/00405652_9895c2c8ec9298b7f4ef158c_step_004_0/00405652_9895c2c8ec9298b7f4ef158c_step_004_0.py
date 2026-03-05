import cadquery as cq

# Parametric dimensions
total_height = 120.0
total_width = 40.0
max_depth = 30.0
web_thickness = 6.0
gap_height = 25.0
lower_wedge_height = 35.0

# Calculated vertical positions
upper_wedge_bottom_z = lower_wedge_height + gap_height

# Define the profile points on the YZ plane (Side view)
# (Y, Z) coordinates assuming origin at bottom-back corner
# Y is depth (thickness), Z is height
profile_pts = [
    (0, 0),                                      # Bottom-back corner
    (0, total_height),                           # Top-back corner
    (web_thickness, total_height),               # Top face front edge
    (max_depth, upper_wedge_bottom_z),           # Top wedge tip
    (web_thickness, upper_wedge_bottom_z),       # Top wedge undercut (inner corner)
    (web_thickness, lower_wedge_height),         # Bottom wedge top (inner corner)
    (max_depth, lower_wedge_height),             # Bottom wedge tip
    (web_thickness, 0)                           # Bottom face front edge
]

# Create the 3D model
result = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(total_width)
)