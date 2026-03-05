import cadquery as cq

# --- Parameters ---

# Main Mounting Plate
plate_width = 100.0
plate_height = 250.0
plate_thickness = 15.0
plate_chamfer = 2.0

# Top Motor Mount Block
motor_mount_width = 60.0
motor_mount_depth = 50.0
motor_mount_height = 15.0

# Top Motor (NEMA 17 style approximation)
motor_body_width = 42.0
motor_body_height = 40.0
motor_shaft_dia = 5.0
motor_shaft_len = 20.0
motor_boss_dia = 22.0
motor_boss_height = 2.0

# Linear Rail Blocks (The 4 corner supports)
rail_block_width = 25.0
rail_block_height = 20.0
rail_block_depth = 20.0
rail_block_x_offset = 35.0  # Distance from center to center of block
rail_block_y_offset = 80.0  # Distance from center to center of block
rail_groove_radius = 4.0

# Back Structure (Linear Rail / Actuator Body behind the plate)
back_structure_width = 80.0
back_structure_depth = 40.0
back_structure_height = 220.0

# Small Center Mechanism (Limit switch or anti-backlash nut housing)
center_block_width = 30.0
center_block_height = 30.0
center_block_depth = 15.0

# Roller Wheels (Bottom Center)
wheel_radius = 8.0
wheel_thickness = 6.0
wheel_spacing_x = 12.0
wheel_y_pos = -60.0

# --- Geometry Construction ---

# 1. Main Plate
plate = (cq.Workplane("XY")
         .box(plate_width, plate_height, plate_thickness)
         .edges("|Z").chamfer(plate_chamfer)
         )

# 2. Top Motor Mount Block (Attached to the top of the plate)
motor_mount = (cq.Workplane("XY")
               .workplane(offset=plate_thickness/2 + motor_mount_height/2)
               .center(0, plate_height/2 - motor_mount_depth/2)
               .box(motor_mount_width, motor_mount_depth, motor_mount_height)
               )

# 3. Motor (NEMA style)
motor_pos_y = plate_height/2 - motor_mount_depth/2
motor_base_z = plate_thickness/2 + motor_mount_height

motor_body = (cq.Workplane("XY")
              .workplane(offset=motor_base_z + motor_body_height/2)
              .center(0, motor_pos_y)
              .box(motor_body_width, motor_body_width, motor_body_height)
              )

motor_boss = (cq.Workplane("XY")
              .workplane(offset=motor_base_z + motor_body_height)
              .center(0, motor_pos_y)
              .circle(motor_boss_dia/2)
              .extrude(motor_boss_height)
              )

motor_shaft = (cq.Workplane("XY")
               .workplane(offset=motor_base_z + motor_body_height + motor_boss_height)
               .center(0, motor_pos_y)
               .circle(motor_shaft_dia/2)
               .extrude(motor_shaft_len)
               )

motor_coupler = (cq.Workplane("XY")
                 .workplane(offset=motor_base_z + motor_body_height + motor_boss_height + motor_shaft_len)
                 .center(0, motor_pos_y)
                 .circle(motor_shaft_dia) # Slightly larger for coupler visual
                 .extrude(5)
                 )

# 4. Linear Rail Blocks (4 corner mounts)
def create_rail_block(x_loc, y_loc):
    block = (cq.Workplane("XY")
             .workplane(offset=plate_thickness/2 + rail_block_depth/2)
             .center(x_loc, y_loc)
             .box(rail_block_width, rail_block_height, rail_block_depth)
             )
    # Add the "groove" or rail profile cutout
    cutout = (cq.Workplane("XY")
              .workplane(offset=plate_thickness/2 + rail_block_depth)
              .center(x_loc, y_loc)
              .box(rail_block_width + 2, rail_groove_radius*2, rail_block_depth/2) # Simple cutout
              )
    return block.cut(cutout)

# Generate the 4 blocks
blocks = []
for x_sign in [-1, 1]:
    for y_sign in [-1, 1]:
        blocks.append(create_rail_block(x_sign * rail_block_x_offset, y_sign * rail_block_y_offset))

# 5. Back Structure (The rail/extrusion behind the plate)
back_struct = (cq.Workplane("XY")
               .workplane(offset=-plate_thickness/2 - back_structure_depth/2)
               .box(back_structure_width, back_structure_height, back_structure_depth)
               )

# Add side grooves to back structure to simulate aluminum extrusion
side_groove = (cq.Workplane("YZ")
               .center(0, -plate_thickness/2 - back_structure_depth/2)
               .rect(back_structure_height, 5)
               .extrude(back_structure_width + 10)
               )
back_struct = back_struct.cut(side_groove)


# 6. Center Mechanism (Small block in the middle face)
center_block = (cq.Workplane("XY")
                .workplane(offset=plate_thickness/2 + center_block_depth/2)
                .center(0, -20) # Slightly offset downwards based on image
                .box(center_block_width, center_block_height, center_block_depth)
                )

# 7. Roller Wheels
def create_wheel(x_loc, y_loc):
    # Mounting standoff
    standoff = (cq.Workplane("XY")
                .workplane(offset=plate_thickness/2)
                .center(x_loc, y_loc)
                .circle(3)
                .extrude(3)
                )
    # The wheel itself
    wheel = (cq.Workplane("XY")
             .workplane(offset=plate_thickness/2 + 3)
             .center(x_loc, y_loc)
             .circle(wheel_radius)
             .extrude(wheel_thickness)
             )
    # Center hole/screw head
    screw = (cq.Workplane("XY")
             .workplane(offset=plate_thickness/2 + 3 + wheel_thickness)
             .center(x_loc, y_loc)
             .circle(2)
             .extrude(1)
             )
    return standoff.union(wheel).union(screw)

# Create 3 wheels in a triangular/offset pattern
wheels = [
    create_wheel(0, wheel_y_pos + 10),
    create_wheel(-wheel_spacing_x, wheel_y_pos - 5),
    create_wheel(wheel_spacing_x, wheel_y_pos - 5)
]

# --- Combine Geometry ---

result = plate
result = result.union(motor_mount)
result = result.union(motor_body)
result = result.union(motor_boss)
result = result.union(motor_shaft)
result = result.union(motor_coupler)
result = result.union(back_struct)
result = result.union(center_block)

for b in blocks:
    result = result.union(b)

for w in wheels:
    result = result.union(w)

# Add filleting to make it look machined/realistic
try:
    # Select edges of the main plate that aren't on the mounting faces
    result = result.edges("|Z").fillet(1.0)
except:
    pass # Fallback if fillet fails on complex geometry intersections

# Export or display
# show_object(result)