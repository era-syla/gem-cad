import cadquery as cq

# --- Parameters ---

# Central Hub Dimensions
hub_length = 40.0
hub_width = 24.0
hub_height = 10.0
hub_fillet_r = 2.0

# Side Wings Dimensions
wing_span_total = 80.0 # Total tip-to-tip
wing_width = 20.0      # Dimension along the main axis
wing_thickness = 4.0

# Front Tongue Dimensions
tongue_length = 40.0
tongue_width = 20.0
tongue_thickness = 4.0

# Rear Hinge Lug Dimensions
lug_width = 10.0      # Thickness of the lug (Y direction)
lug_depth = 12.0      # Length of the lug base (X direction)
lug_height = 18.0     # Height protruding above the hub
lug_hole_dia = 5.0
lug_base_fillet = 5.0 # Radius of fillet connecting lug to hub

# Small Vertical Hole
small_hole_dia = 2.5
small_hole_dist = 5.0 # Distance from lug front face

# Lever (Detached Part) Dimensions
lever_height = 35.0
lever_base_x = 10.0
lever_base_y = 16.0
lever_top_x = 8.0     # Thickness at top (should allow for hinge ear rounding)
lever_top_y = 14.0
ear_height = 10.0
slot_width = 10.5     # Slightly larger than lug_width
pin_hole_dia = 5.0

# --- Modeling Base Part ---

# 1. Central Hub
hub = (
    cq.Workplane("XY")
    .box(hub_length, hub_width, hub_height, centered=(True, True, False))
    .edges("|Z")
    .fillet(hub_fillet_r)
)

# 2. Side Wings
# Created as a single strip crossing the hub
wings = (
    cq.Workplane("XY")
    .box(wing_width, wing_span_total, wing_thickness, centered=(True, True, False))
)

# 3. Front Tongue
# Positioned at the +X end of the hub
tongue = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(hub_length/2 + tongue_length/2, 0)
    .box(tongue_length, tongue_width, tongue_thickness, centered=(True, True, False))
)

# Union the base platform
base_platform = hub.union(wings).union(tongue)

# 4. Rear Lug
# Define profile on XZ plane to get the rounded top "tombstone" shape naturally
# Positioned at -X end
lug_x_pos = -hub_length/2 + lug_depth/2
lug_z_base = hub_height

lug_profile = (
    cq.Workplane("XZ")
    .center(lug_x_pos, lug_z_base)
    .moveTo(-lug_depth/2, 0)
    .lineTo(-lug_depth/2, lug_height - lug_depth/2)
    # Create semi-circle top
    .threePointArc((0, lug_height), (lug_depth/2, lug_height - lug_depth/2))
    .lineTo(lug_depth/2, 0)
    .close()
    .extrude(lug_width/2, both=True) # Extrude symmetrically in Y
)

# Combine lug with platform
base_solid = base_platform.union(lug_profile)

# 5. Features on Base
# Fillet the junction between Lug and Hub (Front face of lug)
# Select edge near (lug_x_pos + lug_depth/2, 0, hub_height)
try:
    edge_selector = cq.selectors.BoxSelector(
        (lug_x_pos + lug_depth/2 - 1, -lug_width/2 - 1, hub_height - 1),
        (lug_x_pos + lug_depth/2 + 1, lug_width/2 + 1, hub_height + 1)
    )
    base_solid = base_solid.edges(edge_selector).fillet(lug_base_fillet)
except:
    pass # Skip if geometry selection is ambiguous

# Cut Hinge Hole in Lug
hole_z_center = lug_z_base + lug_height - lug_depth/2
base_solid = base_solid.cut(
    cq.Workplane("YZ")
    .center(0, hole_z_center)
    .circle(lug_hole_dia/2)
    .extrude(100, both=True)
)

# Cut Small Vertical Hole
small_hole_x = lug_x_pos + lug_depth/2 + small_hole_dist
base_solid = base_solid.cut(
    cq.Workplane("XY")
    .center(small_hole_x, 0)
    .circle(small_hole_dia/2)
    .extrude(hub_height, both=True)
)

# --- Modeling Lever Part ---

# 1. Tapered Body
lever_body = (
    cq.Workplane("XY")
    .rect(lever_base_x, lever_base_y)
    .workplane(offset=lever_height)
    .rect(lever_top_x, lever_top_y)
    .loft(combine=True)
)

# 2. Hinge Head (Straight section on top)
head = (
    cq.Workplane("XY")
    .workplane(offset=lever_height)
    .box(lever_top_x, lever_top_y, ear_height, centered=(True, True, False))
)

# Round the top of the head (edges parallel to Y)
head = head.edges(">Z and |Y").fillet(lever_top_x/2 - 0.01)

lever = lever_body.union(head)

# 3. Cut Slot for Base Lug
# Slot cuts through the center of the head
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=lever_height - 1) # Start slightly below head
    .box(lever_top_x + 5, slot_width, ear_height + 10, centered=(True, True, False))
)
lever = lever.cut(slot_cut)

# 4. Cut Pin Holes in Ears
# Calculate center relative to head geometry
# Center of the rounded top is at Z = lever_height + ear_height - radius
ear_radius = lever_top_x / 2
pin_z_local = lever_height + ear_height - ear_radius

lever = lever.cut(
    cq.Workplane("YZ")
    .center(0, pin_z_local)
    .circle(pin_hole_dia/2)
    .extrude(100, both=True)
)

# --- Assembly ---

# Position the lever above and offset from the base for the exploded view
# Align X/Y with the lug, lift in Z
lever_positioned = lever.translate((lug_x_pos, 0, lug_z_base + lug_height + 20))

# Combine into final result
result = base_solid.union(lever_positioned)