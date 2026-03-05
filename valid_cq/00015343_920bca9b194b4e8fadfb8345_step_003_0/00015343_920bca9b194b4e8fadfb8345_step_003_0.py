import cadquery as cq

# --- Parametric Dimensions ---
plate_width = 30.0
plate_thickness = 5.0
plate_straight_len = 35.0
plate_radius = plate_width / 2.0

block_len = 35.0  # Length of the block section (matches straight part of plate)
block_height = 25.0 # Height of block below the plate
block_floor_thick = 5.0 # Thickness of the floor of the tunnel
block_wall_thick = 6.0  # Thickness of the side walls of the block

# Derived Cutout Dimensions
cutout_width = block_len - 2 * block_wall_thick
cutout_radius = cutout_width / 2.0
# Calculate straight height of cutout based on available height and desired top web thickness
top_web_thick = 5.0 
cutout_straight_height = block_height - block_floor_thick - top_web_thick - cutout_radius

# Ensure geometry validity
if cutout_straight_height < 0:
    cutout_straight_height = 0

# --- Modeling ---

# 1. Top Plate
# Create the plate with a straight section and a rounded end.
# Origin is placed at the center of the square back face.
# X-axis runs along the length, Y-axis along the width.
plate = (
    cq.Workplane("XY")
    .moveTo(0, -plate_width/2.0)
    .lineTo(plate_straight_len, -plate_width/2.0)
    .threePointArc(
        (plate_straight_len + plate_radius, 0),          # Midpoint of arc (tip)
        (plate_straight_len, plate_width/2.0)            # End point of arc
    )
    .lineTo(0, plate_width/2.0)
    .close()
    .extrude(plate_thickness)
)

# 2. Bottom Block
# Create the rectangular block underneath the straight section of the plate.
# Extrudes downwards (Negative Z).
block = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(0, -plate_width/2.0)
    .lineTo(block_len, -plate_width/2.0)
    .lineTo(block_len, plate_width/2.0)
    .lineTo(0, plate_width/2.0)
    .close()
    .extrude(-block_height)
)

# Join plate and block
result = plate.union(block)

# 3. Transverse Cutout (Tunnel)
# Cut a "tombstone" shape (rectangle + semi-circle) through the block along the Y axis.
# Calculations for sketch positioning on XZ plane.
cutout_x_center = block_len / 2.0
cutout_z_base = -block_height + block_floor_thick

result = (
    result
    .faces(">Y") # Select the side face of the block
    .workplane(centerOption="ProjectedOrigin") # Project global origin to align coordinates
    # Draw the profile
    .moveTo(cutout_x_center + cutout_width/2.0, cutout_z_base)
    .lineTo(cutout_x_center + cutout_width/2.0, cutout_z_base + cutout_straight_height)
    .threePointArc(
        (cutout_x_center, cutout_z_base + cutout_straight_height + cutout_radius), # Apex of arch
        (cutout_x_center - cutout_width/2.0, cutout_z_base + cutout_straight_height) # End of arch
    )
    .lineTo(cutout_x_center - cutout_width/2.0, cutout_z_base)
    .close()
    .cutThruAll()
)