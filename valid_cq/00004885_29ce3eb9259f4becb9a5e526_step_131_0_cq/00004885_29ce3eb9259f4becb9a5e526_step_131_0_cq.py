import cadquery as cq

# -- Parametric Dimensions --
length = 80.0       # Total width of the block
height = 80.0       # Total height of the block
thickness = 25.0    # Thickness of the block

corner_chamfer = 10.0  # Size of the chamfer on the corners

# Mounting holes (4 corners)
mount_hole_dia = 10.0
mount_hole_spacing = 50.0  # Distance between hole centers (square pattern)

# Center hole
center_hole_dia = 15.0

# Side hole
side_hole_dia = 8.0
side_hole_depth = 15.0 # Depth of side hole, though it might be through. Let's make it through to center or just deep enough.

# -- Geometry Construction --

# 1. Base Block
# Create a centered rectangle and extrude it
base = cq.Workplane("XY").box(length, height, thickness)

# 2. Chamfer Corners
# Select edges parallel to Z axis (the vertical edges of the block in XY plane perspective)
# The image shows chamfers on all 4 corners, or at least visible ones suggest symmetry.
# Let's apply to all 4 corners for a standard mounting plate look.
result = base.edges("|Z").chamfer(corner_chamfer)

# 3. Face Holes
# Create the 4 corner mounting holes and the center hole.
# We work on the front face (Z max).
result = (
    result.faces(">Z")
    .workplane()
    # Create the 4 corner holes using a rectangular pattern
    .rect(mount_hole_spacing, mount_hole_spacing, forConstruction=True)
    .vertices()
    .hole(mount_hole_dia)
    # Create the center hole
    .center(0, 0) # Reset to center
    .hole(center_hole_dia)
)

# 4. Side Hole
# The image shows a hole on the left vertical face (-X).
# It looks centered vertically on that face.
result = (
    result.faces("<X")
    .workplane()
    .center(0, 0) # Center on the face
    .hole(side_hole_dia)
)

# Return the final result
# The variable 'result' contains the final geometry as requested.