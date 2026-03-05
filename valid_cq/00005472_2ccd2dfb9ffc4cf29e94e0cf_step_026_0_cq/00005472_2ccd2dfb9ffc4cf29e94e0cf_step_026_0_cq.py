import cadquery as cq

# --- Parametric Dimensions ---
shelf_length = 800.0  # Total length of the shelf
shelf_depth = 250.0   # Depth of the shelf
shelf_thickness = 18.0 # Thickness of the main board

rail_width = 15.0      # Width of the support rail
rail_height = 25.0     # Height of the support rail
rail_thickness = 2.0   # Wall thickness of the rail profile
rail_offset_y = 10.0   # Offset from the front edge

screw_diam = 3.5
screw_len = 20.0
screw_head_diam = 7.0
screw_head_h = 2.5

bracket_width = 15.0
bracket_len = 40.0
bracket_thickness = 2.0

# --- Geometry Construction ---

# 1. Main Shelf Board
# A simple rectangular box
shelf = cq.Workplane("XY").box(shelf_length, shelf_depth, shelf_thickness)

# 2. Front Support Rail
# A U-channel or hollow rectangular tube located under the front edge
# Let's model a C-channel or tube. Looking at the image, it seems like a rectangular tube.
rail_outer = cq.Workplane("YZ").rect(rail_height, rail_width).extrude(shelf_length)
rail_inner = cq.Workplane("YZ").rect(rail_height - 2*rail_thickness, rail_width - 2*rail_thickness).extrude(shelf_length)
rail = rail_outer.cut(rail_inner)

# Position the rail under the front edge
# The shelf is centered at (0,0,0), so front edge is at y = -shelf_depth/2
# Bottom of shelf is at z = -shelf_thickness/2
rail_y_pos = -shelf_depth/2 + rail_width/2 + rail_offset_y
rail_z_pos = -shelf_thickness/2 - rail_height/2
rail = rail.translate((0, rail_y_pos, rail_z_pos))
rail = rail.rotate((0,0,0), (0,1,0), 90) # Rotate to align with X axis
# Fix rotation artifact: the extrusion was along normal, which was X for YZ plane, so it's already aligned with X.
# But default center is (0,0,0). Let's re-center properly.
# Actually, creating on YZ and extruding creates along X.
# Centering: box centers at origin.
# We need to move it so it aligns with the shelf length.
rail = rail.translate((-shelf_length/2, 0, 0)) # Move start to correct X, if extrusion started at 0
# Actually, let's rebuild rail more simply relative to global coords
rail = (
    cq.Workplane("YZ")
    .rect(rail_width, rail_height)
    .rect(rail_width - 2*rail_thickness, rail_height - 2*rail_thickness)
    .extrude(shelf_length)
)
# The extrusion goes into positive X. Shelf is centered on X.
# Move rail to center on X
rail = rail.translate((-shelf_length/2, -shelf_depth/2 + rail_offset_y + rail_width/2, -shelf_thickness/2 - rail_height/2))

# 3. Small Hardware (Screws/Dowels)
# The image shows some small loose parts on the left.
# Let's add a couple of generic screw shapes near the end of the rail to represent the hardware shown.

def create_screw():
    s = cq.Workplane("XY").circle(screw_head_diam/2).extrude(screw_head_h)
    shank = cq.Workplane("XY").circle(screw_diam/2).extrude(-screw_len)
    s = s.union(shank)
    return s

screw1 = create_screw().rotate((0,1,0), (0,0,0), -90).translate((-shelf_length/2 - 15, -shelf_depth/2 + rail_offset_y, -shelf_thickness/2 - 5))
screw2 = create_screw().rotate((0,1,0), (0,0,0), -90).translate((-shelf_length/2 - 15, -shelf_depth/2 + rail_offset_y + 10, -shelf_thickness/2 - 5))

# 4. Small Bracket/Insert
# There appears to be a small rectangular piece near the screws, likely an end cap or connector.
bracket = cq.Workplane("YZ").rect(rail_width - 1, rail_height - 1).extrude(5)
bracket = bracket.translate((-shelf_length/2 - 10, -shelf_depth/2 + rail_offset_y + rail_width/2, -shelf_thickness/2 - rail_height/2))

# --- Combine Assembly ---

result = shelf.union(rail).union(screw1).union(screw2).union(bracket)

# If you want to color/export, you would do it here, but the prompt asks for 'result' variable.