import cadquery as cq

# Main dimensions
length = 160
width = 130
height = 12
corner_radius = 8
wall_thickness = 3
lip_height = 2
lip_width = 4

# Create the main base body
base = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# Round the corners of the base
base = base.edges("|Z").fillet(corner_radius)

# Add chamfer to top edges
base = base.edges(">Z").chamfer(1.5)

# Add chamfer to bottom edges
base = base.edges("<Z").chamfer(1.0)

# Create a recessed panel on top (the sunken center)
recess_depth = 2
recess_margin = wall_thickness + lip_width

panel_recess = (
    cq.Workplane("XY")
    .workplane(offset=height - recess_depth)
    .rect(length - recess_margin * 2, width - recess_margin * 2)
    .extrude(recess_depth + 1)
)

# Cut the recess
base = base.cut(panel_recess)

# Add a lip/groove around the perimeter on the side
groove_depth = 1.5
groove_height = 2
groove_z = height / 2

groove = (
    cq.Workplane("XY")
    .workplane(offset=groove_z)
    .rect(length + 1, width + 1)
    .rect(length - groove_depth * 2, width - groove_depth * 2)
    .extrude(groove_height)
)

base = base.cut(groove)

# Add mounting screw holes (4 corners, recessed)
screw_radius = 2.5
screw_depth = 6
screw_offset_x = length / 2 - 18
screw_offset_y = width / 2 - 15

screw_positions = [
    (screw_offset_x, screw_offset_y),
    (-screw_offset_x, screw_offset_y),
    (screw_offset_x, -screw_offset_y),
    (-screw_offset_x, -screw_offset_y),
]

for x, y in screw_positions:
    screw_hole = (
        cq.Workplane("XY")
        .workplane(offset=height - recess_depth)
        .center(x, y)
        .circle(screw_radius)
        .extrude(screw_depth)
    )
    base = base.cut(screw_hole)

    # Countersink
    countersink = (
        cq.Workplane("XY")
        .workplane(offset=height - recess_depth)
        .center(x, y)
        .circle(screw_radius + 1.5)
        .extrude(1.5)
    )
    base = base.cut(countersink)

result = base