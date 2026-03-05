import cadquery as cq

# Parameters for the Reuleaux Tetrahedron / Spherical tetrahedron shape
radius = 50.0  # The radius of the spheres used to form the intersection

# Creating the shape
# A Reuleaux tetrahedron is formed by the intersection of 4 spheres
# centered at the vertices of a regular tetrahedron.
# The image shows a similar shape, often called a spherical tetrahedron or a curved tetrahedron.
# It looks like the intersection of four spheres positioned at tetrahedral vertices.

# 1. Define the vertices of a regular tetrahedron centered at the origin
# The vertices (x, y, z) can be defined as:
# (1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)
# We will scale these to match our desired radius. 
# However, for the intersection to be "puffy" like the image, the sphere radius needs 
# to be significantly larger than the distance from the center to the vertex.
# Let's place the centers such that the resulting shape is centered.

# Distance from center to vertex of tetrahedron with side length 'a' is a * sqrt(6) / 4.
# Let's simplify: construct 4 spheres.

# Offset distance for the centers of the spheres
offset = 25.0 
sphere_radius = 45.0

# Define the 4 corner points of a reference tetrahedron
p1 = (offset, offset, offset)
p2 = (offset, -offset, -offset)
p3 = (-offset, offset, -offset)
p4 = (-offset, -offset, offset)

# Create 4 spheres centered at these points
s1 = cq.Workplane("XY").center(*p1[:2]).workplane(offset=p1[2]).sphere(sphere_radius)
s2 = cq.Workplane("XY").center(*p2[:2]).workplane(offset=p2[2]).sphere(sphere_radius)
s3 = cq.Workplane("XY").center(*p3[:2]).workplane(offset=p3[2]).sphere(sphere_radius)
s4 = cq.Workplane("XY").center(*p4[:2]).workplane(offset=p4[2]).sphere(sphere_radius)

# The shape in the image is the intersection of these four spheres.
# This creates a shape bounded by 4 spherical caps.
result = s1.intersect(s2).intersect(s3).intersect(s4)

# Rotate the result for a better view alignment with the image (optional visual tweak)
# The image shows a vertex pointing down/towards the viewer slightly.
result = result.rotate((0,0,0), (1,0,0), 45).rotate((0,0,0), (0,0,1), 45)