import cadquery as cq

# -- Parametric Dimensions --
channel_width = 15.0       # Outer width of the channel
channel_height = 12.0      # Outer height of the channel
wall_thickness = 1.5       # Thickness of walls and floor
trunk_length = 40.0        # Length of the straight main section
arm_length = 35.0          # Length of the branching arms
branch_angle = 35.0        # Angle of arms from the center axis (degrees)

flange_length = 20.0       # Length of the side mounting tabs
flange_width = 6.0         # Width (stick-out) of the tabs
flange_thickness = 2.0     # Thickness of the tabs
flange_top_offset = 3.0    # Distance from the top rim to the top of the flange

# -- Modeling --

# 1. Create the Main Trunk
# Positioned starting at Y=0, centered on X, sitting on Z=0
trunk = (
    cq.Workplane("XY")
    .box(channel_width, trunk_length, channel_height)
    .translate((0, trunk_length / 2, channel_height / 2))
)

# 2. Create the Arms
# Helper to create an arm positioned at the origin pointing up Y
base_arm = (
    cq.Workplane("XY")
    .box(channel_width, arm_length, channel_height)
    .translate((0, arm_length / 2, channel_height / 2))
)

# Left Arm: Rotate and move to end of trunk
left_arm = (
    base_arm
    .rotate((0, 0, 0), (0, 0, 1), branch_angle)
    .translate((0, trunk_length, 0))
)

# Right Arm: Rotate and move to end of trunk
right_arm = (
    base_arm
    .rotate((0, 0, 0), (0, 0, 1), -branch_angle)
    .translate((0, trunk_length, 0))
)

# Union the base shapes
solid_y = trunk.union(left_arm).union(right_arm)

# 3. Hollow out to create U-channel
# Select the top faces and shell inwards
# A negative thickness in shell() removes the selected face and adds thickness inwards
channel = solid_y.faces(">Z").shell(-wall_thickness)

# 4. Add Flanges
# Calculate Z position for the flange center
flange_z = channel_height - flange_top_offset - (flange_thickness / 2)

# Left Flange
flange_l = (
    cq.Workplane("XY")
    .box(flange_width, flange_length, flange_thickness)
    .translate((-channel_width/2 - flange_width/2, flange_length/2, flange_z))
)

# Right Flange
flange_r = (
    cq.Workplane("XY")
    .box(flange_width, flange_length, flange_thickness)
    .translate((channel_width/2 + flange_width/2, flange_length/2, flange_z))
)

# Final Boolean Union
result = channel.union(flange_l).union(flange_r)