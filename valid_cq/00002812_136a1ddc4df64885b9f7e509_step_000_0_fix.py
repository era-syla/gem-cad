import cadquery as cq

# Main dimensions
piano_length = 140
piano_depth = 30
piano_height = 15
piano_y_offset = 60  # height from ground to bottom of piano body

# Stand leg dimensions
leg_width = 8
leg_depth = 28
leg_height = piano_y_offset
leg_x_offset = 10

# Cross brace
brace_width = piano_length - 2 * leg_x_offset - leg_width
brace_height = 6
brace_depth = 4
brace_z = 15

# Build the piano body (main box)
piano_body = (
    cq.Workplane("XY")
    .box(piano_length, piano_depth, piano_height)
    .translate((0, 0, piano_y_offset + piano_height / 2))
)

# Add keyboard area - slightly raised panel on top front
keyboard_panel = (
    cq.Workplane("XY")
    .box(piano_length - 10, piano_depth * 0.6, 3)
    .translate((0, -piano_depth * 0.2, piano_y_offset + piano_height + 1.5))
)

# White keys representation (simplified as a box with slight detail)
white_keys = (
    cq.Workplane("XY")
    .box(piano_length - 14, piano_depth * 0.55, 4)
    .translate((0, -piano_depth * 0.22, piano_y_offset + piano_height + 2))
)

# Black keys (slightly narrower, thinner, raised)
black_keys = (
    cq.Workplane("XY")
    .box(piano_length - 20, piano_depth * 0.3, 3)
    .translate((0, -piano_depth * 0.3, piano_y_offset + piano_height + 4.5))
)

# Left leg
left_leg = (
    cq.Workplane("XY")
    .box(leg_width, leg_depth, leg_height)
    .translate((-(piano_length / 2 - leg_x_offset - leg_width / 2), 0, leg_height / 2))
)

# Right leg
right_leg = (
    cq.Workplane("XY")
    .box(leg_width, leg_depth, leg_height)
    .translate(((piano_length / 2 - leg_x_offset - leg_width / 2), 0, leg_height / 2))
)

# Cross brace connecting the two legs
cross_brace = (
    cq.Workplane("XY")
    .box(brace_width, brace_depth, brace_height)
    .translate((0, -piano_depth * 0.3, brace_z + brace_height / 2))
)

# Back panel (thin vertical panel at rear)
back_panel = (
    cq.Workplane("XY")
    .box(piano_length, 2, piano_height * 0.8)
    .translate((0, piano_depth / 2 - 1, piano_y_offset + piano_height * 0.4))
)

# Combine all parts
result = (
    piano_body
    .union(keyboard_panel)
    .union(white_keys)
    .union(black_keys)
    .union(left_leg)
    .union(right_leg)
    .union(cross_brace)
    .union(back_panel)
)