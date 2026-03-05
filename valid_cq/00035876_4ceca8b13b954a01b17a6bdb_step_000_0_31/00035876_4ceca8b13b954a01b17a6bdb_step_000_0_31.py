import cadquery as cq

# Parametric dimensions
length = 120.0
width = 48.0
thickness = 4.0

border_width = 4.0
center_rib_width = 4.0
slat_width = 2.0
slot_width = 5.0
num_slots = 6

leg_size = 4.0
leg_height = 30.0
leg_inset_x = 25.0
# Center the leg exactly under the solid border
leg_inset_y = border_width / 2.0 

# Create the main rectangular top
top = cq.Workplane("XY").box(length, width, thickness)

# Calculate slot dimensions and positions
slot_length = (length - 2 * border_width - center_rib_width) / 2.0
x_offset = slot_length / 2.0 + center_rib_width / 2.0

y_start = -width / 2.0 + border_width + slot_width / 2.0
y_step = slot_width + slat_width

# Generate points for all slots
slot_pts = []
for i in range(num_slots):
    y_pos = y_start + i * y_step
    slot_pts.append((-x_offset, y_pos))
    slot_pts.append((x_offset, y_pos))

# Cut the slots through the top
top_with_slots = (
    top.faces(">Z")
    .workplane()
    .pushPoints(slot_pts)
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# Generate points for the legs
leg_pts = [
    (length / 2.0 - leg_inset_x, width / 2.0 - leg_inset_y),
    (length / 2.0 - leg_inset_x, -(width / 2.0 - leg_inset_y)),
    (-(length / 2.0 - leg_inset_x), width / 2.0 - leg_inset_y),
    (-(length / 2.0 - leg_inset_x), -(width / 2.0 - leg_inset_y))
]

# Extrude the legs from the bottom face
result = (
    top_with_slots.faces("<Z")
    .workplane()
    .pushPoints(leg_pts)
    .rect(leg_size, leg_size)
    .extrude(leg_height)
)