import cadquery as cq

outer_radius = 10
height = 150
slot_depth = 40
gap_width = 5
hole_diameter = 5
hole_offset = 15

prong_thickness = (2*outer_radius - gap_width)/2
prong_center = gap_width/2 + prong_thickness/2

# main cylinder
result = cq.Workplane("XY").cylinder(height, outer_radius)

# cut the top slot
slot = cq.Workplane("XY").box(gap_width, 2*outer_radius*1.1, slot_depth)
slot = slot.translate((0, 0, height - slot_depth/2))
result = result.cut(slot)

# cut the two radial holes in the prongs
hole_cut = (
    cq.Workplane("XZ")
    .pushPoints([
        (prong_center, height - hole_offset),
        (-prong_center, height - hole_offset)
    ])
    .circle(hole_diameter/2)
    .extrude(2*outer_radius + 2, both=True)
)
result = result.cut(hole_cut)