import cadquery as cq

# Main motor body (stepper motor like block)
motor_body = (
    cq.Workplane("XY")
    .box(42, 42, 48)
)

# Front face plate
front_plate = (
    cq.Workplane("XY")
    .workplane(offset=24)
    .box(42, 42, 4)
)

# Combine motor body with front plate
motor = motor_body.union(front_plate)

# Add mounting holes on front face (4 corners)
motor = (
    motor
    .faces(">Z")
    .workplane()
    .pushPoints([(15, 15), (-15, 15), (15, -15), (-15, -15)])
    .hole(3.5, 6)
)

# Center hole on front face (output shaft hole)
motor = (
    motor
    .faces(">Z")
    .workplane()
    .hole(8, 10)
)

# Output shaft extending from front
output_shaft = (
    cq.Workplane("XY")
    .workplane(offset=26)
    .circle(2)
    .extrude(60)
)

motor = motor.union(output_shaft)

# Gearbox section on the side
gearbox = (
    cq.Workplane("YZ")
    .workplane(offset=-21)
    .rect(38, 28)
    .extrude(20)
)

motor = motor.union(gearbox)

# Mounting bracket (L-bracket)
bracket_base = (
    cq.Workplane("XY")
    .workplane(offset=-24)
    .rect(52, 8)
    .extrude(4)
    .translate((0, -21, 0))
)

bracket_vert = (
    cq.Workplane("YZ")
    .workplane(offset=-26)
    .rect(8, 40)
    .extrude(4)
    .translate((0, -21, -4))
)

bracket = bracket_base.union(bracket_vert)

# Add mounting holes to bracket
bracket = (
    bracket
    .faces("<X")
    .workplane()
    .pushPoints([(0, 10), (0, -10)])
    .hole(4.5, 8)
)

motor = motor.union(bracket)

# Top cable/wire coming out of top
wire_top = (
    cq.Workplane("XY")
    .workplane(offset=26)
    .center(8, 8)
    .circle(1)
    .extrude(50)
)

motor = motor.union(wire_top)

# Small connector block on top
connector = (
    cq.Workplane("XY")
    .workplane(offset=26)
    .center(5, 5)
    .rect(12, 10)
    .extrude(8)
)

motor = motor.union(connector)

# Round protrusion on gearbox side (gear output)
gear_output = (
    cq.Workplane("XZ")
    .workplane(offset=25)
    .circle(8)
    .extrude(6)
    .translate((0, 0, 0))
)

# Side shaft from gearbox
side_shaft = (
    cq.Workplane("XZ")
    .workplane(offset=31)
    .circle(3)
    .extrude(2)
)

result = motor.union(gear_output).union(side_shaft)