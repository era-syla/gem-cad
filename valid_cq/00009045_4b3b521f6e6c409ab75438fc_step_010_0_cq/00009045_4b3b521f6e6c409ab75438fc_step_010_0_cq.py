import cadquery as cq

# --- Parametric Dimensions ---
# Overall block dimensions
block_length = 60.0  # Width of the block
block_height = 50.0  # Total height of the block
block_thickness = 20.0  # Depth of the block

# Cutout dimensions
cutout_radius = 20.0  # Radius of the semi-circular cutout
# The center of the cutout is assumed to be centered on the top edge

# --- Modeling Process ---

# 1. Create the main rectangular block
# We center it on X and Y to make symmetry operations easier if needed later,
# but aligning the bottom to Z=0 is good practice.
block = cq.Workplane("XY").box(block_length, block_thickness, block_height)

# 2. Create the cylindrical cutter
# The cylinder needs to be oriented along the Y-axis (thickness direction)
# and positioned so its axis intersects the top face of the block.
# We create a cylinder along the Y axis.
cutter = (
    cq.Workplane("XZ")
    .transformed(offset=(0, block_height / 2.0, 0)) # Move origin to top center of block
    .circle(cutout_radius)
    .extrude(block_thickness + 10.0, both=True) # Extrude enough to cut through, centered
)

# 3. Perform the boolean cut operation
result = block.cut(cutter)
