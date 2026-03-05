import cadquery as cq

# Parametric dimensions
length = 80.0
outer_diameter = 10.0
inner_diameter = 5.0
groove_width = 1.5
groove_depth = 0.75
groove_land_top = 2.5  # Distance from top face to the start of the groove
top_chamfer_size = 0.5

# 1. Create the main cylinder body
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(length)

# 2. Cut the central through-hole
# Selecting the top face and making a hole through the entire part
result = result.faces(">Z").workplane().hole(inner_diameter)

# 3. Cut the circumferential groove
# Calculate the Z-height where the groove starts (from the bottom)
# The groove sits below the top "land"
groove_z_start = length - groove_land_top - groove_width

# Create a cutting tool (a ring) to subtract the material for the groove
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=groove_z_start)
    .circle(outer_diameter / 2.0 + 2.0)            # Outer boundary (clearance)
    .circle(outer_diameter / 2.0 - groove_depth)   # Inner boundary (depth of cut)
    .extrude(groove_width)
)

# Apply the cut
result = result.cut(groove_cutter)

# 4. Apply chamfer to the top outer edge
# We select the top face, then filter for the edge closest to the outer perimeter
result = result.faces(">Z").edges(
    cq.NearestToPointSelector((outer_diameter / 2.0, 0, length))
).chamfer(top_chamfer_size)

# Optional: Apply a small chamfer to the bottom edge for a finished look
result = result.faces("<Z").edges(
    cq.NearestToPointSelector((outer_diameter / 2.0, 0, 0))
).chamfer(top_chamfer_size)