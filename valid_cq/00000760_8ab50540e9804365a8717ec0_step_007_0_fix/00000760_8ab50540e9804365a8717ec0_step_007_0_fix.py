import cadquery as cq

# AA Battery dimensions (in mm)
battery_length = 50.5
battery_diameter = 14.5
battery_radius = battery_diameter / 2

# Positive terminal (nub) dimensions
nub_diameter = 5.5
nub_height = 1.5

# Negative terminal (flat with small indent) dimensions
neg_indent_diameter = 4.0
neg_indent_depth = 0.5

# Create the main battery body (cylinder)
body = (
    cq.Workplane("XY")
    .cylinder(battery_length, battery_radius)
)

# Add slight edge fillets to the main cylinder ends
body = (
    body
    .faces(">Z")
    .edges()
    .chamfer(0.5)
    .faces("<Z")
    .edges()
    .chamfer(0.5)
)

# Add positive terminal nub on top (+Z face)
nub = (
    cq.Workplane("XY")
    .workplane(offset=battery_length / 2)
    .circle(nub_diameter / 2)
    .extrude(nub_height)
)

# Add fillet to nub top edge
nub = (
    nub
    .faces(">Z")
    .edges()
    .fillet(0.5)
)

# Union body and nub
result = body.union(nub)

# Cut negative terminal indent on bottom (-Z face)
neg_cut = (
    cq.Workplane("XY")
    .workplane(offset=-(battery_length / 2))
    .circle(neg_indent_diameter / 2)
    .extrude(neg_indent_depth)
)

result = result.cut(neg_cut)