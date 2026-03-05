import cadquery as cq

# Parameters for dimensions
plate_length = 200.0
plate_width = 140.0
plate_thickness = 5.0
corner_radius = 8.0

cutout_length = 50.0
cutout_width = 30.0
cutout_margin_x = 20.0  # Distance from the edge along the length
cutout_margin_y = 20.0  # Distance from the edge along the width

# Calculate the position of the cutout center
# Assuming the plate is centered at (0,0), we target the top-left corner (-X, +Y)
cut_x_pos = -(plate_length / 2) + cutout_margin_x + (cutout_length / 2)
cut_y_pos = (plate_width / 2) - cutout_margin_y - (cutout_width / 2)

# Create the base geometry
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the rectangular cutout
result = (
    result.faces(">Z")
    .workplane()
    .center(cut_x_pos, cut_y_pos)
    .rect(cutout_length, cutout_width)
    .cutThruAll()
)