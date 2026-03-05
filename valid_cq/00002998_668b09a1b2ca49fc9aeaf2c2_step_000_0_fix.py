import cadquery as cq

# Parameters
outer_width = 120
outer_height = 80
wall_thickness = 10
base_thickness = 5
total_height = 20
chamfer_size = 15

# Pin parameters
pin_radius = 5
pin_height = 15

# Create the outer octagonal prism
# Octagon approximated by chamfering a rectangle
outer = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(total_height)
)

# Chamfer the vertical edges to create octagonal shape
outer = outer.edges("|Z").chamfer(chamfer_size)

# Create inner cutout (octagonal hole)
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness
inner_chamfer = chamfer_size - wall_thickness

inner_cut = (
    cq.Workplane("XY")
    .rect(inner_width, inner_height)
    .extrude(total_height)
)

if inner_chamfer > 0:
    inner_cut = inner_cut.edges("|Z").chamfer(inner_chamfer)

# Subtract inner from outer to create the ring shape
# Move inner cut up by base_thickness to leave the base
inner_cut2 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(inner_width, inner_height)
    .extrude(total_height - base_thickness + 1)
)

if inner_chamfer > 0:
    inner_cut2 = inner_cut2.edges("|Z").chamfer(inner_chamfer)

result = outer.cut(inner_cut2)

# Add center pin on the base
pin = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(pin_radius)
    .extrude(pin_height)
)

result = result.union(pin)