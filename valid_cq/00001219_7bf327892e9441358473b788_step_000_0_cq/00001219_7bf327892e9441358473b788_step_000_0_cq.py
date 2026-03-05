import cadquery as cq

# --- Parameters ---
# Central base plate
plate_length = 50.0
plate_width = 30.0
plate_thickness = 5.0
plate_fillet = 5.0

# Central vertical cylinder
center_cyl_radius = 8.0
center_cyl_height = 40.0

# Inner extension of central cylinder (slightly wider base)
base_cyl_radius = 12.0
base_cyl_height = 25.0

# Spiral Arms
arm_radius = 5.0
arm_length = 30.0
num_arms = 12
spiral_radius = 25.0  # Distance from center to arm base
vertical_pitch = 30.0  # Height difference for one full revolution
angle_step = 360.0 / num_arms

# --- Construction ---

# 1. Create the base plate
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(plate_fillet)
)

# 2. Create the central hub structure
# The wider base cylinder
hub_base = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .circle(base_cyl_radius)
    .extrude(base_cyl_height)
)

# The taller, narrower central cylinder
hub_top = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .circle(center_cyl_radius)
    .extrude(center_cyl_height)
)

# Combine central parts
center_assembly = base_plate.union(hub_base).union(hub_top)

# 3. Create the spiral of cylinders
arms = cq.Workplane("XY")

for i in range(num_arms):
    angle = i * angle_step
    # Calculate height offset for spiral effect
    # The image shows them going downwards and upwards, let's center the spiral vertically around the plate
    # Or start from the plate and go down. Based on image, it looks like a helix.
    # Let's assume a helix pattern.
    
    # Calculate z-position based on angle (helix)
    z_pos = -(vertical_pitch / 360.0) * angle + 10 # Start slightly high and go down
    
    # Create a single arm
    # Rotate position vector
    x_pos = spiral_radius 
    y_pos = 0
    
    # The cylinder needs to point outwards radially
    arm = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(0, 0) # Start at origin to rotate frame
        .transformed(rotate=(0, 0, angle)) # Rotate to the correct angle around Z
        .center(spiral_radius, 0) # Move out to the spiral radius
        .transformed(rotate=(0, 90, 0)) # Rotate so cylinder points outwards (X-axis of local plane)
        .circle(arm_radius)
        .extrude(arm_length)
    )
    
    # Alternatively, create cylinder at origin aligned X, move, then rotate Z
    # Let's try a simpler approach for the arm position logic to ensure radial alignment
    arm_geo = (
        cq.Workplane("YZ") # Create cylinder along X axis
        .circle(arm_radius)
        .extrude(arm_length)
        .translate((spiral_radius, 0, z_pos)) # Move out to radius and correct height
        .rotate((0,0,0), (0,0,1), angle) # Rotate around Z axis to final position
    )
    
    if i == 0:
        arms = arm_geo
    else:
        arms = arms.union(arm_geo)

# Combine everything
result = center_assembly.union(arms)