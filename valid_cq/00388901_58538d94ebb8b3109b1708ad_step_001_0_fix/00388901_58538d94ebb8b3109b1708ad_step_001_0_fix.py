import cadquery as cq

# Parameters
L, W, H = 100, 20, 10        # Length, width, height of main body
P_thick = 8                  # Thickness (depth) of end plate
S_width = 12                 # Width (diameter) of U‐slot
S_depth = 5                  # Depth of U‐slot into the plate
R_fillet = 2                 # Fillet radius on top edges

# Create main bar
result = cq.Workplane("XY").box(L, W, H)

# Add end plate on +X side
plate = cq.Workplane("XY").box(P_thick, W, H).translate((L/2 - P_thick/2, 0, 0))
result = result.union(plate)

# Compute rectangle height for slot (below the semicircle)
C = H - S_width

# Create rectangular cut for the U‐slot
slot_rect = (
    cq.Workplane("YZ")
    .transformed(offset=(L/2, 0, -H/2 + C/2))
    .rect(S_width, C)
    .extrude(-S_depth)
)

# Create semicircular cut for the U‐slot
slot_cyl = (
    cq.Workplane("YZ")
    .transformed(offset=(L/2, 0, -H/2 + C + S_width/2))
    .circle(S_width/2)
    .extrude(-S_depth)
)

# Subtract the slot shapes
result = result.cut(slot_rect).cut(slot_cyl)

# Fillet all edges (top edges will be rounded)
result = result.edges().fillet(R_fillet)  # fillet radius

# 'result' now holds the final solid geometry.