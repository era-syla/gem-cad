import cadquery as cq

# --- Parametric Dimensions ---
# Left Head Section
head_dia = 12.0
head_len = 16.0
hole_dia = 4.0

# First Groove (Neck)
neck1_dia = 9.0
neck1_len = 4.0

# Main Shaft Section
main_dia = 12.0
main_len = 50.0

# Step Section (Right)
step_dia = 10.0
step_len = 10.0

# Second Groove (Neck)
neck2_dia = 7.5
neck2_len = 3.5

# Right Tip
tip_dia = 10.0
tip_len = 4.0

# Details
chamfer_size = 0.5
fillet_radius = 0.5

# --- Geometry Construction ---

# 1. Build the stepped shaft profile using stacked extrusions
# Start at Z=0 and build upwards
current_z = 0.0

# Base Head
shaft = cq.Workplane("XY").circle(head_dia / 2.0).extrude(head_len)
current_z += head_len
z_neck1_start = current_z

# Neck 1
shaft = shaft.faces(">Z").workplane().circle(neck1_dia / 2.0).extrude(neck1_len)
current_z += neck1_len
z_neck1_end = current_z

# Main Body
shaft = shaft.faces(">Z").workplane().circle(main_dia / 2.0).extrude(main_len)
current_z += main_len

# Step
shaft = shaft.faces(">Z").workplane().circle(step_dia / 2.0).extrude(step_len)
current_z += step_len
z_neck2_start = current_z

# Neck 2
shaft = shaft.faces(">Z").workplane().circle(neck2_dia / 2.0).extrude(neck2_len)
current_z += neck2_len
z_neck2_end = current_z

# Tip
shaft = shaft.faces(">Z").workplane().circle(tip_dia / 2.0).extrude(tip_len)

# 2. Cut the through-hole in the Head
# Position: Center of head length, rotated 90 deg to cut through X/Y plane
result = (
    shaft.faces("<Z").workplane(offset=head_len / 2.0)
    .transformed(rotate=(90, 0, 0))
    .circle(hole_dia / 2.0)
    .cutThruAll()
)

# 3. Apply Chamfers to the very ends
result = result.faces("<Z").edges().chamfer(chamfer_size)
result = result.faces(">Z").edges().chamfer(chamfer_size)

# 4. Apply Fillets to the groove transitions
# Using NearestToPointSelector to reliably find the circular edges at specific Z heights
# Neck 1 Edges
result = result.edges(cq.NearestToPointSelector((0, head_dia/2, z_neck1_start))).fillet(fillet_radius)
result = result.edges(cq.NearestToPointSelector((0, head_dia/2, z_neck1_end))).fillet(fillet_radius)

# Neck 2 Edges
result = result.edges(cq.NearestToPointSelector((0, step_dia/2, z_neck2_start))).fillet(fillet_radius)
result = result.edges(cq.NearestToPointSelector((0, tip_dia/2, z_neck2_end))).fillet(fillet_radius)

# The 'result' variable contains the final CadQuery object