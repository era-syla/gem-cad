import cadquery as cq

# Parameters
base_radius = 20
center_hole_radius = 6
base_thickness = 4
fin_height = 12
fin_thickness = 2
fin_inner_radius = center_hole_radius
fin_outer_radius = base_radius + 3
num_fins = 6

# Create base disk and cut center hole
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
    .faces(">Z")
    .workplane()
    .circle(center_hole_radius)
    .cutThruAll()
)

# Create and union fins
fins = cq.Workplane("XY")
for i in range(num_fins):
    fin = (
        cq.Workplane("XY")
        .rect(fin_thickness, fin_outer_radius - fin_inner_radius)
        .translate((0, fin_inner_radius + (fin_outer_radius - fin_inner_radius) / 2, base_thickness))
        .rotate((0, 0, 0), (0, 0, 1), i * 360 / num_fins)
        .extrude(fin_height)
    )
    fins = fins.union(fin)

result = base.union(fins)