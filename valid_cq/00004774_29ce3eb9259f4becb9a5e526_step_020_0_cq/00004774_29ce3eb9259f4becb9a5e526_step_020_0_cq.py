import cadquery as cq

# Parameters
length = 80.0
width = 20.0
height = 10.0
corner_radius = 4.0  # Slightly rounded corners, not fully semicircular ends based on image

# Hole parameters
center_hole_diameter = 6.0
outer_hole_diameter = 6.0
small_hole_diameter = 3.0

# Distances from center
outer_hole_offset = 30.0
small_hole_offset = 18.0

# Create the main body
# We start with a box and fillet the vertical edges
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the holes
# 1. Center hole
result = result.faces(">Z").workplane().hole(center_hole_diameter)

# 2. Outer large holes (symmetric)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(outer_hole_offset, 0), (-outer_hole_offset, 0)])
    .hole(outer_hole_diameter)
)

# 3. Inner small holes (symmetric, offset from center but closer than outer holes)
# Looking at the image, these are slightly offset in Y as well?
# No, they look collinear along the X-axis, located between the center and outer holes.
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(small_hole_offset, 0), (-small_hole_offset, 0)])
    .hole(small_hole_diameter)
)