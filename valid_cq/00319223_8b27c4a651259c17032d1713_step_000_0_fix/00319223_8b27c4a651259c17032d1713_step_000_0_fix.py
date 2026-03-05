import cadquery as cq

head_radius = 30
thickness = 4
handle_length = 40
handle_width_top = 12
handle_width_bottom = 20
hole_d = 4
hole_radius = hole_d / 2
cols = 13
rows = 10
dx = 6
dy = 6
slot_length = 20
slot_width = 6
slot_offset_y = -head_radius / 3

# Create head
head = cq.Workplane("XY").circle(head_radius).extrude(thickness)

# Create handle
handle = (
    cq.Workplane("XY")
    .moveTo(-handle_width_top / 2, -head_radius)
    .lineTo(handle_width_top / 2, -head_radius)
    .lineTo(handle_width_bottom / 2, -head_radius - handle_length)
    .lineTo(-handle_width_bottom / 2, -head_radius - handle_length)
    .close()
    .extrude(thickness)
)

# Combine head and handle
result = head.union(handle)

# Drill array of holes in head
hole_positions = []
for i in range(cols):
    for j in range(rows):
        x = (i - (cols - 1) / 2) * dx
        y = (j - (rows - 1) / 2) * dy
        if x * x + y * y <= (head_radius - hole_radius) ** 2:
            hole_positions.append((x, y))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_radius)
    .cutThruAll()
)

# Cut central slot
result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_offset_y)
    .rect(slot_length, slot_width)
    .cutThruAll()
)