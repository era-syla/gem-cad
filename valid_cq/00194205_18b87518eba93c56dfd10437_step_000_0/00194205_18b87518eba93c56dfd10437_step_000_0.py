import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_width = 14.0
body_length = 14.0
body_height = 8.0
wall_thickness = 3.0
hole_size = body_width - (2 * wall_thickness) # 8.0

# Flat Pin dimensions (Left side)
flat_pin_w = 4.0        # Width along the side wall
flat_pin_t = 1.2        # Thickness
flat_pin_top_h = 14.0   # Extension above top face
flat_pin_bot_h = 6.0    # Extension below bottom face

# Round Pin dimensions
pin_dia = 2.0
pin_top_h = 3.5
pin_bot_h = 6.0

# Small top hole dimensions
small_hole_dia = 1.2
small_hole_depth = 2.0

# --- Geometry Construction ---

# 1. Create the main body block
# We create it centered at the origin
result = cq.Workplane("XY").box(body_width, body_length, body_height)

# 2. Cut the central square hole
result = result.faces(">Z").workplane().rect(hole_size, hole_size).cutThruAll()

# Calculate the center-line offset for the walls to position pins correctly
# This places pins in the middle of the solid wall material
offset_dist = (body_width + hole_size) / 4.0

# 3. Create the Flat Pin (Left Wall)
# Located at -X, centered on Y axis
flat_pin = (
    cq.Workplane("XY")
    .workplane(offset = -body_height/2 - flat_pin_bot_h)
    .moveTo(-offset_dist, 0)
    .rect(flat_pin_t, flat_pin_w)
    .extrude(flat_pin_bot_h + body_height + flat_pin_top_h)
)

# 4. Create the Front-Left Round Pin
# Located at -X, -Y corner
pin_fl = (
    cq.Workplane("XY")
    .workplane(offset = -body_height/2 - pin_bot_h)
    .moveTo(-offset_dist, -offset_dist)
    .circle(pin_dia / 2.0)
    .extrude(pin_bot_h + body_height + pin_top_h)
)

# 5. Create the Back-Right Round Pin
# Located at +X, +Y corner
# This pin appears to extend upwards.
pin_br = (
    cq.Workplane("XY")
    .workplane(offset = body_height/2)
    .moveTo(offset_dist, offset_dist)
    .circle(pin_dia / 2.0)
    .extrude(pin_top_h)
)

# 6. Union all parts together
result = result.union(flat_pin).union(pin_fl).union(pin_br)

# 7. Create the small indicator hole
# Located on the top face, back wall, slightly offset from the pin
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(1.5, offset_dist)
    .circle(small_hole_dia / 2.0)
    .cutBlind(-small_hole_depth)
)