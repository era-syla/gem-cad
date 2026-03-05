import cadquery as cq

# Parameters used to define the model geometry
height = 80.0
width = 24.0
depth = 24.0
chamfer_size = 6.0
large_hole_diameter = 7.0
small_hole_diameter = 3.5
hole_depth = 20.0

# 1. Create the base rectangular prism centered on the XY plane
result = cq.Workplane("XY").box(width, depth, height)

# 2. Chamfer one of the vertical edges along the entire height.
# Selecting the edge at minimum X and maximum Y (top-left corner in top view)
result = result.edges("|Z and <X and >Y").chamfer(chamfer_size)

# 3. Create the two holes on the top face.
# The large hole is positioned closer to the chamfered edge (positive Y),
# and the small hole is positioned towards the opposite side (negative Y).
result = result.faces(">Z").workplane() \
    .pushPoints([(0, 5.0)]) \
    .hole(large_hole_diameter, depth=hole_depth) \
    .pushPoints([(0, -5.0)]) \
    .hole(small_hole_diameter, depth=hole_depth)