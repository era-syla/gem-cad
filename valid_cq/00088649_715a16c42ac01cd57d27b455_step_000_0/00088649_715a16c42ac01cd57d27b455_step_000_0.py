import cadquery as cq

# -- Parametric Dimensions --
# Main body dimensions
body_width = 40.0
body_depth = 20.0
body_height = 80.0

# Antenna dimensions
ant_base_radius = 3.5
ant_base_height = 5.0
ant_mast_radius = 2.0
ant_mast_height = 35.0
ant_offset_x = 12.0  # Distance from center along width

# Middle Knob dimensions
knob_radius = 2.5
knob_height = 3.0
knob_offset_x = -3.0

# Left Button dimensions
btn_radius = 2.0
btn_height = 2.0
btn_offset_x = -13.0

# -- Modeling --

# 1. Main Body
# Create the rectangular prism centered at the origin
# Top face will be at Z = body_height / 2
main_body = cq.Workplane("XY").box(body_width, body_depth, body_height)

# Calculate the Z level for the top face
top_z = body_height / 2.0

# 2. Antenna
# Constructed separately and unioned later to ensure robust selection
antenna = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .center(ant_offset_x, 0)
    .circle(ant_base_radius)
    .extrude(ant_base_height)
    .faces(">Z").workplane()  # Select top of the base
    .circle(ant_mast_radius)
    .extrude(ant_mast_height)
    .faces(">Z")              # Select top of the mast
    .fillet(ant_mast_radius - 0.1)  # Round the tip
)

# 3. Middle Knob
knob = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .center(knob_offset_x, 0)
    .circle(knob_radius)
    .extrude(knob_height)
    .faces(">Z").edges()
    .fillet(0.2)  # Slight rounding on the edge
)

# 4. Left Button (Dome/Light)
button = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .center(btn_offset_x, 0)
    .circle(btn_radius)
    .extrude(btn_height)
    .faces(">Z")
    .fillet(btn_radius - 0.1)  # Heavy fillet to create a dome shape
)

# -- Assembly --
# Combine all parts into a single solid
result = main_body.union(antenna).union(knob).union(button)