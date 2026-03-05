import cadquery as cq

# Parametric dimensions for a standard 2020 T-slot aluminum extrusion
length = 300.0
width = 20.0
height = 20.0

outer_slot_width = 6.2
outer_slot_depth = 1.8
inner_slot_width = 11.5
inner_slot_depth = 4.5

center_hole_dia = 5.0
corner_radius = 1.5

# 1. Create the base block with filleted outer corners
base = (
    cq.Workplane("XY")
    .box(width, height, length)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Add the center hole extending entirely through the extrusion
result = base.faces(">Z").workplane().hole(center_hole_dia)

# 3. Create the T-slot cutter geometry
# Built on the right-side (+X) face, to be rotated for the other sides
cut_length = length + 2.0  # Extended slightly to ensure clean boolean cuts

outer_cut = (
    cq.Workplane("XY")
    .box(outer_slot_depth, outer_slot_width, cut_length)
    .translate((width / 2.0 - outer_slot_depth / 2.0, 0, 0))
)

inner_cut = (
    cq.Workplane("XY")
    .box(inner_slot_depth, inner_slot_width, cut_length)
    .translate((width / 2.0 - outer_slot_depth - inner_slot_depth / 2.0, 0, 0))
)

cutter = outer_cut.union(inner_cut)

# 4. Subtract the T-slot cutter from all four sides
result = result.cut(cutter)
result = result.cut(cutter.rotate((0, 0, 0), (0, 0, 1), 90))
result = result.cut(cutter.rotate((0, 0, 0), (0, 0, 1), 180))
result = result.cut(cutter.rotate((0, 0, 0), (0, 0, 1), 270))