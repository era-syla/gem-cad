import cadquery as cq

# Parameters for the nameplate
plate_length = 120.0
plate_width = 30.0
base_thickness = 2.0
rim_height = 1.0
rim_thickness = 1.5
corner_radius = 2.0

text_string = "Ed Sherman"
font_size = 14
text_extrusion = 1.0

# 1. Create the main body block (base + rim)
# This represents the full outer volume before cutting the pocket
main_body = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, base_thickness + rim_height)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Create the pocket (cutout) to form the rim
# Calculate dimensions for the inner pocket
pocket_length = plate_length - (2 * rim_thickness)
pocket_width = plate_width - (2 * rim_thickness)
# Ensure pocket fillet is concentric with outer fillet
pocket_fillet = max(0.1, corner_radius - rim_thickness)

pocket = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .box(pocket_length, pocket_width, rim_height)
    .edges("|Z")
    .fillet(pocket_fillet)
)

# Cut the pocket from the main body to create the tray shape
plate_base = main_body.cut(pocket)

# 3. Add the embossed text
# The text sits on the floor of the pocket (at z = base_thickness)
text_obj = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .text(
        text_string,
        fontsize=font_size,
        distance=text_extrusion,
        font="Serif",
        halign="center",
        valign="center"
    )
)

# 4. Add the small circular detail feature
# Located near the corner inside the pocket
feature_radius = 0.8
feature_offset_x = -(pocket_length / 2) + 3.0
feature_offset_y = -(pocket_width / 2) + 3.0

detail_feature = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(feature_offset_x, feature_offset_y)
    .circle(feature_radius)
    .extrude(text_extrusion)
)

# 5. Combine all geometry into the final result
result = plate_base.union(text_obj).union(detail_feature)