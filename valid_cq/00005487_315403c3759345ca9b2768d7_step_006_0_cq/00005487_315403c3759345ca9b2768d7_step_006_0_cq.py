import cadquery as cq

# Parameters for the Linear Actuator
rail_length = 500.0
rail_width = 60.0
rail_height = 40.0

# Carriage Block Parameters
carriage_length = 80.0
carriage_width = 58.0
carriage_height = 25.0
carriage_offset = 100.0  # Distance from motor end

# End Plate Parameters (Motor Side)
motor_plate_thickness = 15.0
motor_plate_width = rail_width
motor_plate_height = rail_height + 15.0

# End Plate Parameters (End Side)
end_plate_thickness = 12.0

# Ball Screw Parameters
screw_diameter = 12.0
screw_length = rail_length - motor_plate_thickness - end_plate_thickness

# Motor Mount Parameters (Generic NEMA 23-ish shape)
motor_body_length = 60.0
motor_body_width = 57.0
motor_shaft_dia = 6.35
motor_shaft_len = 20.0

# --- Geometry Construction ---

# 1. Base Rail (Main Extrusion)
# A simple rectangular profile with a slot for the screw/carriage
rail_profile = (
    cq.Workplane("XY")
    .rect(rail_length, rail_width)
    .extrude(rail_height)
)

# Create a central channel for the ball screw and mechanism
rail_channel = (
    cq.Workplane("XY")
    .rect(rail_length, rail_width * 0.6)
    .extrude(rail_height * 0.7)
    .translate((0, 0, rail_height * 0.3))
)

rail_base = rail_profile.cut(rail_channel)

# 2. Linear Guides (Simulated rails on top edges)
guide_rail_width = 10.0
guide_rail_height = 5.0
guide_rail_y_offset = (rail_width / 2) - (guide_rail_width / 2) - 2.0

left_guide = (
    cq.Workplane("XY")
    .rect(rail_length, guide_rail_width)
    .extrude(guide_rail_height)
    .translate((0, -guide_rail_y_offset, rail_height))
)

right_guide = (
    cq.Workplane("XY")
    .rect(rail_length, guide_rail_width)
    .extrude(guide_rail_height)
    .translate((0, guide_rail_y_offset, rail_height))
)

# 3. Ball Screw
ball_screw = (
    cq.Workplane("YZ")
    .circle(screw_diameter / 2)
    .extrude(screw_length)
    .translate((-screw_length/2, 0, rail_height * 0.6)) # Centered in channel height-wise roughly
    .rotate((0,1,0), (0,0,0), 90) # Re-orient to X-axis
)

# 4. Carriage Blocks (Two blocks as shown in image)
def create_carriage(x_pos):
    # Main block body
    blk = (
        cq.Workplane("XY")
        .rect(carriage_length, carriage_width)
        .extrude(carriage_height)
        .translate((x_pos, 0, rail_height + guide_rail_height))
    )
    
    # Cutout for the top mounting surface look
    top_cut = (
        cq.Workplane("XY")
        .rect(carriage_length * 0.8, carriage_width * 0.6)
        .extrude(5)
        .translate((x_pos, 0, rail_height + guide_rail_height + carriage_height - 5))
    )
    
    # Bolt holes
    holes = (
        cq.Workplane("XY")
        .rect(carriage_length - 15, carriage_width - 15, forConstruction=True)
        .vertices()
        .circle(2.5)
        .extrude(10)
        .translate((x_pos, 0, rail_height + guide_rail_height + carriage_height - 10))
    )
    
    return blk.cut(top_cut).cut(holes)

# Create two carriages side-by-side or slightly spaced
carriage_1 = create_carriage(rail_length/2 - carriage_offset)
carriage_2 = create_carriage(rail_length/2 - carriage_offset - carriage_length - 5)


# 5. Motor End Plate
motor_plate = (
    cq.Workplane("YZ")
    .rect(motor_plate_width, motor_plate_height)
    .extrude(motor_plate_thickness)
    .translate((rail_length/2 + motor_plate_thickness/2, 0, rail_height/2))
)

# 6. Idle End Plate
idle_plate = (
    cq.Workplane("YZ")
    .rect(motor_plate_width, motor_plate_height)
    .extrude(end_plate_thickness)
    .translate((-rail_length/2 - end_plate_thickness/2, 0, rail_height/2))
)

# 7. Motor Model
motor_x_pos = rail_length/2 + motor_plate_thickness
motor_z_pos = rail_height * 0.6 # Aligned with screw

motor_body = (
    cq.Workplane("YZ")
    .rect(motor_body_width, motor_body_width)
    .extrude(motor_body_length)
    .translate((motor_x_pos + motor_body_length/2, 0, motor_z_pos))
)

motor_shaft = (
    cq.Workplane("YZ")
    .circle(motor_shaft_dia/2)
    .extrude(motor_shaft_len + motor_body_length + 10) # Stick out back and front
    .translate((motor_x_pos + motor_body_length/2 - 5, 0, motor_z_pos))
)

# Chamfer the motor body edges for aesthetics
motor_body = motor_body.edges("|X").chamfer(2.0)


# --- Assembly ---

# Union everything together
linear_actuator = (
    rail_base
    .union(left_guide)
    .union(right_guide)
    .union(ball_screw)
    .union(carriage_1)
    .union(carriage_2)
    .union(motor_plate)
    .union(idle_plate)
    .union(motor_body)
    .union(motor_shaft)
)

# Add some mounting holes to the end plates
end_plate_holes_motor = (
    cq.Workplane("YZ")
    .rect(motor_plate_width - 10, motor_plate_height - 10, forConstruction=True)
    .vertices()
    .circle(3)
    .extrude(motor_plate_thickness * 2)
    .translate((rail_length/2, 0, rail_height/2))
)

end_plate_holes_idle = (
    cq.Workplane("YZ")
    .rect(motor_plate_width - 10, motor_plate_height - 10, forConstruction=True)
    .vertices()
    .circle(3)
    .extrude(end_plate_thickness * 2)
    .translate((-rail_length/2 - end_plate_thickness, 0, rail_height/2))
)

result = linear_actuator.cut(end_plate_holes_motor).cut(end_plate_holes_idle)

# Final result ready for export or display
if "show_object" in locals():
    show_object(result)