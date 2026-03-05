import cadquery as cq

# -- Parametric Dimensions --
# Base plate dimensions
plate_width = 100.0
plate_height = 240.0
plate_thickness = 15.0

# Top Hole Parameters (Tweeter position - smaller hole)
top_y_offset = 40.0
top_outer_dia = 65.0  # Counterbore diameter
top_inner_dia = 50.0  # Through hole diameter
top_cb_depth = 5.0    # Counterbore depth

# Bottom Hole Parameters (Woofer position - larger hole)
bot_y_offset = -30.0
bot_outer_dia = 90.0
bot_inner_dia = 75.0
bot_cb_depth = 5.0

# -- Modeling --

# 1. Create the base rectangular plate centered at the origin
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Cut the top counterbored hole
# Select the top face (+Z), create a workplane, move to position, and cut
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, top_y_offset)
    .cboreHole(top_inner_dia, top_outer_dia, top_cb_depth)
)

# 3. Cut the bottom counterbored hole
# Select the top face again to ensure operations are referenced from the surface
# The geometric engine handles the intersection of the counterbores automatically
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, bot_y_offset)
    .cboreHole(bot_inner_dia, bot_outer_dia, bot_cb_depth)
)