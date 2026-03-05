import cadquery as cq

# Parameters for the hexagonal rod
rod_length = 100.0  # Total length of the rod
hex_size = 10.0     # Distance across flats (or effectively the diameter)
chamfer_dist = 0.5  # Size of the chamfer at the ends

# Create the hexagonal cross-section
# polygon with 6 sides, circumscribed radius calculated from flat-to-flat distance if needed, 
# but usually 'r' in cq.Workplane.polygon is the radius of the circumscribed circle.
# If hex_size is flat-to-flat distance (W), the radius R = W / sqrt(3).
# Let's assume hex_size is a reasonable radius or diameter equivalent.
# For a standard hex key or rod, often specified by "width across flats".
# Here, I'll treat hex_size as the circumradius for simplicity, or we can calculate it.
# Circumradius R = (Width Across Flats) / sqrt(3). 
# Let's just define a generic size parameter.

circumradius = hex_size / 1.732  # Approximate conversion if hex_size was width-across-flats. 
# Or simply use a direct radius parameter. Let's stick to a radius.
r_outer = 5.0 # Radius of circumscribed circle

result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_size * 2) # diameter here refers to the circumscribed circle diameter
    .extrude(rod_length)
)

# Apply chamfers to both ends
# We need to select the edges at the top and bottom faces (Z-min and Z-max)
# The selector ">Z" gets the top face, "<Z" gets the bottom face.
# Then we select the outer edges of those faces.

result = (
    result
    .faces("<Z or >Z") # Select both end faces
    .edges()           # Select the edges of these faces
    .chamfer(chamfer_dist)
)