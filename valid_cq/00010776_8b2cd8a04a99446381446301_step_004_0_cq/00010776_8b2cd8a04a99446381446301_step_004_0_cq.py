import cadquery as cq

# Parametric Dimensions
plate_length = 80.0
plate_width = 50.0
plate_thickness = 10.0
fillet_radius = 2.0

# Central hole pattern (Counterbored holes)
center_hole_spacing_x = 25.0
center_hole_spacing_y = 25.0
cb_hole_dia = 6.0
cb_head_dia = 12.0
cb_head_depth = 4.0

# Outer hole pattern (Simple small holes)
outer_hole_spacing_x = 65.0
outer_hole_spacing_y = 35.0
outer_hole_dia = 4.0

# Bottom boss
boss_dia = 30.0
boss_height = 10.0

# Create the main rectangular plate
plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Create the circular boss on the bottom
# We select the bottom face (<Z), create a circle, and extrude it downwards
boss = (
    plate.faces("<Z")
    .workplane()
    .circle(boss_dia / 2.0)
    .extrude(boss_height)
)

# Add the 4 central counterbored holes
# We use rect to define the centers, then cboreHole
part_with_center_holes = (
    boss.faces(">Z")
    .workplane()
    .rect(center_hole_spacing_x, center_hole_spacing_y, forConstruction=True)
    .vertices()
    .cboreHole(cb_hole_dia, cb_head_dia, cb_head_depth)
)

# Add the 4 outer mounting holes
# We use rect to define the centers, then hole
result = (
    part_with_center_holes.faces(">Z")
    .workplane()
    .rect(outer_hole_spacing_x, outer_hole_spacing_y, forConstruction=True)
    .vertices()
    .hole(outer_hole_dia)
)