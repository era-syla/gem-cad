import cadquery as cq

# --- Parametric Dimensions ---

# Main Housing Body
housing_width = 60.0
housing_depth = 40.0
housing_height = 150.0
wall_thickness = 4.0

# Top Motor Mount Block
top_block_height = 25.0
top_block_overhang = 5.0  # How much it sticks out to the front

# Linear Rail / Guide
rail_width = 12.0
rail_depth = 8.0
rail_length = housing_height - 20.0

# Carriage / Slider
carriage_width = 30.0
carriage_height = 40.0
carriage_depth = 10.0

# Back Mounting Plate
plate_width = housing_width + 10.0
plate_height = housing_height
plate_thickness = 5.0

# Lead Screw / Motor Assembly (Separate component in image, but we'll integrate or model the main assembly)
motor_nema_size = 42.0 # Nema 17 approx
motor_height = 34.0
coupling_height = 20.0
coupling_dia = 18.0
leadscrew_dia = 8.0
leadscrew_len = 100.0

# Small detailed features (clips/mounts on front)
clip_width = 10.0
clip_height = 8.0
clip_depth = 6.0

# --- Geometry Construction ---

# 1. Main Vertical Housing
# A rectangular tower with some cutouts/features
housing = (
    cq.Workplane("XY")
    .box(housing_width, housing_depth, housing_height)
    .edges("|Z")
    .fillet(2.0) # Soften edges
)

# 2. Top Cap / Motor Mount Area
# Adding a block on top
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=housing_height/2 + top_block_height/2)
    .box(housing_width, housing_depth + top_block_overhang, top_block_height)
    .edges("|Z").fillet(2.0)
)

# 3. Linear Rail Simulation
# A groove or added material on the front face
rail = (
    cq.Workplane("XZ")
    .workplane(offset=housing_depth/2) # Front face
    .rect(rail_width, rail_length)
    .extrude(rail_depth)
)

# 4. Carriage Block (The part that moves)
# Positioned somewhere in the middle
carriage_pos_z = -20.0
carriage = (
    cq.Workplane("XZ")
    .workplane(offset=housing_depth/2 + rail_depth)
    .center(0, carriage_pos_z)
    .rect(carriage_width, carriage_height)
    .extrude(carriage_depth)
)

# Add some detailing to the carriage (mounting holes)
carriage = (
    carriage.faces(">Y")
    .workplane()
    .pushPoints([(-10, 0), (10, 0), (0, 10)])
    .hole(3.0)
)


# 5. Side Clips / Cable Managers
# Four clips seen on the front face in the image
clips = cq.Workplane("XZ").workplane(offset=housing_depth/2)

clip_positions = [
    (-housing_width/2 + 10, -40),
    (housing_width/2 - 10, -40),
    (-housing_width/2 + 10, 20),
    (housing_width/2 - 10, 20)
]

clip_solid = (
    cq.Workplane("XY")
    .rect(clip_width, clip_depth)
    .extrude(clip_height)
    .faces(">Z").workplane()
    .rect(clip_width - 2, clip_depth) # Cut slot
    .cutBlind(-clip_height/2)
)

# Combine clips onto the main body
for pos in clip_positions:
    located_clip = clip_solid.translate((pos[0], housing_depth/2 + clip_depth/2, pos[1]))
    housing = housing.union(located_clip)


# 6. Central Circular Feature (Lead Screw Nut Housing)
nut_housing = (
    cq.Workplane("XZ")
    .workplane(offset=housing_depth/2)
    .center(0, -10)
    .circle(12.0)
    .extrude(15.0)
)
# Add nut detail
nut_housing = (
    nut_housing.faces(">Y").workplane()
    .polygon(6, 10.0)
    .cutBlind(-5.0)
)


# 7. Motor / Lead Screw Assembly (The detached part in the image)
# We will model this separately and translate it to the side as shown
motor_x_offset = 80.0

# Motor Body (NEMA 17 style)
motor = (
    cq.Workplane("XY")
    .rect(motor_nema_size, motor_nema_size)
    .extrude(motor_height)
    .edges("|Z").fillet(3.0)
)

# Motor Mounting Plate
motor_plate = (
    cq.Workplane("XY")
    .workplane(offset=-5)
    .rect(motor_nema_size + 10, motor_nema_size + 10)
    .extrude(5.0)
)
# Mounting Holes on plate
motor_plate = (
    motor_plate.faces(">Z").workplane()
    .rect(motor_nema_size, motor_nema_size, forConstruction=True)
    .vertices()
    .hole(3.5)
)

# Shaft/Coupling
coupling = (
    cq.Workplane("XY")
    .workplane(offset=-5 - coupling_height)
    .circle(coupling_dia/2)
    .extrude(coupling_height)
)

# Lead Screw
screw = (
    cq.Workplane("XY")
    .workplane(offset=-5 - coupling_height - leadscrew_len)
    .circle(leadscrew_dia/2)
    .extrude(leadscrew_len)
)

# Combine Motor Assembly
motor_assembly = motor.union(motor_plate).union(coupling).union(screw)
# Position it
motor_assembly = motor_assembly.rotate((1,0,0), (0,0,0), 90).translate((motor_x_offset, 0, 50))


# 8. Combine Main Assembly
main_assembly = (
    housing
    .union(top_cap)
    .union(rail)
    .union(carriage)
    .union(nut_housing)
)

# Add "Backplate" visual (darker part in image) behind housing
backplate = (
    cq.Workplane("XY")
    .workplane(offset=0) # Centered on Z
    .box(plate_width, plate_thickness, plate_height)
    .translate((0, -housing_depth/2 - plate_thickness/2, 0))
)
main_assembly = main_assembly.union(backplate)

# 9. Lower wheels/rollers simulation (seen near bottom)
wheel_radius = 6.0
wheel_thick = 4.0
wheels = cq.Workplane("XY")
for i in range(3):
    w = (
        cq.Workplane("YZ")
        .circle(wheel_radius)
        .extrude(wheel_thick)
        .translate((0, housing_depth/2 + 5, -50 - (i*15)))
    )
    main_assembly = main_assembly.union(w)


# Final Union of the two main separated parts for the 'result'
result = main_assembly.union(motor_assembly)