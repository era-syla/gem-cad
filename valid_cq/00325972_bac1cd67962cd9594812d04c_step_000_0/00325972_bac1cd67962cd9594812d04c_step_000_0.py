import cadquery as cq

# Parameter definitions
length = 100.0         # Total length of the bar
width = 30.0           # Total width of the base
base_height = 10.0     # Height of the rectangular base section
rail_height = 10.0     # Height of the trapezoidal rail above the base
top_width = 12.0       # Width of the flat top surface of the rail
flat_length = 35.0     # Length of the flat section at the back
ramp_length = 20.0     # Length of the ramp transition

# Side key parameters
key_length = 25.0
key_width = 6.0
key_height = 5.0
key_offset_ramp = 5.0  # Distance from end of ramp to start of key

# Derived parameters
total_height = base_height + rail_height
key_x_center = flat_length + ramp_length + key_offset_ramp + key_length / 2.0
key_z_center = base_height + key_height / 2.0
# Y position is calculated to ensure the key intersects the sloped face 
# and protrudes slightly.
# Approximate width of rail at key top height is ~10.5mm. 
# We position the key to penetrate this.
key_y_center = 13.0 

# 1. Create the main body extrusion
# We sketch the profile of the rail end (trapezoid on rectangle) on the YZ plane
# and extrude it along the X axis.
profile_pts = [
    (width / 2, 0),
    (width / 2, base_height),
    (top_width / 2, total_height),
    (-top_width / 2, total_height),
    (-width / 2, base_height),
    (-width / 2, 0)
]

main_body = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(length)
)

# 2. Create the cutter to form the flat section and the ramp
# The cutter is defined in the XZ plane. It removes material from the top 
# to create the lower flat section and the angled ramp.
cutter_pts = [
    (0, base_height),
    (flat_length, base_height),
    (flat_length + ramp_length, total_height),
    (flat_length + ramp_length, total_height + 10.0),  # Go high up to ensure full cut
    (0, total_height + 10.0)
]

cutter = (
    cq.Workplane("XZ")
    .polyline(cutter_pts)
    .close()
    .extrude(width + 10.0, both=True)  # Extrude wide enough to cut the entire width
)

# Apply the cut to the main body
base_shape = main_body.cut(cutter)

# 3. Create and add the side key
# The key is a rectangular block added to the side of the rail
key = (
    cq.Workplane("XY")
    .box(key_length, key_width, key_height)
    .translate((key_x_center, key_y_center, key_z_center))
)

# Combine to get the final result
result = base_shape.union(key)