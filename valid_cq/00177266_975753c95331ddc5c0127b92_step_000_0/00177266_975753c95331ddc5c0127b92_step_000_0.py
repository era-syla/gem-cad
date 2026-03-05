import cadquery as cq

# Dimensions
length = 140.0
height_left = 35.0
height_right = 20.0
thickness = 12.0
step_x = 50.0  # Distance from the left end to the vertical step

# Chamfer dimensions (width along X, height along Y)
chamfer_left_w = 20.0
chamfer_left_h = 20.0
chamfer_right_w = 15.0
chamfer_right_h = 10.0

# Hole configuration
hole_dia = 8.0
# Hole positions defined relative to the Top-Left origin (0,0)
hole_left_pos = (20.0, -height_left / 2.0)
hole_right_pos = (length - 15.0, -height_right / 2.0)

# Define the profile vertices
# Coordinate system: Origin at Top-Left, +X is right, -Y is down
pts = [
    (0, 0),                                           # Top-Left corner
    (length, 0),                                      # Top-Right corner
    (length, -(height_right - chamfer_right_h)),      # Start of right chamfer
    (length - chamfer_right_w, -height_right),        # End of right chamfer
    (step_x, -height_right),                          # Bottom edge of right section
    (step_x, -height_left),                           # Step down to left section depth
    (chamfer_left_w, -height_left),                   # Bottom edge of left section
    (0, -(height_left - chamfer_left_h))              # End of left chamfer
]

# Create the 3D solid
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    .faces(">Z")  # Select the top face (relative to extrusion)
    .workplane(centerOption="ProjectedOrigin")  # Use projected origin to maintain X,Y coords
    .pushPoints([hole_left_pos, hole_right_pos])
    .hole(hole_dia)
)