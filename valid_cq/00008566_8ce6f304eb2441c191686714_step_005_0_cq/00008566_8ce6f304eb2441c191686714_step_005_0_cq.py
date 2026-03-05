import cadquery as cq

# Parametric dimensions
large_outer_radius = 20.0
large_inner_radius = 12.0
small_outer_radius = 10.0
small_inner_radius = 3.0
thickness = 5.0
center_distance = 24.0  # Distance between the two circle centers

# Create the main body
# We will create two cylinders and fuse them, then cut the holes.
# Center of large circle at (0,0)
# Center of small circle at (-center_distance, 0)

# 1. Create the large disk
large_disk = cq.Workplane("XY").circle(large_outer_radius).extrude(thickness)

# 2. Create the small disk, shifted along X axis
small_disk = (
    cq.Workplane("XY")
    .center(-center_distance, 0)
    .circle(small_outer_radius)
    .extrude(thickness)
)

# 3. Fuse the two disks together
body = large_disk.union(small_disk)

# 4. Cut the large inner hole
body = body.faces(">Z").workplane().circle(large_inner_radius).cutThruAll()

# 5. Cut the small inner hole
# Note: We need to center the workplane correctly relative to the new body
# or just specify the center explicitly.
result = (
    body.faces(">Z")
    .workplane()
    .center(-center_distance, 0)
    .circle(small_inner_radius)
    .cutThruAll()
)