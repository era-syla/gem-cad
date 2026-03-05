import cadquery as cq

# --- Parameters ---
# Main Rail/Base Dimensions
base_length = 300.0
base_width = 40.0
base_height = 20.0
rail_width = 15.0
rail_height = 10.0
groove_depth = 4.0
groove_width = 3.0

# Carriage Dimensions
carriage_length = 60.0
carriage_width = 50.0
carriage_height = 12.0
carriage_offset = -30.0 # Position along the rail

# Motor Mount / End Block Dimensions
end_plate_thickness = 10.0
motor_mount_size = 42.0 # NEMA 17 style
motor_mount_offset = 20.0

# Motor Dimensions (Simplified representation)
motor_body_diam = 35.0
motor_body_length = 30.0
motor_shaft_diam = 5.0
motor_shaft_length = 15.0
coupling_diam = 18.0
coupling_length = 20.0

# --- Geometry Construction ---

# 1. Base Extrusion Profile
# Create a rectangular base with a T-slot like structure on top for the rail
base_profile = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_length)
    .rotate((0, 0, 0), (0, 1, 0), 90) # Orient along X axis
    .translate((base_length/2, 0, -base_height/2))
)

# 2. Linear Rail
# A simplified rail profile on top of the base
rail = (
    cq.Workplane("XY")
    .rect(rail_width, rail_height)
    .extrude(base_length)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((base_length/2, 0, rail_height/2))
)

# Grooves on the rail (visual detail)
rail_groove_l = (
    cq.Workplane("YZ")
    .rect(groove_width, groove_depth)
    .extrude(base_length)
    .translate((base_length/2, -rail_width/2, rail_height/2))
)
rail_groove_r = (
    cq.Workplane("YZ")
    .rect(groove_width, groove_depth)
    .extrude(base_length)
    .translate((base_length/2, rail_width/2, rail_height/2))
)

# Combine base and rail, cut grooves
structure = base_profile.union(rail).cut(rail_groove_l).cut(rail_groove_r)

# 3. Carriage (Slider)
# Block riding on the rail
carriage_body = (
    cq.Workplane("XY")
    .rect(carriage_length, carriage_width)
    .extrude(carriage_height)
    .translate((carriage_offset + base_length/2, 0, rail_height + carriage_height/2))
)

# Cutout for the rail underneath the carriage
rail_cutout = (
    cq.Workplane("XY")
    .rect(carriage_length, rail_width + 1.0) # slightly wider for clearance
    .extrude(rail_height)
    .translate((carriage_offset + base_length/2, 0, rail_height/2))
)

carriage = carriage_body.cut(rail_cutout)

# Add mounting holes to carriage
carriage = (
    carriage.faces(">Z")
    .workplane()
    .rect(carriage_length - 10, carriage_width - 10, forConstruction=True)
    .vertices()
    .hole(3.5)
)

# 4. End Plate (Motor Mount)
end_plate = (
    cq.Workplane("YZ")
    .rect(base_width, base_height + rail_height + 10) # Covers end
    .extrude(end_plate_thickness)
    .translate((-end_plate_thickness/2, 0, (rail_height - 10)/2))
)

# Motor mounting flange (NEMA style)
motor_flange = (
    cq.Workplane("YZ")
    .rect(motor_mount_size, motor_mount_size)
    .extrude(5.0)
    .translate((-end_plate_thickness - 2.5, 0, 5.0))
)

# 5. Motor and Coupling (Representation)
# The large cylinder object floating in the reference image looks like a motor or sensor
# positioned strangely, or perhaps it's a separate component. 
# However, typical linear actuators have a motor at the end.
# Based on the image, there is a distinct cylindrical object floating above/near the rail end.
# Let's model the object shown in the image: A large cylinder (head) and a smaller shaft.

floating_obj_head_diam = 40.0
floating_obj_head_len = 20.0
floating_obj_shaft_diam = 20.0
floating_obj_shaft_len = 60.0

floating_object = (
    cq.Workplane("YZ")
    .circle(floating_obj_head_diam/2)
    .extrude(floating_obj_head_len)
    .translate((base_length - 30, 0, 50)) # Position roughly as in image
)

floating_object_shaft = (
    cq.Workplane("YZ")
    .circle(floating_obj_shaft_diam/2)
    .extrude(floating_obj_shaft_len)
    .translate((base_length - 30 + floating_obj_head_len/2 + floating_obj_shaft_len/2, 0, 50))
)
floating_assembly = floating_object.union(floating_object_shaft)

# Center hole in floating object
floating_assembly = floating_assembly.faces("<X").workplane().circle(5).cutBlind(-floating_obj_head_len)


# 6. Motor at the drive end (End Plate side)
# The image shows a square block at the end, let's detail that.
drive_end_block = (
    cq.Workplane("YZ")
    .rect(45, 45)
    .extrude(15)
    .translate((-15/2, 0, 5))
)

drive_shaft_hole = (
    drive_end_block.faces("<X").workplane()
    .circle(15)
    .cutBlind(-10) # Counterbore
    .faces("<X").workplane()
    .circle(5)
    .cutBlind(-20) # Through hole
)


# Assemble everything
result = (
    structure
    .union(carriage)
    .union(drive_shaft_hole)
    .union(floating_assembly)
)

# Add some details to the main rail extrusion to make it look realistic
side_groove = (
    cq.Workplane("XZ")
    .rect(base_length, 4.0)
    .extrude(base_width + 2.0) # Cut through
    .translate((base_length/2, -5, 0)) # Vertical position
)

result = result.cut(side_groove)

# Add bolting holes on the end block
result = (
    result.faces("<X").workplane()
    .rect(32, 32, forConstruction=True)
    .vertices()
    .hole(3.5, depth=10)
)