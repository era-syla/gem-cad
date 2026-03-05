import cadquery as cq

# --- Parameters ---

# Cylindrical Hopper/Mixer Parameters
hopper_dia = 50.0
hopper_height = 40.0
hopper_wall_thk = 2.0
base_plate_size = 80.0
base_plate_thk = 2.0

# Mixer Arm/Mechanism Parameters
motor_box_length = 30.0
motor_box_width = 15.0
motor_box_height = 10.0
arm_length = 40.0
arm_width = 5.0
arm_height = 3.0
vertical_support_height = 50.0
vertical_support_width = 5.0

# Large Control Cabinet Parameters
cabinet_width = 30.0
cabinet_depth = 30.0
cabinet_height = 60.0

# Platform/Floor Parameters
platform_thk = 1.0

# Layout coordinates (approximate based on image)
positions = [
    (-60, 60, 0),   # Top Left
    (60, 60, 0),    # Top Right
    (-60, -60, 0),  # Bottom Left
    (100, -60, 0)   # Bottom Right (Standalone unit)
]

# --- Helper Functions ---

def create_hopper_unit():
    """Creates a single mixing/hopper station."""
    
    # 1. Base Plate
    base = cq.Workplane("XY").box(base_plate_size, base_plate_size, base_plate_thk)
    
    # 2. Cylindrical Hopper
    # Create a cylinder and shell it (or subtract inner cylinder)
    hopper_outer = cq.Workplane("XY").workplane(offset=base_plate_thk/2).circle(hopper_dia/2).extrude(hopper_height)
    hopper_inner = cq.Workplane("XY").workplane(offset=base_plate_thk/2 + 2).circle((hopper_dia/2) - hopper_wall_thk).extrude(hopper_height)
    hopper = hopper_outer.cut(hopper_inner)
    
    # 3. Vertical Support Column
    support = (cq.Workplane("XY")
               .workplane(offset=base_plate_thk/2)
               .center(-hopper_dia/2 - 5, 0)
               .box(vertical_support_width, vertical_support_width, vertical_support_height, centered=(True, True, False))
              )

    # 4. Motor/Gearbox Housing on top
    motor_housing = (cq.Workplane("XY")
                     .workplane(offset=vertical_support_height)
                     .center(-hopper_dia/2 - 5 + motor_box_length/2 - 5, 0) # Offset to align
                     .box(motor_box_length, motor_box_width, motor_box_height)
                    )
    
    # Fillet the motor housing for style (rounded back)
    motor_housing = motor_housing.edges("|Z").fillet(motor_box_width/2.1)

    # 5. Mixer Arm sticking out into the hopper
    arm = (cq.Workplane("XY")
           .workplane(offset=vertical_support_height - 5)
           .center(-hopper_dia/2, 0)
           .box(arm_length, arm_width, arm_height, centered=(False, True, True))
          )

    # Combine parts
    unit = base.union(hopper).union(support).union(motor_housing).union(arm)
    
    # Add triangular braces at base of support
    brace = (cq.Workplane("YZ")
             .workplane(offset=-hopper_dia/2 - 5 - vertical_support_width/2)
             .lineTo(15, 0).lineTo(0, 30).close()
             .extrude(2)
            )
    # Move brace to correct Z height
    brace = brace.translate((0, 0, base_plate_thk/2))
    
    unit = unit.union(brace)

    return unit

def create_cabinet_block():
    """Creates the large electrical/control cabinets."""
    # Main tall cabinet
    cab1 = cq.Workplane("XY").box(cabinet_width, cabinet_depth, cabinet_height, centered=(True, True, False))
    
    # Smaller side cabinet
    cab2 = (cq.Workplane("XY")
            .center(cabinet_width/2 + cabinet_depth/2, 0)
            .box(cabinet_depth, cabinet_depth, cabinet_height * 0.7, centered=(True, True, False)))
            
    return cab1.union(cab2)

def create_conveyor_segment():
    """Creates a simple conveyor belt representation."""
    belt = cq.Workplane("XY").box(60, 15, 5, centered=(True, True, False))
    # Legs
    leg1 = cq.Workplane("XY").center(-25, 0).box(2, 10, 20, centered=(True, True, False)).translate((0,0,-15))
    leg2 = cq.Workplane("XY").center(25, 0).box(2, 10, 20, centered=(True, True, False)).translate((0,0,-15))
    return belt.union(leg1).union(leg2)

# --- Assembly Construction ---

# 1. Create the individual instances
unit1 = create_hopper_unit().translate(positions[0])
unit2 = create_hopper_unit().rotate((0,0,1), (0,0,0), 180).translate(positions[1]) # Rotated for variety
unit3 = create_hopper_unit().translate(positions[2])
unit4 = create_hopper_unit().translate(positions[3])

# 2. Central Equipment (Cabinets)
# Located roughly between the first three units
central_cabinets = create_cabinet_block().translate((0, 0, 0))

# 3. Connecting Platform/Floor
# A complex polygon shape or just a union of boxes to simulate the floor mat
floor_p1 = cq.Workplane("XY").center(-60, 60).box(120, 100, platform_thk)
floor_p2 = cq.Workplane("XY").center(0, 0).box(100, 100, platform_thk)
floor_p3 = cq.Workplane("XY").center(-60, -60).box(100, 100, platform_thk)

# Wall panel behind the first unit
wall = (cq.Workplane("XZ")
        .workplane(offset=-110) # Position in Y
        .center(-60, 30)
        .box(150, 60, 2)
       )

# 4. Conveyor connecting central area to isolated unit
conveyor = create_conveyor_segment().translate((60, -40, 15)).rotate((0,0,1),(0,0,0), -30)

# 5. Additional small boxes/details seen in image
small_box = cq.Workplane("XY").box(15, 30, 10).translate((-20, -20, 0))


# --- Combine All ---

result = (
    unit1
    .union(unit2)
    .union(unit3)
    .union(unit4)
    .union(central_cabinets)
    .union(floor_p1)
    .union(floor_p2)
    .union(floor_p3)
    .union(wall)
    .union(conveyor)
    .union(small_box)
)