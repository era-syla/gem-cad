import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
length = 60.0
width = 20.0
height_right = 20.0  # Height of the block on the right
height_left = 30.0   # Height of the block on the left
base_thickness = 10.0 # Thickness of the connecting bottom plate

# Left side chamfer
chamfer_size = 5.0

# Right side hole
hole_diameter = 6.0
hole_height = 10.0 # Height from bottom to center of hole (centered in the block)

# Center Slot
slot_width = 6.0
slot_length = 30.0
# The slot is centered along the width and positioned in the middle of the base

# --- Modeling ---

# 1. Start with the main body profile. 
# We'll create the side profile (XZ plane) and extrude it along Y (width).
# Profile shape:
# (0,0) -> (length, 0) -> (length, height_right) -> (length - thickness_right, height_right)
# -> (length - thickness_right, base_thickness) -> (thickness_left, base_thickness)
# -> (thickness_left, height_left) -> (0, height_left) -> close
# Let's simplify: Create a base block, then add the two uprights.

# Alternative approach: Constructive Solid Geometry (CSG)
# Create the base plate
base = cq.Workplane("XY").box(length, width, base_thickness)

# Create the left upright
# Position: -X end.
# Dimensions: thickness_left x width x (height_left - base_thickness) sitting on top
thickness_left = 10.0
left_block = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2) # Top of base
    .center(-length/2 + thickness_left/2, 0)
    .box(thickness_left, width, height_left - base_thickness, centered=(True, True, False))
)

# Create the right upright
# Position: +X end
# Dimensions: thickness_right x width x (height_right - base_thickness) sitting on top
thickness_right = 10.0
right_block = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2) # Top of base
    .center(length/2 - thickness_right/2, 0)
    .box(thickness_right, width, height_right - base_thickness, centered=(True, True, False))
)

# Combine the parts
result = base.union(left_block).union(right_block)

# 2. Add the Chamfer on the left upright
# We need to select the top outer edge of the left block.
# That edge is at x = -length/2, z = height_left - base_thickness/2 (since base center is at 0,0,0)
# Actually, let's just select by position.
# The top face of the left block is the highest Z face.
# The outer edge corresponds to the min X coordinate on that face.
result = result.edges(f">Z and <X").chamfer(chamfer_size)


# 3. Add the Hole on the right upright
# It goes through the right face (max X).
# Centered in Y, and at a specific Z height.
# Z center of the hole should be in the middle of the right block's face? 
# Looking at the image, it looks centered on the square face of the right block.
# Height of right block is 20, so center is at 10 from bottom.
# Since our origin is center of base (Z=0), bottom is at -base_thickness/2 (-5).
# So hole center Z = -5 + 10 = 5.
result = (
    result.faces(">X")
    .workplane()
    .center(0, (height_right/2) - (base_thickness/2)) # Shift center up relative to face center if needed, but face center is at Z=5 relative to global?
    # Let's re-verify face center. 
    # The right face spans Z from -5 to +15. Center is at Z=5. Perfect.
    # So we just drill at the center of the workplane.
    .hole(hole_diameter)
)

# 4. Add the Slot in the base
# The slot is in the base plate. It looks like a slot with rounded ends.
# Position: Centered in the base.
# Orientation: Along X axis.
result = (
    result.faces(">Z[1]") # Select the top face of the base (between the uprights)
    # Since there are multiple faces at different Z heights, we need to be careful.
    # The base top face is at Z = base_thickness/2 = 5.
    # The upright tops are higher. 
    # Let's select by nearest point or simply construct on the XY plane and cut.
    .workplane(centerOption="CenterOfBoundBox")
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)

# Refinement on Slot selection logic to be more robust:
# Create a cutter and subtract it.
# Slot center is (0,0,0).
# cutter = (
#     cq.Workplane("XY")
#     .slot2D(slot_length, slot_width)
#     .extrude(base_thickness + 5, both=True) # Make sure it cuts through
# )
# result = result.cut(cutter)
# The previous method using faces(">Z[1]") might select the wrong face depending on sorting.
# Let's stick to the robust cut method.

result = (
    result.faces("<Z") # Bottom face
    .workplane()
    .slot2D(slot_length, slot_width)
    .cutThruAll()
)

# Final check of the model
# - Left block with chamfer
# - Right block with hole
# - Base connecting them
# - Slot in the base