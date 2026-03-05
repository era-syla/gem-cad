import cadquery as cq

# --- Parametric Dimensions ---
width = 80.0            # Total width of the part
depth = 35.0            # Total depth of the part
thickness = 12.0        # Thickness of the main body
notch_width = 40.0      # Width of the front cutout
notch_depth = 18.0      # Depth of the front cutout
back_chamfer = 8.0      # Chamfer size for back corners
pin_size = 10.0         # Width/Length of the square pins
pin_height = 10.0       # Height of the pins (extrusion length)
pin_tip_chamfer = 3.0   # Chamfer size at the tip of the pins

# --- Modeling ---

# 1. Create the main body block
# Centered at (0,0,0) so Z spans from -thickness/2 to +thickness/2
main_body = cq.Workplane("XY").box(width, depth, thickness)

# 2. Cut the notch from the front (-Y direction)
# We position the cutter rectangle centered on the front edge Y coordinate
# We extrude with both=True to ensure it cuts through the full thickness
cutter = (
    cq.Workplane("XY")
    .moveTo(0, -depth / 2.0)
    .rect(notch_width, notch_depth * 2) # Double depth to ensure it clears the edge
    .extrude(thickness, both=True)
)

result = main_body.cut(cutter)

# 3. Apply chamfers to the back corners
# Select vertical edges (|Z) that are at the maximum Y position (>Y)
result = result.edges("|Z and >Y").chamfer(back_chamfer)

# 4. Add the pins (legs) underneath the arms
# Calculate X position: Center of the remaining arm material
arm_width = (width - notch_width) / 2.0
pin_x = (notch_width / 2.0) + (arm_width / 2.0)

# Calculate Y position: Center of the arm length (front-to-notch)
# Arms extend from -depth/2 to (-depth/2 + notch_depth)
pin_y = -(depth / 2.0) + (notch_depth / 2.0)

# Select bottom face (<Z), draw rectangles, and extrude
result = (
    result.faces("<Z").workplane()
    .pushPoints([(-pin_x, pin_y), (pin_x, pin_y)])
    .rect(pin_size, pin_size)
    .extrude(pin_height)
)

# 5. Chamfer the tips of the pins
# Select the edges at the lowest Z coordinate (<Z)
result = result.edges("<Z").chamfer(pin_tip_chamfer)