import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions (estimated from proportions)
plate_length = 80.0
plate_width = 50.0
plate_thickness = 5.0
corner_radius = 5.0

# Motor Mount Area (Right side)
large_hole_diameter = 22.0  # Likely a NEMA 17 style center pilot
motor_mount_spacing = 31.0  # NEMA 17 standard spacing
motor_mount_hole_dia = 3.0  # M3 clearance

# Additional Mounting Holes (Left side)
# Two pairs of larger holes
left_hole_dia = 5.0 # Looks like M5 clearance
left_hole_x_spacing = 20.0
left_hole_y_spacing = 30.0

# Position offsets
# The motor mount is centered on one half, the other holes on the other half
# Let's shift the large hole slightly to the right of the global center
motor_center_offset = 20.0 
left_holes_center_offset = -20.0

# --- Geometry Construction ---

# 1. Base Plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Motor Mount Features (Large hole + 4 surrounding holes)
# Large Center Hole
result = (
    result.faces(">Z")
    .workplane()
    .center(motor_center_offset, 0)
    .hole(large_hole_diameter)
)

# 4 Surrounding Motor Mount Holes
# Using rect to place them in a square pattern centered on the offset
result = (
    result.faces(">Z")
    .workplane()
    .center(motor_center_offset, 0)
    .rect(motor_mount_spacing, motor_mount_spacing, forConstruction=True)
    .vertices()
    .hole(motor_mount_hole_dia)
)

# 3. Additional Mounting Holes (Left side)
# Based on the image, there are 4 holes on the left side
# arranged in a rectangular pattern.

result = (
    result.faces(">Z")
    .workplane()
    .center(left_holes_center_offset, 0)
    .rect(left_hole_x_spacing, left_hole_y_spacing, forConstruction=True)
    .vertices()
    .hole(left_hole_dia)
)