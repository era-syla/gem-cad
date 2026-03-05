import cadquery as cq

thickness = 5.0

# 2D side profile vertices (XY plane)
side_profile = [
    (0, 15),
    (0, 0),
    (60, 0),
    (75, -10),
    (80, -10),
    (80, 0),
    (100, 0),
    (100, 15),
    (80, 15),
    (60, 15),
]

# Extrude the side profile to create the main body
result = (
    cq.Workplane("XY")
    .polyline(side_profile)
    .close()
    .extrude(thickness)
)

# Parameters for the U‐channel cutout at the bracket end
bracket_x1 = 80
bracket_x2 = 100
wall_thickness = 2.0
cut_width = (bracket_x2 - bracket_x1) - 2 * wall_thickness
channel_depth = 10.0
top_y = 15.0
bottom_y = top_y - channel_depth

# Center of the cut rectangle
cut_cx = bracket_x1 + wall_thickness + cut_width / 2.0
cut_cy = (top_y + bottom_y) / 2.0

# Subtract the U‐channel from the top face through the full thickness
result = (
    result
    .faces(">Z")
    .workplane()
    .center(cut_cx, cut_cy)
    .rect(cut_width, channel_depth)
    .cutThruAll()
)