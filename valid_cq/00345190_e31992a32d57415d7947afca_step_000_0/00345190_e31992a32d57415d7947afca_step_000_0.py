import cadquery as cq

# Parametric dimensions estimated from the image
width = 100.0       # Total width of the plate
depth = 70.0        # Total depth of the plate
thickness = 5.0     # Thickness of the plate
notch_width = 60.0  # Width of the rectangular cutout
notch_depth = 20.0  # Depth of the rectangular cutout

# 1. Create the base rectangular plate
# We center it on the XY plane for easier symmetry operations
base = cq.Workplane("XY").box(width, depth, thickness)

# 2. Create the cutout geometry
# We create a box that acts as a "tool" to cut the notch.
# We position it at the center of the top edge (y = depth/2).
# By making the cutter depth = notch_depth * 2 and centering it on the edge,
# it will penetrate exactly 'notch_depth' into the material.
# We also make the cutter thicker than the plate to ensure a clean boolean cut.
cutter = (
    cq.Workplane("XY")
    .moveTo(0, depth / 2)
    .box(notch_width, notch_depth * 2, thickness * 2)
)

# 3. Subtract the cutter from the base to create the final shape
result = base.cut(cutter)