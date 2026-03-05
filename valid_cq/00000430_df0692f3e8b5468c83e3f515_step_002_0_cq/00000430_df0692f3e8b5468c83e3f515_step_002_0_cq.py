import cadquery as cq

# Parametric dimensions
base_width = 100.0   # Length of the base box
base_depth = 50.0    # Width of the base box
base_height = 50.0   # Height of the base box

lid_thickness = 5.0  # Thickness of the top plate/lid
lid_overhang = 2.0   # How much the lid extends past the base on all sides

# Calculated dimensions for the lid
lid_width = base_width + (2 * lid_overhang)
lid_depth = base_depth + (2 * lid_overhang)

# Create the base box
# We create a simple box centered on X and Y, sitting on the Z plane
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# Create the lid
# We create another box on top of the base. 
# We need to offset the workplane to the top of the base.
lid = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2 + lid_thickness/2)
    .box(lid_width, lid_depth, lid_thickness)
)

# Combine the parts
# Since the base was centered at Z=0 with height 50, its top is at Z=25.
# However, standard box() is centered on all axes.
# Let's rebuild more precisely to ensure alignment.

# Alternative approach: Build from bottom up to be clearer about positions.

# 1. Base Box
# Centered at (0,0, base_height/2) so the bottom is at Z=0
base = cq.Workplane("XY").box(base_width, base_depth, base_height, centered=(True, True, False))

# 2. Lid
# Positioned on top of the base. Z start = base_height.
lid = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .box(lid_width, lid_depth, lid_thickness, centered=(True, True, False))
)

# Combine into a single object
result = base.union(lid)