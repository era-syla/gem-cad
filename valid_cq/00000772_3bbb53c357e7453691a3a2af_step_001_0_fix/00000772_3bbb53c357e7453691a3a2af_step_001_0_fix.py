import cadquery as cq

# Main cylinder body
cylinder_radius = 15
cylinder_height = 50
cylinder_z = 0

main_body = (
    cq.Workplane("XY")
    .cylinder(cylinder_height, cylinder_radius)
)

# Top cap / transition piece
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height/2)
    .circle(cylinder_radius)
    .workplane(offset=5)
    .circle(cylinder_radius * 0.7)
    .loft()
)

# Rod / shaft extending upward
rod_radius = 5
rod_height = 60

rod = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height/2 + 5)
    .cylinder(rod_height, rod_radius)
)

# Hex nut at top of rod
nut_z = cylinder_height/2 + 5 + rod_height
nut = (
    cq.Workplane("XY")
    .workplane(offset=nut_z)
    .polygon(6, rod_radius * 2.5)
    .extrude(5)
)

# Bottom clevis / mounting bracket
clevis_width = 10
clevis_height = 15
clevis_thickness = 5
clevis_hole_radius = 3

# Left clevis tab
left_clevis = (
    cq.Workplane("XY")
    .workplane(offset=-cylinder_height/2 - clevis_height)
    .center(-cylinder_radius * 0.6, 0)
    .rect(clevis_thickness, clevis_width)
    .extrude(clevis_height)
)

left_clevis_hole = (
    cq.Workplane("YZ")
    .workplane(offset=-cylinder_radius * 0.6 - clevis_thickness/2)
    .center(0, -cylinder_height/2 - clevis_height/2)
    .circle(clevis_hole_radius)
    .extrude(clevis_thickness)
)

# Right clevis tab
right_clevis = (
    cq.Workplane("XY")
    .workplane(offset=-cylinder_height/2 - clevis_height)
    .center(cylinder_radius * 0.6, 0)
    .rect(clevis_thickness, clevis_width)
    .extrude(clevis_height)
)

right_clevis_hole = (
    cq.Workplane("YZ")
    .workplane(offset=cylinder_radius * 0.6 - clevis_thickness/2)
    .center(0, -cylinder_height/2 - clevis_height/2)
    .circle(clevis_hole_radius)
    .extrude(clevis_thickness)
)

# Combine all parts
result = (
    main_body
    .union(top_cap)
    .union(rod)
    .union(nut)
    .union(left_clevis)
    .cut(left_clevis_hole)
    .union(right_clevis)
    .cut(right_clevis_hole)
)

# Add fillets to main body edges
result = (
    result
    .edges("|Z")
    .fillet(0.5)
)