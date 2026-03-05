import cadquery as cq

# Main dimensions
outer_width = 200
outer_height = 80
frame_depth = 15
wall_thickness = 20
inner_width = 120
inner_height = 40

# Create the main rectangular frame (like a picture frame)
# Outer rectangle minus inner rectangle

# Left panel
left_panel = (
    cq.Workplane("XY")
    .box(wall_thickness, outer_height, frame_depth)
)

# Right panel
right_panel = (
    cq.Workplane("XY")
    .transformed(offset=(outer_width - wall_thickness, 0, 0))
    .box(wall_thickness, outer_height, frame_depth)
)

# Top panel
top_panel = (
    cq.Workplane("XY")
    .transformed(offset=(outer_width/2, (outer_height - wall_thickness)/2, 0))
    .box(outer_width, wall_thickness, frame_depth)
)

# Bottom panel
bottom_panel = (
    cq.Workplane("XY")
    .transformed(offset=(outer_width/2, -(outer_height - wall_thickness)/2, 0))
    .box(outer_width, wall_thickness, frame_depth)
)

# Build frame as a single solid using union
frame = (
    cq.Workplane("XY")
    .box(outer_width, outer_height, frame_depth)
    .cut(
        cq.Workplane("XY")
        .box(outer_width - 2*wall_thickness, outer_height - 2*wall_thickness, frame_depth + 2)
    )
)

# Add corner/edge details - small tabs on corners
# Add mounting holes
hole_diameter = 6
hole_positions_top = [
    (30, outer_height/2 - wall_thickness/2),
    (70, outer_height/2 - wall_thickness/2),
    (130, outer_height/2 - wall_thickness/2),
    (170, outer_height/2 - wall_thickness/2),
]
hole_positions_bottom = [
    (30, -(outer_height/2 - wall_thickness/2)),
    (70, -(outer_height/2 - wall_thickness/2)),
    (130, -(outer_height/2 - wall_thickness/2)),
    (170, -(outer_height/2 - wall_thickness/2)),
]
hole_positions_left = [
    (wall_thickness/2, 0),
]
hole_positions_right = [
    (outer_width - wall_thickness/2, 0),
]

# Punch mounting holes through the frame
for x, y in hole_positions_top + hole_positions_bottom:
    frame = frame.cut(
        cq.Workplane("XY")
        .transformed(offset=(x - outer_width/2, y, 0))
        .cylinder(frame_depth + 2, hole_diameter/2)
    )

# Side holes
for x, y in hole_positions_left + hole_positions_right:
    frame = frame.cut(
        cq.Workplane("XY")
        .transformed(offset=(x - outer_width/2, y, 0))
        .cylinder(frame_depth + 2, hole_diameter/2)
    )

# Center divider bar (black element in the middle)
divider = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 0))
    .box(10, outer_height, frame_depth + 5)
)

# Combine frame with divider
assembly = frame.union(divider)

# Add a small pin/rod extending from divider
pin = (
    cq.Workplane("XZ")
    .transformed(offset=(-15, 0, 0))
    .circle(2)
    .extrude(20)
)

assembly = assembly.union(pin)

# Add small flange tabs on left and right sides
left_tab = (
    cq.Workplane("XY")
    .transformed(offset=(-outer_width/2 - 5, 0, -frame_depth/2 + 2))
    .box(10, outer_height, 4)
)

right_tab = (
    cq.Workplane("XY")
    .transformed(offset=(outer_width/2 + 5, 0, -frame_depth/2 + 2))
    .box(10, outer_height, 4)
)

assembly = assembly.union(left_tab).union(right_tab)

result = assembly