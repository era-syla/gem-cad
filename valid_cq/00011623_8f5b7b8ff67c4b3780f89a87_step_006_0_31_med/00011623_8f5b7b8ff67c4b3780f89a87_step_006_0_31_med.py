import cadquery as cq

# Parameters for the main plate
plate_length = 200.0
plate_width = 150.0
plate_thickness = 3.0
outer_corner_radius = 5.0

# Parameters for the rectangular cutout
hole_length = 40.0
hole_width = 25.0
hole_corner_radius = 2.0
margin_x = 15.0
margin_y = 10.0

# 1. Create the base plate and apply fillets to the vertical edges (outer corners)
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)
plate = plate.edges("|Z").fillet(outer_corner_radius)

# 2. Calculate the center position of the hole relative to the origin (center of plate)
# Positioning the hole at the top-left corner (min X, max Y)
hx = -plate_length / 2.0 + margin_x + hole_length / 2.0
hy = plate_width / 2.0 - margin_y - hole_width / 2.0

# 3. Create a separate tool body for the hole with its own corner fillets
hole_tool = (
    cq.Workplane("XY")
    .center(hx, hy)
    .box(hole_length, hole_width, plate_thickness * 3.0) # Taller to ensure a clean cut
    .edges("|Z")
    .fillet(hole_corner_radius)
)

# 4. Perform the boolean cut to create the final geometry
result = plate.cut(hole_tool)