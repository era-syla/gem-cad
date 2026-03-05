import cadquery as cq

# Parameters
base_diameter = 80.0
base_height = 15.0
base_fillet_radius = 5.0

stem_diameter = 4.0
stem_height = 120.0
stem_fillet_radius = 5.0  # Fillet where stem meets base

bore_diameter = 1.5  # Small hole at the top
bore_depth = 10.0

# Construction
# 1. Create the base cylinder
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# 2. Fillet the top edge of the base
base = base.edges(">Z").fillet(base_fillet_radius)

# 3. Create the vertical stem
# We start from the top face of the base
stem = (
    base.faces(">Z")
    .workplane()
    .circle(stem_diameter / 2)
    .extrude(stem_height)
)

# 4. Fillet the connection between the stem and the base
# We need to select the edge at the bottom of the stem (which is now part of the union)
# A robust way is to select edges near the Z-height of the base top
result = stem.edges(
    cq.selectors.NearestToPointSelector((0, 0, base_height))
).fillet(stem_fillet_radius)

# 5. Add the small bore hole at the top of the stem
result = (
    result.faces(">Z")
    .workplane()
    .circle(bore_diameter / 2)
    .cutBlind(-bore_depth)
)