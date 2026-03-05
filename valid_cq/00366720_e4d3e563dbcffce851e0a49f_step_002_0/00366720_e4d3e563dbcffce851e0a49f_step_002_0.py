import cadquery as cq

# -- Parameters --
thickness = 2.0       # Thickness of the plate
width_max = 140.0     # Maximum width of the plate (at the widest point)
height = 80.0         # Total vertical height (depth) of the plate
front_flat = 40.0     # Width of the flat bottom edge
corner_height = 15.0  # Vertical distance from bottom to the widest corners
notch_width = 24.0    # Total width of the top notch tips
notch_depth = 12.0    # Vertical depth of the V-notch

# -- Calculation of coordinates --
# We assume the bottom flat edge is centered on the X-axis at Y=0
x_flat = front_flat / 2.0
x_corner = width_max / 2.0
x_top = notch_width / 2.0
y_top = height
y_notch_bottom = height - notch_depth

# Define points clockwise from the top notch center
points = [
    (0, y_notch_bottom),          # Center bottom of the V-notch
    (x_top, y_top),               # Top right tip
    (x_corner, corner_height),    # Right corner (widest point)
    (x_flat, 0),                  # Bottom right of flat edge
    (-x_flat, 0),                 # Bottom left of flat edge
    (-x_corner, corner_height),   # Left corner
    (-x_top, y_top)               # Top left tip
]

# -- Geometry Generation --
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)