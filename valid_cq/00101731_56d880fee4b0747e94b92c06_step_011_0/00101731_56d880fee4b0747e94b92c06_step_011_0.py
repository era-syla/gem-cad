import cadquery as cq

# ==========================================
# Parameters
# ==========================================

# Main Body Dimensions
body_dia = 12.0
body_length = 40.0
cut_angle = 45.0  # Angle of the front face relative to the cylinder axis

# Rear Groove Dimensions
groove_offset = 8.0  # Distance from the back face
groove_width = 0.8
groove_depth = 0.5

# Cable Connector / Stem Dimensions
stem_x_pos = 4.0     # Distance from the back face
stem_dia = 1.5
stem_length = 25.0
hex_width = 4.0      # Width across flats
hex_height = 2.0

# Connector Head Dimensions
head_dia = 5.0
head_height = 3.5
slot_width = 1.0
slot_depth = 1.2
hole_dia = 1.5

# ==========================================
# 3D Modeling Construction
# ==========================================

# 1. Main Cylinder Body
# Create the main cylinder along the X-axis, starting at X=0
main_body = cq.Workplane("YZ").circle(body_dia / 2.0).extrude(body_length)

# 2. Angled Cut
# Define a cutting plane anchored at the bottom-front tip of the cylinder.
# This ensures the bottom length remains 'body_length' while the top is cut shorter.
cut_origin = (body_length, 0, -body_dia / 2.0)

# Create a workplane rotated to the cut angle. 
# Rotation about Y-axis (-45 deg) tilts the normal Up and Back towards the cylinder.
cutter_plane = cq.Workplane("YZ", origin=cut_origin).transformed(rotate=(0, -cut_angle, 0))

# Create a large block to subtract the material
# Extruding along the plane's normal (outwards) defines the volume to remove.
cutter_solid = cutter_plane.rect(body_dia * 4, body_dia * 4).extrude(body_length)

# Apply the cut
main_body = main_body.cut(cutter_solid)

# 3. Rear Groove
# Create a ring-shaped tool to subtract the groove
groove_tool = cq.Workplane("YZ", origin=(groove_offset, 0, 0)) \
    .circle(body_dia / 2.0 + 1.0) \
    .circle(body_dia / 2.0 - groove_depth) \
    .extrude(groove_width)

main_body = main_body.cut(groove_tool)

# 4. Connector Assembly (Hex Base + Rod + Head)

# Calculate the mounting point on the cylinder surface (Top/Z-positive side)
mount_point = (stem_x_pos, 0, body_dia / 2.0)

# Hex Nut Base
hex_base = cq.Workplane("XY", origin=mount_point) \
    .polygon(6, hex_width).extrude(hex_height)

# Vertical Rod
rod_start_z = body_dia / 2.0 + hex_height
rod = cq.Workplane("XY", origin=(stem_x_pos, 0, rod_start_z)) \
    .circle(stem_dia / 2.0).extrude(stem_length)

# Head Cylinder
head_start_z = rod_start_z + stem_length
head_base = cq.Workplane("XY", origin=(stem_x_pos, 0, head_start_z)) \
    .circle(head_dia / 2.0).extrude(head_height)

# 5. Head Details (Slot and Hole)
# Workplane at the top of the head
head_top_z = head_start_z + head_height
head_tool_plane = cq.Workplane("XY", origin=(stem_x_pos, 0, head_top_z))

# Create solids for the slot and central hole to subtract
slot_tool = head_tool_plane.rect(head_dia * 2, slot_width).extrude(-slot_depth)
hole_tool = head_tool_plane.circle(hole_dia / 2.0).extrude(-head_height)

# Apply details to the head
head_final = head_base.cut(slot_tool).cut(hole_tool)

# Add chamfers to the head for detail (Top and Bottom edges of the cylinder)
try:
    head_final = head_final.edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.2)
except:
    pass # Fail gracefully if selection is ambiguous

# 6. Final Assembly
result = main_body.union(hex_base).union(rod).union(head_final)