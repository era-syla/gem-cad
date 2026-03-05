import cadquery as cq

# Create a sphere and cut it to create an eighth-sphere (octant).
# We start with a full sphere and intersect it with a large box positioned in the first octant,
# or simply intersect three half-spaces. Another clean way is to revolve a quarter-circle arc.
# However, boolean operations on primitives are often the most straightforward in CadQuery.

# Parameters
radius = 10.0

# Method 1: Boolean Intersection of a Sphere and a Box
# We create a sphere centered at origin.
sphere = cq.Workplane("XY").sphere(radius)

# We create a large box positioned such that one corner is at the origin (0,0,0)
# and it extends into the positive X, Y, and Z directions.
# To ensure it fully covers the sphere's octant, the box size should be >= radius.
# The center of such a box of size 's' would be at (s/2, s/2, s/2).
box_size = radius * 1.1 # Slightly larger to ensure clean cut
box = cq.Workplane("XY").box(box_size, box_size, box_size).translate((box_size/2, box_size/2, box_size/2))

# Intersect the sphere with the box to keep only the volume common to both (the 1/8th sphere)
result = sphere.intersect(box)

# Alternative Method (more geometric construction style):
# result = (
#     cq.Workplane("XY")
#     .moveTo(0, 0)
#     .lineTo(radius, 0)
#     .radiusArc((0, radius), -radius) # Quarter circle in XY plane
#     .close()
#     .revolve(90, (0,0,0), (0,1,0)) # Revolve 90 degrees around Y axis
#     # Note: Revolution axes can be tricky depending on the initial plane orientation.
# )

# Export or display the result (standard boilerplate for these requests usually just creates 'result')