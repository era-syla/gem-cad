import cadquery as cq

# Parametric dimensions
width = 100.0       # Overall width of the U-shape
depth = 80.0        # Depth of the side arms
thickness = 10.0    # Thickness of the base material
height = 8.0        # Height of the profile
slot_width = 3.0    # Width of the internal groove/slot
slot_depth = 3.0    # Depth of the internal groove/slot
back_block_size = 15.0 # Size of the cube-like blocks at the back corners
back_block_height = 15.0 # Height of the back blocks

# Derived dimensions
arm_spacing = width - 2 * thickness

# 1. Create the main U-shaped profile
# We will sketch the path and sweep a profile, or extrude and cut. 
# A simpler approach for this rectilinear shape is to create the base U-shape and cut the slot.

# Create the base U-shape
# Coordinates are relative to the center of the back bar
path = (
    cq.Workplane("XY")
    .moveTo(-width/2 + thickness/2, 0)
    .lineTo(-width/2 + thickness/2, depth)  # Left arm path
    .moveTo(width/2 - thickness/2, 0)
    .lineTo(width/2 - thickness/2, depth)   # Right arm path
    .moveTo(-width/2, 0)
    .lineTo(width/2, 0)                     # Back bar path (centerline logic needs care)
)

# Alternative method: Build separate bars and union them. This is often cleaner for control.

# Left Arm
left_arm = (
    cq.Workplane("XY")
    .box(thickness, depth, height, centered=(True, False, False))
    .translate((-width/2 + thickness/2, 0, 0))
)

# Right Arm
right_arm = (
    cq.Workplane("XY")
    .box(thickness, depth, height, centered=(True, False, False))
    .translate((width/2 - thickness/2, 0, 0))
)

# Back Bar
# It connects the two arms at the start (y=0)
back_bar = (
    cq.Workplane("XY")
    .box(width, thickness, height, centered=(True, False, False))
    .translate((0, 0, 0))
)

# Union the main frame
frame = left_arm.union(right_arm).union(back_bar)

# 2. Create the groove/slot
# The slot runs along the inside of the U-shape.
# It seems to be centered vertically on the bar height.

# Slot Profile
slot_z = height / 2

# Cut slot on Left Arm (inner face is facing +X)
# The arm is at x = -width/2 + thickness/2. Inner face x = -width/2 + thickness.
cut_left = (
    cq.Workplane("YZ")
    .rect(depth, slot_width)
    .extrude(slot_depth)
    .translate((-width/2 + thickness, depth/2, slot_z))
    # Needs rotation or careful plane selection.
    # Let's re-think: just make a cutter object.
)

# Create a U-shaped cutter for the slot
# The slot follows the inside perimeter.
inner_width = width - 2 * thickness

# Slot on the back bar (inner face facing +Y)
back_slot_cutter = (
    cq.Workplane("XY")
    .box(inner_width, slot_depth, slot_width, centered=(True, False, True))
    .translate((0, thickness/2, slot_z)) # Shift to inner face of back bar
)

# Slot on the left arm (inner face facing +X)
left_slot_cutter = (
    cq.Workplane("XY")
    .box(slot_depth, depth - thickness/2, slot_width, centered=(False, False, True))
    .translate((-width/2 + thickness - slot_depth, thickness/2, slot_z))
)

# Slot on the right arm (inner face facing -X)
right_slot_cutter = (
    cq.Workplane("XY")
    .box(slot_depth, depth - thickness/2, slot_width, centered=(False, False, True))
    .translate((width/2 - thickness, thickness/2, slot_z))
)

slot_cutters = back_slot_cutter.union(left_slot_cutter).union(right_slot_cutter)

# Apply the cut
frame_with_slot = frame.cut(slot_cutters)

# 3. Add the corner blocks
# Located at the back corners of the U-shape.
# Based on image, they stick out backwards slightly or are flush with back, and stick up.
# Let's assume they are centered on the corners of the overall bounding box.

block_left = (
    cq.Workplane("XY")
    .box(back_block_size, back_block_size, back_block_height, centered=(True, True, False))
    .translate((-width/2 + thickness/2, thickness/2, 0)) # Positioned at the corner
    # Adjust position to match image: looks like it sits "behind" the main U slightly?
    # No, it looks like it sits on top of the corner join.
    # Let's align it with the outer back corner.
    .translate((0, -back_block_size/2 + thickness/2, 0)) 
)

block_right = (
    cq.Workplane("XY")
    .box(back_block_size, back_block_size, back_block_height, centered=(True, True, False))
    .translate((width/2 - thickness/2, thickness/2, 0))
    .translate((0, -back_block_size/2 + thickness/2, 0))
)

# Combine everything
result = frame_with_slot.union(block_left).union(block_right)