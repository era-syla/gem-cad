import cadquery as cq

# --- Parametric Dimensions ---
# Overall plate dimensions
length = 60.0
width = 20.0
thickness = 6.0

# Central square recess dimensions
recess_size = 14.0  # Square side length
recess_depth = 3.0

# Central hole dimensions
center_hole_diameter = 6.0

# Mounting hole dimensions (the two side holes)
mount_hole_diameter = 4.0
mount_hole_spacing = 40.0 # Distance between centers (20mm from center each side)

# --- Geometry Construction ---

# 1. Create the main rectangular block
base = cq.Workplane("XY").box(length, width, thickness)

# 2. Create the central square pocket (recess)
# We select the top face, sketch a rectangle, and cut down
result = (
    base
    .faces(">Z")
    .workplane()
    .rect(recess_size, recess_size)
    .cutBlind(-recess_depth)
)

# 3. Create the central through-hole
# This hole goes through the bottom of the recess
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(center_hole_diameter)
)

# 4. Create the two mounting holes
# We use pushPoints to place them symmetrically
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)])
    .hole(mount_hole_diameter)
)