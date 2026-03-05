import cadquery as cq

# Parameters
length = 100.0
height = 50.0
thickness = 15.0
top_length = 60.0
left_height = 15.0

# Define the points for the profile
# Starting from bottom-left corner
pts = [
    (0, 0),                                # Bottom-left
    (length, 0),                           # Bottom-right
    (length, height),                      # Top-right
    (length - top_length, height),         # Top-left of flat top
    (0, left_height)                       # Top of the vertical left side
]

# Create the 3D model
result = cq.Workplane("front").polyline(pts).close().extrude(thickness)