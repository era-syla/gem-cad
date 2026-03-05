import cadquery as cq

# Parametric dimensions
# Large block (Left/Back)
L1 = 60.0
W1 = 40.0
H1 = 15.0

# Small block (Right/Front)
L2 = 40.0
W2 = 20.0
H2 = 15.0
fillet_radius = 3.0

# Positioning
gap = 5.0  # Gap between the two blocks
stagger_x = 15.0  # Offset in X axis to create the staggered look

# Create the large block
# Placed on the XY plane, centered Z
# Shifted to the left (-X) and back (+Y)
box1 = (
    cq.Workplane("XY")
    .box(L1, W1, H1)
    .translate((-stagger_x / 2, (W1 + gap) / 2, H1 / 2))
)

# Create the small block
# Placed on the XY plane, centered Z
# Apply fillets to the top edges running along the length (X-axis)
# Shifted to the right (+X) and front (-Y)
box2 = (
    cq.Workplane("XY")
    .box(L2, W2, H2)
    .edges("|X")  # Select edges parallel to X
    .edges(">Z")  # Filter for edges on the top face
    .fillet(fillet_radius)
    .translate((stagger_x / 2, -(W2 + gap) / 2, H2 / 2))
)

# Combine the two solids into a single result
result = box1.union(box2)