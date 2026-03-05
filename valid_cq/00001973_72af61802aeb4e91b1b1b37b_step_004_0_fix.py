import cadquery as cq

# Dimensions
length = 30
hex_width = 20  # across flats for hexagonal cross-section
cylinder_radius = 11
hole1_radius = 4
hole2_radius = 2.5
hole1_offset = 0  # center hole
hole2_offset = 5  # offset for small hole

# Create the main body: intersection of a hexagonal prism and a cylinder
# The shape appears to be a cylinder with hexagonal ends / hex prism with rounded sides

# Create hexagonal prism
hex_prism = (
    cq.Workplane("YZ")
    .polygon(6, hex_width * 2 / (3**0.5))  # diameter from flat to flat
    .extrude(length)
)

# Create cylinder along same axis
cylinder = (
    cq.Workplane("YZ")
    .circle(cylinder_radius)
    .extrude(length)
)

# Intersect to get the shape (hex with rounded profile or cylinder with hex ends)
# Looking at the image: it's a hex prism but with cylindrical sides - intersection of both
body = hex_prism.intersect(cylinder)

# Now cut the two holes through the length (along X axis)
# Large center hole
body = (
    body
    .faces(">X")
    .workplane()
    .hole(hole1_radius * 2)
)

# Small offset hole
body = (
    body
    .faces(">X")
    .workplane()
    .center(0, hole2_offset)
    .circle(hole2_radius)
    .cutThruAll()
)

result = body