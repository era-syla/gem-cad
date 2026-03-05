import cadquery as cq

# Parameters for the geometry
large_cube_size = 20.0
small_cube_size = 10.0
connecting_rod_width = 5.0
connecting_rod_length = 40.0 # Length covering the distance between shapes
sphere_radius = 12.0

# 1. Create the main connecting rod (the central spine)
# We orient this along the X-axis for easier visualization.
rod = cq.Workplane("YZ").box(connecting_rod_width, connecting_rod_width, connecting_rod_length)

# 2. Create the large cube at one end
# We position it at the positive X end of the rod.
large_cube = (
    cq.Workplane("YZ")
    .workplane(offset=connecting_rod_length / 2)
    .box(large_cube_size, large_cube_size, large_cube_size)
)

# 3. Create the small intermediate cube
# This cube seems to be positioned somewhere along the rod.
# Let's place it roughly in the middle-ish, offset towards the sphere side.
small_cube_offset = -connecting_rod_length / 6
small_cube = (
    cq.Workplane("YZ")
    .workplane(offset=small_cube_offset)
    .box(small_cube_size, small_cube_size, small_cube_size)
)

# 4. Create the sphere at the other end
# We position it at the negative X end of the rod.
sphere_center_offset = -connecting_rod_length / 2
sphere = (
    cq.Workplane("XY")
    .transformed(offset=(sphere_center_offset, 0, 0))
    .sphere(sphere_radius)
)

# 5. Combine all parts into a single object
result = rod.union(large_cube).union(small_cube).union(sphere)

# Export or visualization steps would happen here in a real IDE,
# but the variable 'result' holds the final geometry as requested.