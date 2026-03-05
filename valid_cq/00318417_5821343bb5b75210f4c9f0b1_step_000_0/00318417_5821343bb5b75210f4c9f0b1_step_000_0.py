import cadquery as cq

# Parametric dimensions
cube_size = 10.0
ring_outer_diameter = 50.0
ring_thickness = 1.0
ring_height = 10.0
# Distance between the center of the cube and the center of the ring
center_distance = 60.0

# Create the cube
# The box is created centered at the origin by default, so we translate it to the left
cube = (
    cq.Workplane("XY")
    .box(cube_size, cube_size, cube_size)
    .translate((-center_distance, 0, 0))
)

# Create the ring
# We draw the outer circle and inner circle to create a hollow profile, then extrude
ring = (
    cq.Workplane("XY")
    .circle(ring_outer_diameter / 2.0)
    .circle((ring_outer_diameter / 2.0) - ring_thickness)
    .extrude(ring_height)
)

# Adjust vertical alignment
# The default box is centered in Z (from -height/2 to +height/2).
# The default extrude goes from Z=0 to Z=height.
# We translate the ring down by half its height to align its center with the cube.
ring = ring.translate((0, 0, -ring_height / 2.0))

# Combine the two objects into a single result
result = cube.union(ring)