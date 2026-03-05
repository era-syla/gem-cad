import cadquery as cq

# Parametric dimensions based on the visual proportions
length = 60.0
outer_diameter = 24.0
inner_diameter = 12.0
groove_width = 1.5
groove_depth = 0.8
groove_margin = 6.0  # Distance from the end of the cylinder to the center of the groove
chamfer_size = 1.0

# 1. Create the base cylinder
# We define a circle on the XY plane and extrude it to the desired length along Z
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(length)

# 2. Create the central through-hole
# Select the top face (>Z) and cut a hole through the entire solid
result = result.faces(">Z").workplane().hole(inner_diameter)

# 3. Create the circumferential grooves
# We create a separate solid representing the volume to remove (the cutter).
# We sketch the groove profile on the XZ plane and revolve it around the Z-axis.

# Calculate the position for the cutter profile.
# To ensure a clean cut on the outer surface, we make the cutter rectangle wider than the depth
# and position it so the inner edge is exactly at (OD/2 - groove_depth).
cutter_rect_w = groove_depth * 4.0  # Make it wide enough to extend into 'air' outside
# Center X = Inner_Edge_X + Width/2
cutter_center_x = (outer_diameter / 2.0 - groove_depth) + (cutter_rect_w / 2.0)

groove_cutter = (
    cq.Workplane("XZ")
    .moveTo(cutter_center_x, groove_margin)
    .rect(cutter_rect_w, groove_width)
    .moveTo(cutter_center_x, length - groove_margin)
    .rect(cutter_rect_w, groove_width)
    .revolve(360, (0, 0, 0), (0, 1, 0))  # Revolve around local Y-axis (which is Global Z)
)

# Subtract the groove cutter from the main body
result = result.cut(groove_cutter)

# 4. Apply Chamfers
# Select the outer edges at the top and bottom faces.
# Strategy: Select edges belonging to the top (>Z) or bottom (<Z) faces,
# then filter for the edge with the largest radius (RadiusNthSelector(-1))
# to ensure we pick the outer edge and not the inner hole edge.
result = result.edges("(>Z or <Z)").edges(cq.selectors.RadiusNthSelector(-1)).chamfer(chamfer_size)