import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the unit
width = 120.0    # Total width of the cabinet
depth = 40.0     # Total depth of the cabinet
height = 45.0    # Total height of the cabinet body (excluding legs)
leg_height = 15.0 # Height of the legs
thickness = 2.0  # Thickness of the panels (top, bottom, sides, back)
back_panel_inset = 2.0 # How far the back panel is set in, or just thickness if flush

# --- Modeling ---

# 1. Create the main box body
# We start with a solid block and shell it or construct it from panels. 
# Constructing from panels is often more robust for furniture to control joints, 
# but shelling a box is simpler for a single monolithic look.
# Given the image, it looks like joined panels. Let's make a box and hollow it out.

# Create the outer block
outer_box = cq.Workplane("XY").box(width, depth, height)

# Create the inner cutout to form the open shelf
# The opening is on the front (-Y usually, or based on orientation).
# Let's assume:
# X is width (left-right)
# Y is depth (front-back)
# Z is height (up-down)

# We want to remove material from the front face, leaving 'thickness' on top, bottom, and sides.
# We also need a back panel.
inner_width = width - 2 * thickness
inner_height = height - 2 * thickness
inner_depth = depth - thickness # Removing front, keeping back panel

# The cutout should start from the front face and go inwards.
# Let's align the box so the center is at (0,0,0) for easier calculations.
# Front face is at Y = -depth/2 (or +depth/2 depending on view). Let's say front is +Y.
# We cut a pocket from the front face.

# Re-orienting strategy:
# Let's build the main body centered on Z=height/2 + leg_height to put it on top of legs.
# Actually, let's just build parts relative to origin and union them.

# Main Body Construction
# Outer dimensions: width, depth, height
main_body = cq.Workplane("XY").box(width, depth, height)

# Create the hollow internal volume
# The opening is at the front (let's say +Y face)
# The cut needs to leave material for Left, Right, Top, Bottom, and Back walls.
cutout = (
    cq.Workplane("XY")
    .workplane(offset=-depth/2 + thickness) # Start from the inside of the back panel
    .box(inner_width, depth, inner_height, centered=(True, False, True)) # Extrude towards front
)
# We need to shift the cutout so it cuts through the front face.
# The box above is created. Let's position a cutting tool.

shell = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .faces(">Y") # Select front face
    .workplane()
    .rect(inner_width, inner_height)
    .cutBlind(-(depth - thickness)) # Cut inwards, leaving the back panel thickness
)

# 2. Add the vertical stiffener / Top Apron visual feature
# The image shows a horizontal line across the top front. It looks like the top panel is separate,
# or there is a slight overhang or separate piece.
# Looking closely, it looks like a simple box, but there is a faint line in the middle of the top edge?
# No, it looks like the top slab sits on top of the side panels.
# Let's refine the construction to be panel-based to match the lines better.

# Top Panel
top_panel = cq.Workplane("XY").box(width, depth, thickness).translate((0, 0, height/2 - thickness/2))

# Bottom Panel
bottom_panel = cq.Workplane("XY").box(width, depth, thickness).translate((0, 0, -height/2 + thickness/2))

# Side Panels (Left and Right)
# They fit between top and bottom panels usually, or sides go all the way up.
# Image suggests top panel rests on sides (top is full width).
side_height = height - 2 * thickness
left_panel = (
    cq.Workplane("XY")
    .box(thickness, depth, side_height)
    .translate((-width/2 + thickness/2, 0, 0))
)
right_panel = (
    cq.Workplane("XY")
    .box(thickness, depth, side_height)
    .translate((width/2 - thickness/2, 0, 0))
)

# Back Panel
# Fits between sides, top, and bottom.
back_width = width - 2 * thickness
back_height = height - 2 * thickness
back_panel = (
    cq.Workplane("XY")
    .box(back_width, thickness, back_height)
    .translate((0, depth/2 - thickness/2, 0)) # Positioned at the back (+Y)
)

# Combine body parts
body = top_panel.union(bottom_panel).union(left_panel).union(right_panel).union(back_panel)

# Note: The image shows a faint line in the middle of the top opening. 
# This usually implies a vertical divider or a drawer split, but the space below is open.
# It looks like a reinforcement strip or just a double thickness top edge at the front.
# Or potentially two drawers side-by-side at the top?
# Looking at the shadow inside, the top part looks deeper/darker. 
# It looks like there is a top rail or an "apron" providing structure, 
# making the opening slightly shorter than the full internal height.
# Let's add a top rail at the front.
rail_height = 5.0
front_rail = (
    cq.Workplane("XY")
    .box(width - 2*thickness, thickness, rail_height) # Width fits between sides
    .translate((0, -depth/2 + thickness/2, height/2 - thickness - rail_height/2))
)
# And maybe a center vertical piece for the rail if it mimics drawers?
# The image shows a vertical line in the middle of that top strip.
center_divider_stub = (
    cq.Workplane("XY")
    .box(thickness/4, thickness, rail_height) # Very thin line suggestion
    .translate((0, -depth/2 + thickness/2, height/2 - thickness - rail_height/2))
)

# Let's unite the rail to the body.
body = body.union(front_rail)

# 3. Create Legs
# Simple rectangular legs at the corners.
# The legs seem to support the bottom panel.
leg_width = 4.0
leg_depth = 4.0
leg_x_offset = width/2 - leg_width/2
leg_y_offset = depth/2 - leg_depth/2

# Leg geometry
leg = cq.Workplane("XY").box(leg_width, leg_depth, leg_height)

# Position 4 legs relative to the body
# Body is centered at Z=0 (height/2 to -height/2). 
# We need to move body up or legs down. Let's move body up.
# Final assembly logic:
# Body bottom face is at Z = 0
# Legs go from Z = 0 down to Z = -leg_height

# Adjust body to sit on Z=leg_height
body = body.translate((0, 0, height/2 + leg_height))

# Create legs at Z=leg_height/2
leg_fl = leg.translate((-leg_x_offset, -leg_y_offset, leg_height/2))
leg_fr = leg.translate((leg_x_offset, -leg_y_offset, leg_height/2))
leg_bl = leg.translate((-leg_x_offset, leg_y_offset, leg_height/2))
leg_br = leg.translate((leg_x_offset, leg_y_offset, leg_height/2))

# The image shows the legs might be slightly inset from the very edge, 
# or flush with the side panels but not the top/bottom overhangs?
# Looking at the left side, the leg is flush with the side panel.
# Let's keep them flush with the corners.

# Add slight vertical line detail to the top rail to match image
# The image has a split in the top horizontal bar. 
# I added `center_divider_stub` conceptually, let's cut a groove or just place a small divider.
# To replicate the image exactly, let's cut a tiny groove in the front_rail.
groove = (
     cq.Workplane("XY")
    .box(0.5, thickness * 2, rail_height + 1)
    .translate((0, -depth/2 + thickness/2, height + leg_height - thickness - rail_height/2))
)
body = body.cut(groove)

# Combine everything
result = body.union(leg_fl).union(leg_fr).union(leg_bl).union(leg_br)

# Rotate to match isometric view standard orientation usually expected
# (CadQuery default view is top-down, let's leave it in standard 3D coordinates)