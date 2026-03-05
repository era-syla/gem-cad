import cadquery as cq

# Parametric dimensions for the model
length = 70.0
width = 40.0
height = 18.0
groove_radius = 14.0
hole_diameter = 12.0
chamfer_size = 10.0

# 1. Create the base rectangular block
# The box is centered at the origin (0,0,0), so Z ranges from -height/2 to +height/2
result = cq.Workplane("XY").box(length, width, height)

# 2. Create and cut the semi-cylindrical groove
# We create a cylinder oriented along the Y-axis centered on the top face
groove_cutter = (
    cq.Workplane("XZ", origin=(0, 0, height / 2))
    .circle(groove_radius)
    .extrude(width * 2, both=True)  # Extrude wider than part to ensure clean cut
)
result = result.cut(groove_cutter)

# 3. Apply chamfers to one end of the block
# Select vertical edges (|Z) located at the minimum X coordinate (<X)
result = result.edges("|Z and <X").chamfer(chamfer_size)

# 4. Create the through-hole
# The hole is positioned on the chamfered end (negative X side).
# We calculate the center point between the end of the block and the start of the groove.
# Block end X: -length/2
# Groove edge X: -groove_radius (since groove is centered at 0)
hole_center_x = (-length / 2 - groove_radius) / 2

result = (
    result.faces(">Z")
    .workplane()
    .moveTo(hole_center_x, 0)
    .hole(hole_diameter)
)