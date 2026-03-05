import cadquery as cq

# Parameters for the base plate
thickness = 2.0
width_top = 80.0
width_wing_max = 130.0
width_wing_min = 100.0
width_cutout = 30.0

y_top = 25.0
y_wing_top = 5.0
y_cutout_top = -10.0
y_bottom = -30.0

# Derived X coordinates
x_t = width_top / 2.0
x_w_max = width_wing_max / 2.0
x_w_min = width_wing_min / 2.0
x_c = width_cutout / 2.0

# Polyline points defining the outer profile (clockwise starting from top-left)
pts = [
    (-x_t, y_top),
    (x_t, y_top),
    (x_t, y_wing_top),
    (x_w_max, y_wing_top),
    (x_w_min, y_bottom),
    (x_c, y_bottom),
    (x_c, y_cutout_top),
    (-x_c, y_cutout_top),
    (-x_c, y_bottom),
    (-x_w_min, y_bottom),
    (-x_w_max, y_wing_top),
    (-x_t, y_wing_top)
]

# Create the base extruded shape
plate = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# Define hole locations based on visual features
large_holes_pts = [(-10, 0), (10, 0)]
small_holes_pts = [
    (-20, 15),   # Top left
    (-35, 2),    # Mid left
    (20, -15),   # Bottom right leg
    (48, 2)      # Right wing
]

# Apply cuts for large holes
result = (
    plate.faces(">Z").workplane()
    .pushPoints(large_holes_pts)
    .circle(4.0)
    .cutThruAll()
)

# Apply cuts for small holes
result = (
    result.faces(">Z").workplane()
    .pushPoints(small_holes_pts)
    .circle(1.5)
    .cutThruAll()
)