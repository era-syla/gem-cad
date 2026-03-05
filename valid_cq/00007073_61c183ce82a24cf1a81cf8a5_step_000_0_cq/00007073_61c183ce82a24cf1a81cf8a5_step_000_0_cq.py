import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
table_width = 1500.0   # Long dimension
table_depth = 750.0    # Short dimension
table_height = 900.0   # Total height including top

# Top dimensions
top_thickness = 30.0
overhang = 25.0        # How much the top overhangs the frame

# Leg/Frame dimensions
leg_size = 60.0        # Square profile size for legs
rail_height_top = 80.0 # Height of the top connecting rails
rail_height_bot = 80.0 # Height of the bottom connecting rails
rail_thickness = 20.0  # Thickness of the rails
panel_thickness = 10.0 # Thickness of side/back panels
bottom_rail_offset = 50.0 # Distance from floor to bottom of bottom rail

# Foot/Leveler dimensions
foot_height = 30.0
foot_diameter_top = leg_size
foot_diameter_bottom = leg_size * 0.7

# --- Derived Parameters ---
frame_width = table_width - (2 * overhang)
frame_depth = table_depth - (2 * overhang)
frame_height = table_height - top_thickness - foot_height

# --- Geometry Construction ---

# 1. Legs
# Create a single leg profile to be instantiated 4 times
leg = (
    cq.Workplane("XY")
    .box(leg_size, leg_size, frame_height)
    .translate((0, 0, frame_height / 2 + foot_height))
)

# Create positions for the 4 legs
leg_x_offset = (frame_width - leg_size) / 2
leg_y_offset = (frame_depth - leg_size) / 2

legs = (
    cq.Workplane("XY")
    .pushPoints([
        (leg_x_offset, leg_y_offset),
        (leg_x_offset, -leg_y_offset),
        (-leg_x_offset, leg_y_offset),
        (-leg_x_offset, -leg_y_offset)
    ])
    .eachpoint(lambda loc: leg.val().located(loc))
)

# 2. Feet (Levelers)
# Simple chamfered cylinder or loft for feet
foot = (
    cq.Workplane("XY")
    .circle(foot_diameter_bottom / 2)
    .workplane(offset=foot_height * 0.8)
    .circle(foot_diameter_top / 2)
    .loft(combine=True)
    .faces(">Z").chamfer(2.0)
    .translate((0, 0, 0)) # Base is at Z=0
)

feet = (
    cq.Workplane("XY")
    .pushPoints([
        (leg_x_offset, leg_y_offset),
        (leg_x_offset, -leg_y_offset),
        (-leg_x_offset, leg_y_offset),
        (-leg_x_offset, -leg_y_offset)
    ])
    .eachpoint(lambda loc: foot.val().located(loc))
)

# 3. Rails (Frame)
# Calculate lengths between legs
long_rail_len = frame_width - (2 * leg_size)
short_rail_len = frame_depth - (2 * leg_size)

# Top Rails (Long)
top_rail_long = (
    cq.Workplane("XY")
    .box(long_rail_len, rail_thickness, rail_height_top)
    .translate((0, 0, table_height - top_thickness - rail_height_top / 2))
)

# Top Rails (Short)
top_rail_short = (
    cq.Workplane("XY")
    .box(rail_thickness, short_rail_len, rail_height_top)
    .translate((0, 0, table_height - top_thickness - rail_height_top / 2))
)

# Bottom Rails (Long)
bot_rail_long = (
    cq.Workplane("XY")
    .box(long_rail_len, rail_thickness, rail_height_bot)
    .translate((0, 0, foot_height + bottom_rail_offset + rail_height_bot / 2))
)

# Bottom Rails (Short)
bot_rail_short = (
    cq.Workplane("XY")
    .box(rail_thickness, short_rail_len, rail_height_bot)
    .translate((0, 0, foot_height + bottom_rail_offset + rail_height_bot / 2))
)

# Assemble Rails
rails = (
    cq.Workplane("XY")
    # Front and Back Top Rails
    .pushPoints([(0, leg_y_offset - (leg_size/2) + (rail_thickness/2)), 
                 (0, -leg_y_offset + (leg_size/2) - (rail_thickness/2))])
    .eachpoint(lambda loc: top_rail_long.val().located(loc))
    # Left and Right Top Rails
    .add(
        cq.Workplane("XY")
        .pushPoints([(leg_x_offset - (leg_size/2) + (rail_thickness/2), 0), 
                     (-leg_x_offset + (leg_size/2) - (rail_thickness/2), 0)])
        .eachpoint(lambda loc: top_rail_short.val().located(loc))
    )
    # Front and Back Bottom Rails
    .add(
        cq.Workplane("XY")
        .pushPoints([(0, leg_y_offset - (leg_size/2) + (rail_thickness/2)), 
                     (0, -leg_y_offset + (leg_size/2) - (rail_thickness/2))])
        .eachpoint(lambda loc: bot_rail_long.val().located(loc))
    )
    # Left and Right Bottom Rails
    .add(
        cq.Workplane("XY")
        .pushPoints([(leg_x_offset - (leg_size/2) + (rail_thickness/2), 0), 
                     (-leg_x_offset + (leg_size/2) - (rail_thickness/2), 0)])
        .eachpoint(lambda loc: bot_rail_short.val().located(loc))
    )
)


# 4. Panels
# Create panels to fill the space between rails and legs
panel_height = (table_height - top_thickness - rail_height_top) - (foot_height + bottom_rail_offset + rail_height_bot)
panel_z_center = foot_height + bottom_rail_offset + rail_height_bot + (panel_height / 2)

# Long Panel (Back only usually, but let's do front and back for symmetry based on image)
long_panel = (
    cq.Workplane("XY")
    .box(long_rail_len, panel_thickness, panel_height)
    .translate((0, 0, panel_z_center))
)

# Short Panel (Sides)
short_panel = (
    cq.Workplane("XY")
    .box(panel_thickness, short_rail_len, panel_height)
    .translate((0, 0, panel_z_center))
)

panels = (
    cq.Workplane("XY")
    # Front and Back Panels (slightly inset)
    .pushPoints([(0, leg_y_offset - (leg_size/2) + (rail_thickness/2)), 
                 (0, -leg_y_offset + (leg_size/2) - (rail_thickness/2))])
    .eachpoint(lambda loc: long_panel.val().located(loc))
    # Side Panels
    .add(
        cq.Workplane("XY")
        .pushPoints([(leg_x_offset - (leg_size/2) + (rail_thickness/2), 0), 
                     (-leg_x_offset + (leg_size/2) - (rail_thickness/2), 0)])
        .eachpoint(lambda loc: short_panel.val().located(loc))
    )
)

# 5. Table Top
# A simple box with a slight chamfer or fillet on top edges
top = (
    cq.Workplane("XY")
    .box(table_width, table_depth, top_thickness)
    .translate((0, 0, table_height - top_thickness/2))
    .edges("|Z").fillet(5.0) # Rounded corners
    .faces(">Z").edges().fillet(2.0) # Soft edge on top
)

# --- Final Assembly ---
result = (
    legs
    .union(feet)
    .union(rails)
    .union(panels)
    .union(top)
)