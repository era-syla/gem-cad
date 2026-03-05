import cadquery as cq

# Parametric dimensions based on visual estimation of the V-block shape
# All units assumed to be millimeters
h_left_leg = 60.0       # Height of the vertical left leg
notch_x = 30.0          # X position of the bottom of the V-notch
notch_y = 30.0          # Y position of the bottom of the V-notch (height of the valley)
tip_inner_x = 80.0      # X position of the inner top tip of the right leg
tip_inner_y = 90.0      # Y position of the inner top tip of the right leg
tip_outer_x = 100.0     # X position of the outer top tip of the right leg
tip_outer_y = 70.0      # Y position of the outer top tip of the right leg
base_width = 40.0       # Width of the flat base on the X axis
thickness = 30.0        # Extrusion depth

# Define the vertices of the profile polygon
# Starting from origin (bottom-left) and moving counter-clockwise
profile_points = [
    (0, 0),                       # Bottom-left corner
    (0, h_left_leg),              # Top-left corner
    (notch_x, notch_y),           # Bottom of the V-notch
    (tip_inner_x, tip_inner_y),   # Inner peak of the right leg
    (tip_outer_x, tip_outer_y),   # Outer peak of the right leg
    (base_width, 0)               # Bottom point where right leg meets base line
]

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .polyline(profile_points)
    .close()
    .extrude(thickness)
)