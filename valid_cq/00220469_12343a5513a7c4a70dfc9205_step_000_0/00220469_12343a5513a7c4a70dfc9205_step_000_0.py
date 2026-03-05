import cadquery as cq

# --- Parameters ---
# Main body dimensions
body_length = 320.0
body_width = 46.0
body_height = 46.0
body_y_offset = -12.0  # Offset relative to the head center

# Front Head (Drive housing)
head_width = 95.0
head_height = 68.0
head_depth = 35.0

# Motor dimensions
motor_dia = 42.0
motor_length = 130.0
gearbox_len = 35.0
motor_y_offset = 28.0
motor_z_offset = 5.0

# Carriage dimensions
carriage_len = 110.0
carriage_width = 50.0
carriage_thk = 6.0
carriage_pos = 120.0

# --- Geometry Construction ---

# 1. Front Head Block
# Created centered on YZ, extruded towards negative X
head = (
    cq.Workplane("YZ")
    .rect(head_width, head_height)
    .extrude(head_depth)
    .translate((-head_depth/2, 0, 0))  # Move so front face is at -head_depth
    .edges("|X").fillet(3.0)
)

# Front Boss (Output Shaft Housing)
boss = (
    cq.Workplane("YZ")
    .workplane(offset=-head_depth)
    .circle(16)
    .extrude(12)
)
# Shaft Hole
shaft_hole = (
    boss.faces(">X").workplane()
    .circle(10)
    .cutBlind(-15)
)
head = head.union(boss).cut(shaft_hole)

# 2. Main Body (Profile)
# Extruded from X=0 towards positive X
body = (
    cq.Workplane("YZ")
    .rect(body_width, body_height)
    .extrude(body_length)
    .translate((body_length/2, body_y_offset, 0))
)

# Add T-Slots to the body (Top and Side)
slot_w = 6.0
slot_d = 3.0
top_slot = (
    cq.Workplane("XY")
    .rect(body_length, slot_w)
    .extrude(-slot_d)
    .translate((body_length/2, body_y_offset, body_height/2))
)
side_slot = (
    cq.Workplane("XY")
    .rect(body_length, slot_d)
    .extrude(slot_w)
    .translate((body_length/2, body_y_offset + body_width/2 - slot_d/2, 0))
    .rotate((0,0,0), (1,0,0), 90)
)
body = body.cut(top_slot).cut(side_slot)

# 3. Motor Assembly
# Gearbox connecting head to motor
gearbox = (
    cq.Workplane("YZ")
    .rect(42, 42)
    .extrude(gearbox_len)
    .translate((gearbox_len/2, motor_y_offset, motor_z_offset))
)

# Cylindrical Motor body
motor = (
    cq.Workplane("YZ")
    .workplane(offset=gearbox_len)
    .circle(motor_dia/2)
    .extrude(motor_length)
    .translate((0, motor_y_offset, motor_z_offset))
)

# Connector box on motor
motor_conn = (
    cq.Workplane("XY")
    .rect(22, 22)
    .extrude(12)
    .translate((gearbox_len + 30, motor_y_offset, motor_z_offset + motor_dia/2))
)

motor_assy = gearbox.union(motor).union(motor_conn)

# 4. Carriage (Slider)
carriage_plate = (
    cq.Workplane("XY")
    .rect(carriage_len, carriage_width)
    .extrude(carriage_thk)
    .translate((carriage_pos, body_y_offset, body_height/2 + carriage_thk/2))
)

# Details on carriage (Shock absorbers/Connectors)
cyl_detail = (
    cq.Workplane("YZ")
    .circle(6)
    .extrude(50)
    .translate((carriage_pos - 10, body_y_offset - 8, body_height/2 + carriage_thk + 6))
)
cyl_detail2 = cyl_detail.translate((0, 16, 0))

carriage_assy = carriage_plate.union(cyl_detail).union(cyl_detail2)

# 5. Accessories on Body
# Pneumatic Fittings on side
fitting = (
    cq.Workplane("XZ")
    .circle(4)
    .extrude(15)
    .translate((0, body_y_offset + body_width/2, -8))
    .rotate((0,0,0), (1,0,0), -90)
)
fit1 = fitting.translate((60, 0, 0))
fit2 = fitting.translate((85, 0, 0))

# Sensor block on side slot
sensor = (
    cq.Workplane("XY")
    .rect(25, 12)
    .extrude(8)
    .rotate((0,0,0), (1,0,0), 90)
    .translate((180, body_y_offset + body_width/2, -5))
)

# 6. Rear End Cap
rear_cap = (
    cq.Workplane("YZ")
    .rect(body_width, body_height)
    .extrude(15)
    .translate((body_length + 7.5, body_y_offset, 0))
)
rear_conn = (
    cq.Workplane("YZ")
    .circle(9)
    .extrude(12)
    .translate((body_length + 15 + 6, body_y_offset, 0))
)
rear_assy = rear_cap.union(rear_conn)

# --- Final Boolean Union ---
result = (
    head
    .union(body)
    .union(motor_assy)
    .union(carriage_assy)
    .union(fit1)
    .union(fit2)
    .union(sensor)
    .union(rear_assy)
)