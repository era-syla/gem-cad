import cadquery as cq

# Dimensions
base_length = 120
base_width = 20
base_height = 6

arch_height = 35
arch_width = 80
arch_thickness = 10

hole_radius = 10
hole_spacing = 25

# Build the base plate
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Build the arch body - a rectangular block with rounded top
# The arch sits centered on the base plate
arch_inner_width = arch_width
arch_outer_width = arch_width + arch_thickness * 2
arch_outer_height = arch_height + arch_thickness / 2
arch_depth = base_width

# Create the arch as an extruded profile
# Profile: rectangle with semicircle on top, then subtract inner rectangle with semicircle
def make_arch_profile(wp, outer_w, outer_h, inner_w, inner_h, thickness):
    # Outer profile: rect bottom + semicircle top
    # Inner profile: rect bottom + semicircle top (offset by thickness)
    pass

# Use a 2D profile approach
outer_w = arch_width + arch_thickness * 2
outer_h = arch_height
inner_w = arch_width
inner_h = arch_height - arch_thickness

# Create arch profile on XZ plane
arch = (
    cq.Workplane("XZ")
    .workplane(offset=-arch_depth / 2)
    .moveTo(-outer_w / 2, 0)
    .lineTo(-outer_w / 2, outer_h - outer_w / 2)
    .threePointArc((0, outer_h), (outer_w / 2, outer_h - outer_w / 2))
    .lineTo(outer_w / 2, 0)
    .lineTo(-outer_w / 2, 0)
    .close()
    .extrude(arch_depth)
)

# Inner cutout
inner_cut = (
    cq.Workplane("XZ")
    .workplane(offset=-arch_depth / 2)
    .moveTo(-inner_w / 2, arch_thickness)
    .lineTo(-inner_w / 2, arch_thickness + inner_h - inner_w / 2)
    .threePointArc((0, arch_thickness + inner_h), (inner_w / 2, arch_thickness + inner_h - inner_w / 2))
    .lineTo(inner_w / 2, arch_thickness)
    .lineTo(-inner_w / 2, arch_thickness)
    .close()
    .extrude(arch_depth)
)

arch = arch.cut(inner_cut)

# Position arch on top of base
arch = arch.translate((0, 0, base_height / 2))

# Combine base and arch
combined = base.union(arch)

# Cut three circular holes through the arch
# Holes are in the vertical face of the arch (through Y direction)
# Hole centers: evenly spaced, centered at x=0, z positions in middle of arch opening
hole_y_depth = arch_depth + 2

hole_z = base_height / 2 + arch_thickness + hole_radius + 2

# Three holes spaced along X
hole_positions = [-hole_spacing, 0, hole_spacing]

for x_pos in hole_positions:
    hole = (
        cq.Workplane("XY")
        .workplane(offset=-hole_y_depth / 2)
        .center(x_pos, hole_z)
        .circle(hole_radius)
        .extrude(hole_y_depth)
    )
    combined = combined.cut(hole)

# Add fillets to smooth edges
result = combined.edges("|Y").fillet(1.5)