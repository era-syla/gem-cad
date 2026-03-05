import cadquery as cq

# --- Parametric Dimensions ---

# Main Trough (U-Channel) parameters
trough_width = 100.0
trough_height = 80.0
trough_length = 300.0
trough_thickness = 5.0
flange_width = 15.0

# Support Upright parameters
upright_width = 60.0
upright_height = 120.0  # Height above the trough
upright_thickness = 5.0

# Motor and Gearbox parameters
motor_diameter = 80.0
motor_length = 140.0
gearbox_size = 60.0
gearbox_length = 80.0
motor_mount_plate_size = 90.0
motor_mount_thickness = 8.0

# Pulley/Roller parameters
pulley_diameter = 50.0
pulley_width = 25.0
shaft_diameter = 12.0
shaft_protrusion = 10.0

# --- Geometry Construction ---

# 1. Trough (U-Channel with top flanges)
# We draw the profile and extrude
pts = [
    (0, 0),
    (trough_width + 2*flange_width, 0),
    (trough_width + 2*flange_width, -trough_thickness), # Right Flange thickness
    (trough_width + flange_width + trough_thickness, -trough_thickness),
    (trough_width + flange_width + trough_thickness, -trough_height),
    (flange_width - trough_thickness, -trough_height), # Bottom
    (flange_width - trough_thickness, -trough_thickness),
    (0, -trough_thickness), # Left Flange thickness
    (0, 0)
]

# Inner cutout points to make it hollow
inner_pts = [
    (flange_width, -trough_thickness),
    (trough_width + flange_width, -trough_thickness),
    (trough_width + flange_width, -trough_height + trough_thickness),
    (flange_width, -trough_height + trough_thickness),
    (flange_width, -trough_thickness)
]

# Constructing the main u-channel profile
outer_profile = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (flange_width, 0),
        (flange_width, -trough_height),
        (flange_width + trough_width, -trough_height),
        (flange_width + trough_width, 0),
        (flange_width + trough_width + flange_width, 0),
        (flange_width + trough_width + flange_width, -trough_thickness),
        (flange_width + trough_width + trough_thickness, -trough_thickness),
        (flange_width + trough_width + trough_thickness, -trough_height - trough_thickness),
        (flange_width - trough_thickness, -trough_height - trough_thickness),
        (flange_width - trough_thickness, -trough_thickness),
        (0, -trough_thickness),
        (0, 0)
    ])
    .close()
    .extrude(trough_length)
)

# 2. Vertical Support Upright
# Attached to one side of the trough
upright = (
    cq.Workplane("XY")
    .workplane(offset=-trough_length/2 + 30) # Position near the back
    .moveTo(flange_width - trough_thickness/2, 0) # Align with left wall
    .rect(trough_thickness, upright_width) # Cross section of vertical plate
    .extrude(upright_height + trough_height) # Extrude upwards
)

# 3. Motor Mounting Plate
# On top of the upright
plate_z = upright_height
mount_plate = (
    cq.Workplane("XY")
    .workplane(offset=plate_z)
    .center(flange_width - trough_thickness/2 + gearbox_size/2, -trough_length/2 + 30)
    .rect(motor_mount_plate_size, motor_mount_plate_size + 20)
    .extrude(motor_mount_thickness)
)

# Add bolts to mounting plate (simplified as cylinders)
bolts = (
    cq.Workplane("XY")
    .workplane(offset=plate_z)
    .center(flange_width - trough_thickness/2 + gearbox_size/2, -trough_length/2 + 30)
    .rect(motor_mount_plate_size - 15, motor_mount_plate_size + 5, forConstruction=True)
    .vertices()
    .circle(3)
    .extrude(motor_mount_thickness + 5)
)
mount_plate = mount_plate.union(bolts)

# 4. Gearbox
# Sitting on the plate
gearbox_center_z = plate_z + motor_mount_thickness + gearbox_size/2
gearbox = (
    cq.Workplane("YZ")
    .workplane(offset=flange_width - trough_thickness/2 )
    .center(-trough_length/2 + 30, gearbox_center_z)
    .rect(gearbox_length, gearbox_size)
    .extrude(gearbox_size)
)

# 5. Motor
# Cylinder attached to the gearbox
motor = (
    cq.Workplane("YZ")
    .workplane(offset=flange_width - trough_thickness/2 + gearbox_size)
    .center(-trough_length/2 + 30, gearbox_center_z)
    .circle(motor_diameter/2)
    .extrude(motor_length)
)

# 6. Top Pulley (Driven)
# Stick out from gearbox side
top_pulley_x_center = flange_width - trough_thickness/2 
top_pulley = (
    cq.Workplane("YZ")
    .workplane(offset=top_pulley_x_center)
    .center(-trough_length/2 + 30 - gearbox_length/2 - 10, gearbox_center_z) # Offset slightly
    .circle(pulley_diameter/2)
    .extrude(-pulley_width)
)

# Top Shaft
top_shaft = (
    cq.Workplane("YZ")
    .workplane(offset=top_pulley_x_center + 5)
    .center(-trough_length/2 + 30 - gearbox_length/2 - 10, gearbox_center_z)
    .circle(shaft_diameter/2)
    .extrude(-pulley_width - shaft_protrusion)
)

# 7. Bottom Pulley (Idler)
# Mounted on the side wall of the trough
bottom_pulley_z = -trough_height/2
bottom_pulley_y = -trough_length/2 + 30
bottom_pulley = (
    cq.Workplane("YZ")
    .workplane(offset=flange_width - trough_thickness) # Flush with outer wall
    .center(bottom_pulley_y, bottom_pulley_z)
    .circle(pulley_diameter/2)
    .extrude(-pulley_width)
)

# Bottom Shaft
bottom_shaft = (
    cq.Workplane("YZ")
    .workplane(offset=flange_width - trough_thickness + 5)
    .center(bottom_pulley_y, bottom_pulley_z)
    .circle(shaft_diameter/2)
    .extrude(-pulley_width - shaft_protrusion)
)

# Internal Shaft across the trough (visible in image)
internal_shaft = (
    cq.Workplane("YZ")
    .workplane(offset=flange_width) # Inner left wall
    .center(bottom_pulley_y, bottom_pulley_z)
    .circle(shaft_diameter/2)
    .extrude(trough_width) # Span across
)

# 8. Brace/Stiffener on the upright
# Small horizontal piece connecting upright to trough
brace = (
    cq.Workplane("XY")
    .workplane(offset=0) # Top of trough level
    .center(flange_width - trough_thickness/2, -trough_length/2 + 30)
    .rect(trough_thickness, upright_width + 40) # Wider than upright
    .extrude(5) # Thin plate
)

# Combine all parts
result = (
    outer_profile
    .union(upright)
    .union(mount_plate)
    .union(gearbox)
    .union(motor)
    .union(top_pulley)
    .union(top_shaft)
    .union(bottom_pulley)
    .union(bottom_shaft)
    .union(internal_shaft)
    .union(brace)
)

# Center the result roughly for better viewing
result = result.translate((-trough_width/2, trough_length/2, trough_height/2))