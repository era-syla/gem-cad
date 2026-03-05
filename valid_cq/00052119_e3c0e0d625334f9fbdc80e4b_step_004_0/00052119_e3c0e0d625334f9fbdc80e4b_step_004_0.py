import cadquery as cq

# Dimensions
base_length = 50.0
base_width = 40.0
base_thickness = 3.0

# Anchor (Central Block) dimensions
anchor_length = 20.0
anchor_width_bottom = 26.0
anchor_width_top = 8.0
anchor_height = 14.0
anchor_center_x = 5.0  # Offset from center to allow room for the hole

# Arm dimensions
arm_length = 60.0
arm_width = 8.0
arm_height = 14.0 # Matches anchor height

# Features
hole_diameter = 5.0
hole_pos_x = -15.0

notch_pos_rel = 25.0 # Distance from start of arm
notch_width = 6.0
notch_depth = 5.0

tip_chamfer = 8.0

# 1. Base Plate
# Create the base plate centered on the XY plane
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# 2. Hole
# Cut the hole in the front section of the base
result = (
    result.faces(">Z").workplane()
    .center(hole_pos_x, 0)
    .hole(hole_diameter)
)

# 3. Anchor (Transition Block)
# Create a loft from the base plate top to the arm height
# Define the bottom profile on the top of the base
anchor_bottom_plane = result.faces(">Z").workplane().center(anchor_center_x, 0)
# Define the top profile at the anchor height
anchor_top_plane = anchor_bottom_plane.workplane(offset=anchor_height)

# Create the solid via loft
anchor = (
    anchor_bottom_plane
    .rect(anchor_length, anchor_width_bottom)
    .workplane(offset=anchor_height)
    .rect(anchor_length, anchor_width_top)
    .loft(combine=True)
)

# 4. Arm
# Create the arm extending from the anchor
# Calculate arm position
arm_start_x = anchor_center_x + (anchor_length / 2.0)
arm_center_x = arm_start_x + (arm_length / 2.0)
arm_center_z = (base_thickness / 2.0) + (arm_height / 2.0)

# Create arm box
arm = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2.0) # Start at base top level
    .center(arm_center_x, 0)
    .box(arm_length, arm_width, arm_height, centered=(True, True, False))
)

# Union the arm to the main assembly
result = anchor.union(arm)

# 5. Notch
# Cut a rectangular notch on the top of the arm
notch_abs_x = arm_start_x + notch_pos_rel
# We establish a workplane on the top surface (base + anchor height)
top_z = (base_thickness / 2.0) + anchor_height

result = (
    result.workplane(offset=top_z) # Set Z to top of arm
    .center(notch_abs_x, 0) # Move to notch X position
    .rect(notch_width, arm_width + 2.0) # Slightly wider than arm to ensure clean cut
    .cutBlind(-notch_depth)
)

# 6. Tip Chamfer
# Chamfer the top edge at the end of the arm
# Select the edge with the highest X and highest Z coordinate
result = result.edges(">X and >Z").chamfer(tip_chamfer)