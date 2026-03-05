import cadquery as cq

# --- Parameters ---
# Table Top Dimensions
table_length = 1800.0
table_width = 900.0
table_height = 750.0
top_thickness = 50.0
front_curve_depth = 120.0  # Indent depth for the front edge

# Frame/Leg Dimensions
leg_spacing = 1000.0       # Distance between the two leg frames
leg_width_top = 700.0      # Width of the trapezoid at the top
leg_width_bottom = 500.0   # Width of the trapezoid at the bottom
tube_size = 40.0           # Size of the square metal tubing

# --- 1. Create Table Top ---
# Define points for the top profile on the XY plane
# The front edge (-Y) will have a concave curve
p_back_left = (-table_length / 2.0, table_width / 2.0)
p_back_right = (table_length / 2.0, table_width / 2.0)
p_front_right = (table_length / 2.0, -table_width / 2.0)
p_front_left = (-table_length / 2.0, -table_width / 2.0)
# Midpoint for the arc, indented towards the center
p_front_mid = (0.0, -table_width / 2.0 + front_curve_depth)

# Create the sketch for the top
top_sketch = (
    cq.Sketch()
    .segment(p_back_left, p_back_right)   # Back edge
    .segment(p_front_right)               # Right edge
    .arc(p_front_mid, p_front_left)       # Front curved edge
    .close()
    .assemble()
)

# Extrude the top
table_top = (
    cq.Workplane("XY", origin=(0, 0, table_height - top_thickness))
    .placeSketch(top_sketch)
    .extrude(top_thickness)
)

# --- 2. Create Legs ---
# Calculated Z heights for the tube centerlines
z_tube_bottom = tube_size / 2.0
z_tube_top = table_height - top_thickness - (tube_size / 2.0)
leg_x_offset = leg_spacing / 2.0

# Define points for the trapezoidal leg path in the YZ plane
# We start at the bottom center to ensure the sweep profile aligns correctly
pts = [
    (0, z_tube_bottom),                         # Start: Bottom Center
    (-leg_width_bottom / 2.0, z_tube_bottom),   # Bottom Front
    (-leg_width_top / 2.0, z_tube_top),         # Top Front
    (leg_width_top / 2.0, z_tube_top),          # Top Back
    (leg_width_bottom / 2.0, z_tube_bottom),    # Bottom Back
    (0, z_tube_bottom)                          # Close Loop
]

# Create the path for the left leg
left_leg_path = (
    cq.Workplane("YZ", origin=(-leg_x_offset, 0, 0))
    .polyline(pts)
    .close()
)

# Sweep the square profile along the path
# Profile is defined on XZ plane to be perpendicular to the bottom horizontal segment of the path
left_leg = (
    cq.Workplane("XZ", origin=(-leg_x_offset, 0, z_tube_bottom))
    .rect(tube_size, tube_size)
    .sweep(left_leg_path, transition="right")
)

# Create the right leg by mirroring the left leg
right_leg = left_leg.mirror("YZ")

# --- 3. Create Bottom Connecting Bar ---
# Connects the bottom centers of the two leg loops
connecting_bar = (
    cq.Workplane("YZ", origin=(-leg_x_offset, 0, z_tube_bottom))
    .rect(tube_size, tube_size)
    .extrude(leg_spacing)  # Extrude along global X axis
)

# --- Combine Geometry ---
result = table_top.union(left_leg).union(right_leg).union(connecting_bar)