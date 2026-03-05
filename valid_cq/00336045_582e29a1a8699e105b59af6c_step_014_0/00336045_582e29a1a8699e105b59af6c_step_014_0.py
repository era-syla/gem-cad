import cadquery as cq

# -- Parameters --
# Base Plate Dimensions
plate_length = 100.0
plate_width = 50.0
plate_thickness = 4.0
corner_radius = 5.0

# Motor Mount Parameters (NEMA 17 style)
# Positioned on the right side of the plate
motor_center_offset = 25.0  # Distance from center of plate to center of motor hole
motor_large_hole_dia = 26.0
motor_mount_spacing = 31.0
slot_length = 9.0
slot_width = 3.5

# Mounting Grid Parameters
# Positioned on the left side of the plate
grid_rows = 2
grid_cols = 3
grid_hole_dia = 4.5
grid_spacing_x = 15.0
grid_spacing_y = 20.0
grid_start_x = -35.0  # X coordinate of the first column (relative to center)

# -- Geometry Construction --

# 1. Create Base Plate with Rounded Corners
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Cut Large Motor Hole
result = (
    result.faces(">Z")
    .workplane()
    .center(motor_center_offset, 0)
    .circle(motor_large_hole_dia / 2)
    .cutThruAll()
)

# 3. Cut Motor Mounting Slots
# Define slot positions relative to the plate center
# Slots are oriented horizontally (angle=0)
slot_positions = [
    (motor_center_offset + motor_mount_spacing/2, motor_mount_spacing/2),
    (motor_center_offset + motor_mount_spacing/2, -motor_mount_spacing/2),
    (motor_center_offset - motor_mount_spacing/2, motor_mount_spacing/2),
    (motor_center_offset - motor_mount_spacing/2, -motor_mount_spacing/2),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(slot_positions)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)

# 4. Cut Grid Holes
# Generate coordinates for the 3x2 grid
grid_points = []
for col in range(grid_cols):
    x = grid_start_x + (col * grid_spacing_x)
    for row in range(grid_rows):
        # Center the rows vertically around Y=0
        y = (row - 0.5) * 2 * (grid_spacing_y / 2)
        grid_points.append((x, y))

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(grid_points)
    .circle(grid_hole_dia / 2)
    .cutThruAll()
)