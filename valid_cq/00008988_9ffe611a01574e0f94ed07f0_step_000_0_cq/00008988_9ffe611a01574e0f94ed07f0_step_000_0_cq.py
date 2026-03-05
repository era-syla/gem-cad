import cadquery as cq

# --- Parametric Dimensions ---

# Main Cylinder
cyl_diameter = 60.0
cyl_length = 80.0
wall_thickness = 4.0

# Fork/Mounting Arms (Left side of image)
fork_arm_length = 80.0
fork_arm_width = 12.0
fork_arm_thickness = 10.0
fork_gap = 30.0  # Distance between the two arms
fork_base_plate_width = 80.0 # Width of the plate connecting arms to cylinder
fork_base_plate_height = 20.0
fork_base_plate_thickness = 10.0

# Rear "H" or Cross bracket (Right side of image)
rear_plate_width = 80.0
rear_plate_height = 20.0
rear_plate_thickness = 10.0
vertical_bar_width = 15.0 # The vertical connection in the middle of the cylinder end

# Hole parameters
small_hole_dia = 3.5

# --- Geometry Construction ---

# 1. Main Cylindrical Body
# It looks like a hollow tube
main_body = (
    cq.Workplane("XY")
    .circle(cyl_diameter / 2.0)
    .circle((cyl_diameter / 2.0) - wall_thickness)
    .extrude(cyl_length)
)

# 2. The "Fork" Assembly (Front/Left)
# This consists of a base plate tangent to the cylinder and two long arms extending out.

# Base plate for the fork
fork_base = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at the beginning of the cylinder
    .transformed(rotate=(0, 0, 90)) # Orient correctly
    .center(0, (cyl_diameter / 2.0) + (fork_base_plate_thickness / 2.0) - 2.0) # Position slightly embedded or tangent
    .box(fork_base_plate_width, fork_base_plate_thickness, fork_base_plate_height)
)

# Fork Arms
# Arm 1
arm1 = (
    cq.Workplane("XY")
    .workplane(offset=-fork_arm_length)
    .transformed(rotate=(0, 0, 90))
    .center((fork_gap/2.0) + (fork_arm_width/2.0), (cyl_diameter / 2.0) + (fork_base_plate_thickness / 2.0) - 2.0)
    .box(fork_arm_width, fork_arm_thickness, fork_arm_length)
)

# Arm 2
arm2 = (
    cq.Workplane("XY")
    .workplane(offset=-fork_arm_length)
    .transformed(rotate=(0, 0, 90))
    .center(-((fork_gap/2.0) + (fork_arm_width/2.0)), (cyl_diameter / 2.0) + (fork_base_plate_thickness / 2.0) - 2.0)
    .box(fork_arm_width, fork_arm_thickness, fork_arm_length)
)

# Holes in the fork arms (near the ends)
hole_loc_from_end = 10.0
arm1 = arm1.faces(">Z").workplane().center(0, -hole_loc_from_end).hole(small_hole_dia)
arm2 = arm2.faces(">Z").workplane().center(0, -hole_loc_from_end).hole(small_hole_dia)

# Holes in the fork base plate (ends)
fork_base = fork_base.faces(">Y").workplane().pushPoints([
    ((fork_base_plate_width/2.0) - 6.0, 0),
    (-(fork_base_plate_width/2.0) + 6.0, 0)
]).hole(small_hole_dia)


# 3. The Rear Bracket (Back/Right)
# This looks like two horizontal bars connected by a vertical bar that goes through the cylinder diameter.

# Top horizontal bar
rear_top_bar = (
    cq.Workplane("XY")
    .workplane(offset=cyl_length - rear_plate_height)
    .transformed(rotate=(0, 0, 90))
    .center(0, (cyl_diameter / 2.0) + (rear_plate_thickness / 2.0) - 2.0)
    .box(rear_plate_width, rear_plate_thickness, rear_plate_height)
)

# Bottom horizontal bar
rear_bottom_bar = (
    cq.Workplane("XY")
    .workplane(offset=cyl_length - rear_plate_height)
    .transformed(rotate=(0, 0, 90))
    .center(0, -(cyl_diameter / 2.0) - (rear_plate_thickness / 2.0) + 2.0)
    .box(rear_plate_width, rear_plate_thickness, rear_plate_height)
)

# Vertical connecting bar (inside cylinder end)
vertical_connector = (
    cq.Workplane("XY")
    .workplane(offset=cyl_length - rear_plate_height)
    .transformed(rotate=(0, 0, 90))
    .box(vertical_bar_width, cyl_diameter + 10.0, rear_plate_height) # Slightly oversized height to merge well
)

# Holes in the rear bars
rear_top_bar = rear_top_bar.faces(">Y").workplane().pushPoints([
    ((rear_plate_width/2.0) - 6.0, 0),
    (-(rear_plate_width/2.0) + 6.0, 0)
]).hole(small_hole_dia)

rear_bottom_bar = rear_bottom_bar.faces("<Y").workplane().pushPoints([
    ((rear_plate_width/2.0) - 6.0, 0),
    (-(rear_plate_width/2.0) + 6.0, 0)
]).hole(small_hole_dia)


# Combine all parts
result = (
    main_body
    .union(fork_base)
    .union(arm1)
    .union(arm2)
    .union(rear_top_bar)
    .union(rear_bottom_bar)
    .union(vertical_connector)
)