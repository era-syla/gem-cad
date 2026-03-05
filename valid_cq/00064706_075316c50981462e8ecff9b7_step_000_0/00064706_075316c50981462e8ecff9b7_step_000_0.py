import cadquery as cq

# Parametric dimensions derived from visual estimation
diameter = 20.0
radius = diameter / 2.0
vertical_top_len = 14.0       # Length of vertical section above intersection center
vertical_bottom_len = 40.0    # Length of vertical section below intersection center
horizontal_total_len = 36.0   # Total length of the horizontal section
fillet_r = 1.5                # Radius for the edge fillets

# 1. Create the vertical cylinder
# Centered at X=0, Y=0. Extrudes along Z axis.
# The intersection center is at Z=0.
vertical_cyl = (
    cq.Workplane("XY")
    .workplane(offset=-vertical_bottom_len)
    .circle(radius)
    .extrude(vertical_bottom_len + vertical_top_len)
)

# 2. Create the horizontal cylinder
# Centered at intersection (0,0,0). Extrudes along Y axis.
# We draw on the XZ plane (normal is Y) and extrude symmetrically.
horizontal_cyl = (
    cq.Workplane("XZ")
    .circle(radius)
    .extrude(horizontal_total_len / 2.0, both=True)
)

# 3. Combine the two cylinders into a single solid
result = vertical_cyl.union(horizontal_cyl)

# 4. Apply fillets to the ends
# Select the faces at the extremities (Top, Bottom, Left, Right)
# and fillet their outer edges.
result = (
    result
    .faces(">Z or <Z or >Y or <Y")
    .edges()
    .fillet(fillet_r)
)