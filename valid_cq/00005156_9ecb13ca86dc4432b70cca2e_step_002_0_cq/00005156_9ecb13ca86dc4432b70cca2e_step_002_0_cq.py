import cadquery as cq

# --- Parametric Dimensions ---

# Main Body
body_width = 120.0
body_height = 80.0
body_thickness = 40.0
body_fillet = 5.0

# Grip (Right side lump)
grip_width = 30.0
grip_protrusion = 20.0  # How much it sticks out forward
grip_height = body_height * 0.95
grip_fillet = 8.0

# Top Prism/Flash housing
prism_width = 50.0
prism_height = 20.0
prism_length = body_thickness + 10.0 # Extends slightly forward
prism_slope_offset = 10.0 # For the chamfered look

# Lens Barrel
lens_base_radius = 28.0
lens_base_length = 40.0
lens_mid_radius = 24.0
lens_mid_length = 15.0
lens_tip_radius = 22.0
lens_tip_length = 5.0
lens_ring_radius = 23.0
lens_ring_thickness = 2.0

# Shutter Button
shutter_radius = 8.0
shutter_height = 4.0

# Hotshoe details
hotshoe_width = 16.0
hotshoe_length = 18.0
hotshoe_height = 1.5

# --- Modeling Strategy ---
# 1. Create the main rectangular block (body).
# 2. Add the grip on the left side (from viewer perspective, right side of camera).
# 3. Add the prism/flash housing on top.
# 4. Add the lens assembly on the front.
# 5. Add details: shutter button, hot shoe rails.
# 6. Apply fillets to smooth edges.

# 1. Main Body
main_body = (
    cq.Workplane("XY")
    .box(body_width, body_thickness, body_height)
    .edges("|Z").fillet(body_fillet)
)

# 2. Grip (L-shape protrusion on the side)
# Positioned on the left side of the main body (-X)
grip = (
    cq.Workplane("XY")
    .workplane(offset=-body_height/2) # Start at bottom
    .center(-body_width/2 + grip_width/2, body_thickness/2)
    .box(grip_width, grip_protrusion * 2, grip_height, centered=(True, False, False)) # Extended depth to merge cleanly
    .edges("|Z").fillet(grip_fillet)
)

# Refine grip shape (cut off the back part that shouldn't protrude)
grip = grip.intersect(
    cq.Workplane("XY")
    .center(-body_width/2 + grip_width/2, body_thickness/2 + grip_protrusion/2)
    .box(grip_width + 10, grip_protrusion + body_thickness, body_height + 10)
)
# Position grip vertically
grip = grip.translate((0, 0, (body_height - grip_height)/2 * -1))


# 3. Top Prism / Flash Housing
# This is a complex shape, roughly trapezoidal from the front.
prism_sketch = (
    cq.Workplane("XZ")
    .workplane(offset=body_thickness/2) # Front faceish
    .moveTo(-prism_width/2, body_height/2)
    .lineTo(-prism_width/2 + 5, body_height/2 + prism_height)
    .lineTo(prism_width/2 - 5, body_height/2 + prism_height)
    .lineTo(prism_width/2, body_height/2)
    .close()
    .extrude(-prism_length) # Extrude backwards
)

# Cut a slope on the front of the prism for that overhang look
prism_cut = (
    cq.Workplane("YZ")
    .moveTo(body_thickness/2 + 10, body_height/2)
    .lineTo(body_thickness/2 - 5, body_height/2 + prism_height + 5)
    .lineTo(body_thickness/2 + 20, body_height/2 + prism_height + 5)
    .close()
    .extrude(100, both=True)
)
prism = prism_sketch.cut(prism_cut)

# Fillet the top edges of the prism
prism = prism.edges("|Y").filter(lambda e: e.Center().z > body_height/2 + prism_height/2).fillet(2.0)


# 4. Lens Assembly
# Created as a stack of cylinders
lens_center = (0, body_height/2 - body_height * 0.4) # Slightly offset from center

lens = (
    cq.Workplane("XZ")
    .workplane(offset=body_thickness/2)
    .center(*lens_center)
    .circle(lens_base_radius)
    .extrude(lens_base_length)
)

lens_mid = (
    cq.Workplane("XZ")
    .workplane(offset=body_thickness/2 + lens_base_length)
    .center(*lens_center)
    .circle(lens_mid_radius)
    .extrude(lens_mid_length)
)

lens_tip = (
    cq.Workplane("XZ")
    .workplane(offset=body_thickness/2 + lens_base_length + lens_mid_length)
    .center(*lens_center)
    .circle(lens_tip_radius)
    .extrude(lens_tip_length)
)

# Lens Ring (detail)
lens_ring = (
    cq.Workplane("XZ")
    .workplane(offset=body_thickness/2 + lens_base_length + lens_mid_length + lens_tip_length - 1)
    .center(*lens_center)
    .circle(lens_ring_radius)
    .circle(lens_tip_radius - 1) # Hollow out slightly
    .extrude(1.5)
)

# Inner Glass
lens_glass = (
    cq.Workplane("XZ")
    .workplane(offset=body_thickness/2 + lens_base_length + lens_mid_length + lens_tip_length)
    .center(*lens_center)
    .circle(lens_tip_radius - 2)
    .extrude(0.5)
)


# 5. Shutter Button
# Located on top of the grip area
shutter = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2)
    .center(-body_width/2 + grip_width/2 + 2, body_thickness/2 + grip_protrusion/2 - 5)
    .circle(shutter_radius)
    .extrude(shutter_height)
)

# 6. Hot Shoe Rails (Simplified)
hotshoe = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + prism_height)
    .center(0, -5) # Centered on prism
    .rect(hotshoe_width, hotshoe_length)
    .extrude(hotshoe_height)
)

# Cut the inner channel of hotshoe
hotshoe_channel = (
    cq.Workplane("XY")
    .workplane(offset=body_height/2 + prism_height)
    .center(0, -5)
    .rect(hotshoe_width - 4, hotshoe_length + 2)
    .extrude(hotshoe_height)
)
hotshoe = hotshoe.cut(hotshoe_channel)


# --- Combine All Parts ---

camera = main_body.union(grip).union(prism)
camera = camera.union(lens).union(lens_mid).union(lens_tip).union(lens_ring).union(lens_glass)
camera = camera.union(shutter).union(hotshoe)


# --- Final Refinements (Smoothing transitions) ---

# Try to fillet the junction between lens and body
try:
    camera = camera.edges(cq.selectors.NearestToPointSelector((0, body_thickness/2, 0))).fillet(2.0)
except:
    pass # Sometimes fillets fail on complex unions

# Global smoothing on sharp outer edges where appropriate
# (Selective filleting is safer than global filleting)
camera = camera.edges("|Y").filter(lambda e: e.Center().z > body_height/2 - 10 and abs(e.Center().x) > body_width/4).fillet(2.0)

result = camera