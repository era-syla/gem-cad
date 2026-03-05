import cadquery as cq

# Main box dimensions
box_w = 60
box_d = 60
box_h = 50
wall = 4

# Create the outer box shell (open top)
outer = cq.Workplane("XY").box(box_w, box_d, box_h)

# Create inner cutout (hollow inside, open top)
inner = cq.Workplane("XY").box(
    box_w - 2*wall,
    box_d - 2*wall,
    box_h - wall
).translate((0, 0, wall/2))

result = outer.cut(inner)

# Add back plate that extends above the box
# Back plate is attached to the back face, extending upward
plate_w = box_w + 10
plate_h = 40
plate_thick = wall

# Back plate centered on back face, extending above box top
back_plate = (
    cq.Workplane("XY")
    .box(plate_w, plate_thick, plate_h)
    .translate((0, -(box_d/2 + plate_thick/2), box_h/2 + plate_h/2 - plate_h/2))
)

# Position back plate so its bottom aligns with box top and it extends upward
back_plate = (
    cq.Workplane("XY")
    .box(plate_w, plate_thick, plate_h)
    .translate((0, -(box_d/2 + plate_thick/2), box_h/2 + plate_h/2 - 10))
)

result = result.union(back_plate)

# Add mounting holes to back plate
# The back plate is at y = -(box_d/2 + plate_thick/2), z centered at box_h/2 + plate_h/2 - 10
plate_z_center = box_h/2 + plate_h/2 - 10
plate_y = -(box_d/2 + plate_thick/2)

# Cut mounting holes in back plate (3 holes: top-left, top-right, center-right area)
hole_r = 3
# Holes positions relative to plate center
hole_positions = [
    (-plate_w/2 + 10, plate_z_center + plate_h/2 - 10),
    (plate_w/2 - 10, plate_z_center + plate_h/2 - 10),
    (plate_w/2 - 10, plate_z_center + plate_h/2 - 25),
]

for hx, hz in hole_positions:
    hole_cyl = (
        cq.Workplane("XZ")
        .workplane(offset=plate_y + plate_thick)
        .center(hx, hz)
        .circle(hole_r)
        .extrude(plate_thick + 2)
        .translate((0, -(plate_thick + 2), 0))
    )
    result = result.cut(hole_cyl)

# Cut small rectangular slot in back plate (center)
slot = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(plate_y, plate_z_center + plate_h/2 - 15)
    .rect(plate_thick + 2, 8)
    .extrude(6)
    .translate((-3, 0, 0))
)
result = result.cut(slot)

# Cut circular hole in front face of box (lower area)
front_hole = (
    cq.Workplane("XY")
    .workplane(offset=box_d/2)
    .center(0, -box_h/2 + 12)
    .circle(6)
    .extrude(wall + 2)
    .translate((0, -(wall + 2), 0))
)
result = result.cut(front_hole)