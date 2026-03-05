import cadquery as cq

# Parametric dimensions
plate_length = 150.0
plate_width = 100.0
plate_thickness = 2.0
outer_corner_radius = 4.0

hole_length = 15.0
hole_width = 30.0
inner_corner_radius = 2.0
margin_x = 8.0
margin_y = 8.0

# Calculate hole center position near one corner
hole_cx = (plate_length / 2.0) - margin_x - (hole_length / 2.0)
hole_cy = (plate_width / 2.0) - margin_y - (hole_width / 2.0)

# Create the main plate with filleted outer corners
base_plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(outer_corner_radius)
)

# Create the cutting tool for the hole with its own filleted corners
hole_cutter = (
    cq.Workplane("XY")
    .center(hole_cx, hole_cy)
    .box(hole_length, hole_width, plate_thickness * 5.0)  # Taller to ensure clean through-cut
    .edges("|Z")
    .fillet(inner_corner_radius)
)

# Perform the boolean cut to create the final geometry
result = base_plate.cut(hole_cutter)