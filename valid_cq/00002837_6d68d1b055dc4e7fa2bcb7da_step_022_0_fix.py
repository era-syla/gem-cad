import cadquery as cq

# Two stacked NEMA stepper motors with mounting flanges and shafts
# Motor dimensions (NEMA 17 style)
motor_size = 42  # 42mm square
motor_length = 40  # motor body length
corner_radius = 3
shaft_dia = 5
shaft_length = 24
mount_hole_spacing = 31  # center to center
flange_thickness = 3

def make_stepper_motor(offset_z=0):
    # Main motor body - square with rounded corners
    body = (
        cq.Workplane("XY").workplane(offset=offset_z)
        .rect(motor_size, motor_size)
        .extrude(motor_length)
    )
    
    # Round the vertical edges of the body
    body = body.edges("|Z").fillet(corner_radius)
    
    # Front flange plate
    flange = (
        cq.Workplane("XY").workplane(offset=offset_z + motor_length)
        .rect(motor_size, motor_size)
        .extrude(flange_thickness)
    )
    flange = flange.edges("|Z").fillet(corner_radius)
    
    # Mounting holes in flange - corner holes
    hole_offset = mount_hole_spacing / 2
    flange = (
        flange
        .faces(">Z")
        .workplane()
        .pushPoints([
            (hole_offset, hole_offset),
            (-hole_offset, hole_offset),
            (hole_offset, -hole_offset),
            (-hole_offset, -hole_offset),
        ])
        .hole(3.2)
    )
    
    # Shaft boss on front face
    boss = (
        cq.Workplane("XY").workplane(offset=offset_z + motor_length + flange_thickness)
        .circle(11)
        .extrude(2)
    )
    
    # Motor shaft
    shaft = (
        cq.Workplane("XY").workplane(offset=offset_z + motor_length + flange_thickness)
        .circle(shaft_dia / 2)
        .extrude(shaft_length)
    )
    
    # Back plate
    back = (
        cq.Workplane("XY").workplane(offset=offset_z)
        .rect(motor_size, motor_size)
        .extrude(-flange_thickness)
    )
    back = back.edges("|Z").fillet(corner_radius)
    
    # Combine motor parts
    motor = body.union(flange).union(boss).union(shaft).union(back)
    
    # Add connector boss on back face (circular)
    connector = (
        cq.Workplane("XY").workplane(offset=offset_z - flange_thickness)
        .circle(8)
        .extrude(-3)
    )
    motor = motor.union(connector)
    
    # Add side chamfer details (grooves on sides)
    # Simulate the groove lines on the body with small cuts
    for side_angle in [0, 90, 180, 270]:
        pass  # Skip complex grooves for stability
    
    return motor

# Create first motor (bottom)
motor1 = make_stepper_motor(offset_z=0)

# Create second motor (top, offset in Z)
gap = 5  # gap between motors  
motor2 = make_stepper_motor(offset_z=motor_length + flange_thickness * 2 + gap + 3)

# Combine both motors
combined = motor1.union(motor2)

# Add wires hanging down from bottom motor
# Wires as thin cylinders
wire_positions = [(-4, -6), (-2, -6), (0, -6), (2, -6), (4, -6), (-3, -8), (3, -8)]
wire_length = 60

wires = None
for i, (wx, wy) in enumerate(wire_positions):
    w = (
        cq.Workplane("XY")
        .workplane(offset=-flange_thickness - 3)
        .transformed(offset=cq.Vector(wx, wy, 0))
        .circle(0.4)
        .extrude(-wire_length)
    )
    if wires is None:
        wires = w
    else:
        wires = wires.union(w)

if wires is not None:
    combined = combined.union(wires)

result = combined