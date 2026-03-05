import cadquery as cq

# Parametric dimensions
disk_radius = 40.0
disk_thickness = 30.0
arm_length = 60.0
arm_width = 15.0
arm_height = 15.0
hole_diameter = 4.0
bottom_mount_width = 20.0
bottom_mount_depth = 25.0
bottom_mount_thickness = 5.0
vertical_stem_height = 15.0
vertical_stem_radius = 6.0

# 1. Create the main disk
# We center it at origin to make subsequent operations easier
main_disk = cq.Workplane("XY").circle(disk_radius).extrude(disk_thickness)

# 2. Create the rectangular arm extending from the back
# We'll position it centered on the Y-axis, extending in -X
arm = (
    cq.Workplane("YZ")
    .workplane(offset=-disk_radius)  # Start at the edge of the disk roughly (or center)
    .center(0, disk_thickness / 2.0) # Center vertically relative to disk
    .rect(arm_height, arm_width)     # Cross-section
    .extrude(-arm_length)            # Extrude outwards
)

# 3. Add holes to the arm
# One near the tip, one closer to the body
hole_dist_from_tip = 10.0
hole_spacing = 30.0

arm_with_holes = (
    arm.faces(">X").workplane()
    .center(0, 0) # Ensure we are centered on the arm face
    .pushPoints([(-hole_dist_from_tip, 0), (-hole_dist_from_tip - hole_spacing, 0)])
    .hole(hole_diameter)
)

# 4. Create the bottom mounting structure
# It looks like an 'L' bracket or a pivot mount attached to the bottom of the disk.

# Vertical part connecting to the disk
bottom_stem = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness/2) # Mid-plane of disk thickness
    .center(0, -disk_radius)            # Bottom of the disk
    .rect(bottom_mount_width, bottom_mount_width) # Square profile 
    .extrude(-25) # Extrude downwards
)

# Create the L-shape foot
# We need a horizontal plate at the bottom of the stem
foot_plate = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness/2 - 25) # At the bottom of the stem extrusion
    .center(0, -disk_radius + bottom_mount_depth/2 - bottom_mount_width/2) # Shift out slightly
    .rect(bottom_mount_width, bottom_mount_depth + 10) # Rectangular footprint
    .extrude(-bottom_mount_thickness) # Thickness downwards
)

# Add the cylindrical pivot/pin feature on the foot
pivot_pin = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness/2 - 25) # Top surface of the foot
    .center(0, -disk_radius + 10) # Position slightly outward from the stem
    .circle(vertical_stem_radius)
    .extrude(15) # Height of the pin
)

# Combine all parts
result = (
    main_disk
    .union(arm_with_holes)
    .union(bottom_stem)
    .union(foot_plate)
    .union(pivot_pin)
)

# Refine the connection between disk and bottom stem (Fillet)
# Finding the edges at the intersection is tricky without tags, 
# so we might skip complex fillets to ensure robustness, 
# or apply a general fillet to specific vertical edges of the bottom stem.
try:
    result = result.edges("|Z").filterByPosition(lambda p: p.y < -disk_radius + 10 and p.z < 0).fillet(2.0)
except:
    pass # valid geometry is prioritized over fillets if selection fails