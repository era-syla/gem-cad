import cadquery as cq
import math

# --- Parametric Dimensions ---

# Bottom Threaded Section
thread1_dia = 16.0
thread1_len = 35.0

# Mid Shaft Section
shaft_dia = 16.0
shaft_len = 40.0

# Keyway Parameters
key_width = 5.0
key_depth = 3.5
key_length = 25.0
key_offset_bottom = 5.0  # Distance from the start of the shaft section

# Hexagonal Collar Section
hex_width_flats = 24.0   # Wrench size
hex_height = 12.0

# Flange/Shoulder Section (above Hex)
flange_dia = 28.0
flange_height = 3.0

# Tapered Section
taper_base_dia = 24.0
taper_top_dia = 18.0
taper_height = 25.0

# Top Threaded Section
thread2_dia = 14.0
thread2_len = 20.0

# General Features
chamfer_size = 1.0

# --- Model Construction ---

# 1. Bottom Threaded Cylinder
# Create the base cylinder representing the threaded stud
result = (
    cq.Workplane("XY")
    .circle(thread1_dia / 2.0)
    .extrude(thread1_len)
)

# Chamfer the bottom edge
result = result.faces("<Z").chamfer(chamfer_size)

# 2. Middle Shaft Cylinder
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_dia / 2.0)
    .extrude(shaft_len)
)

# 3. Cut the Keyway
# Calculate position: centered vertically in the defined keyway area
# Z-height center relative to global origin
key_z_center = thread1_len + key_offset_bottom + (key_length / 2.0)

# Create a cutter box. We define it on a plane at the Z-center.
# We offset the box in X so it cuts into the shaft surface to the desired depth.
# Box X-center = (Radius - Depth) + (Box_Width / 2)
cutter_width_buffer = shaft_dia  # Large enough to clear the cut
cut_x_pos = (shaft_dia / 2.0) - key_depth + (cutter_width_buffer / 2.0)

key_cutter = (
    cq.Workplane("XY")
    .workplane(offset=key_z_center)
    .box(cutter_width_buffer, key_width, key_length)
    .translate((cut_x_pos, 0, 0))
)

result = result.cut(key_cutter)

# 4. Hexagonal Collar
# Calculate the circumdiameter for the polygon (across corners)
# Relation: Diameter_Corners = 2 * (Width_Flats / sqrt(3))
hex_circum_dia = 2 * (hex_width_flats / math.sqrt(3))

result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_circum_dia)
    .extrude(hex_height)
)

# 5. Circular Flange Shoulder
result = (
    result.faces(">Z")
    .workplane()
    .circle(flange_dia / 2.0)
    .extrude(flange_height)
)

# 6. Tapered Section
# Using loft to create the conical section
result = (
    result.faces(">Z")
    .workplane()
    .circle(taper_base_dia / 2.0)
    .workplane(offset=taper_height)
    .circle(taper_top_dia / 2.0)
    .loft(combine=True)
)

# 7. Top Threaded Cylinder
result = (
    result.faces(">Z")
    .workplane()
    .circle(thread2_dia / 2.0)
    .extrude(thread2_len)
)

# Chamfer the top edge
result = result.faces(">Z").chamfer(chamfer_size)

# The 'result' variable now contains the final solid geometry