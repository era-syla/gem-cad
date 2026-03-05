import cadquery as cq

# Parameters defining the handle geometry
length = 120.0       # Total length of the handle
depth = 40.0         # Depth from the mounting surface
height = 15.0        # Vertical height (thickness in Z)
thickness = 15.0     # Wall thickness of the handle
fillet_radius = 15.0 # Radius for the outer corners

# Calculate coordinates for the profile
# We center the handle on the X axis, with the front face at Y=0
x_outer = length / 2.0
x_inner = x_outer - thickness
y_back = depth
y_front = 0.0
y_inner_front = thickness

# Define the points for the U-shaped profile (top-down view)
# Starting from the back-left leg and moving counter-clockwise
points = [
    (-x_outer, y_back),          # Back-left outer
    (-x_outer, y_front),         # Front-left outer
    (x_outer, y_front),          # Front-right outer
    (x_outer, y_back),           # Back-right outer
    (x_inner, y_back),           # Back-right inner
    (x_inner, y_inner_front),    # Front-right inner
    (-x_inner, y_inner_front),   # Front-left inner
    (-x_inner, y_back)           # Back-left inner
]

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(height)
    # Select the vertical edges (|Z) at the front of the object (<Y) to fillet
    .edges("|Z").edges("<Y")
    .fillet(fillet_radius)
)