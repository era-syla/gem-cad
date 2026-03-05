import cadquery as cq

# Parameters
R_big = 15
R_small = 10
wall_thickness = 3
length = 20
fillet_radius = 1
small_offset = R_big + R_small - wall_thickness

# Create outer cylinders
outer_big = cq.Workplane("YZ").cylinder(length, R_big)
outer_small = cq.Workplane("YZ").center(0, small_offset).cylinder(length, R_small)
combined_outer = outer_big.union(outer_small)

# Create inner cutout cylinders (slightly longer to ensure clean cut)
inner_big = cq.Workplane("YZ").cylinder(length + 2, R_big - wall_thickness)
inner_small = cq.Workplane("YZ").center(0, small_offset).cylinder(length + 2, R_small - wall_thickness)
combined_inner = inner_big.union(inner_small)

# Cut the inner material and apply fillets, then center on X-axis
result = (
    combined_outer
    .cut(combined_inner)
    .edges().fillet(fillet_radius)
    .translate((-length/2, 0, 0))
)