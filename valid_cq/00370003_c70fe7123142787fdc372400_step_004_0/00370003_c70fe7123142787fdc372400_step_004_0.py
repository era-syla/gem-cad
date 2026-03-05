import cadquery as cq

# -----------------------------------------------------------------------------
# Parameter Definitions
# -----------------------------------------------------------------------------
# Head (Eye) Dimensions
head_od = 32.0          # Outer diameter of the cylindrical head
head_id = 16.0          # Inner diameter (through-hole)
head_height = 28.0      # Height of the head
head_chamfer = 1.5      # Chamfer size for outer edges
hole_chamfer = 0.5      # Chamfer size for the inner hole

# Shaft Dimensions
shaft_diam = 12.0       # Diameter of the threaded shaft
shaft_length = 45.0     # Length of shaft extending from the head surface
shaft_tip_chamfer = 1.0 # Chamfer at the end of the shaft

# -----------------------------------------------------------------------------
# Geometric Modeling
# -----------------------------------------------------------------------------

# 1. Create the Head (Cylinder with hole)
# Centered at the origin on the XY plane, extruded along Z
head = (
    cq.Workplane("XY")
    .circle(head_od / 2.0)
    .circle(head_id / 2.0)
    .extrude(head_height)
)

# Apply chamfers to the head
# Select outer edges (largest radius) for the main chamfer
head = head.edges(cq.selectors.RadiusNthSelector(1)).chamfer(head_chamfer)

# Select inner edges (smallest radius) for the hole chamfer
head = head.edges(cq.selectors.RadiusNthSelector(0)).chamfer(hole_chamfer)

# 2. Create the Shaft
# Calculate total extrusion length to start from center (X=0) to ensure overlap
shaft_extrusion_total = (head_od / 2.0) + shaft_length

# Create shaft aligned with X-axis, centered vertically on the head
shaft = (
    cq.Workplane("YZ")
    .center(0, head_height / 2.0)  # Offset origin to mid-height of head
    .circle(shaft_diam / 2.0)
    .extrude(shaft_extrusion_total)
)

# Chamfer the tip of the shaft
shaft = shaft.faces(">X").edges().chamfer(shaft_tip_chamfer)

# 3. Combine Parts
# Union the head and the shaft to create the final solid
result = head.union(shaft)