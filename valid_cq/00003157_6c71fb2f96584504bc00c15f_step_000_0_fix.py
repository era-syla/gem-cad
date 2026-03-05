import cadquery as cq

# Create a cylinder (large end) + hex prism (small end) combination
# The shape looks like a cylinder on the left with a rounded hex shaft extending to the right

# Parameters
cyl_radius = 15
cyl_height = 20
hex_diameter = 14  # across flats
hex_length = 30

# Create the main cylinder
cylinder = (
    cq.Workplane("YZ")
    .circle(cyl_radius)
    .extrude(cyl_height)
)

# Create the hex shaft - polygon with 6 sides
# The hex shaft extends from the right face of the cylinder
hex_shaft = (
    cq.Workplane("YZ")
    .workplane(offset=cyl_height)
    .polygon(6, hex_diameter)
    .extrude(hex_length)
)

# Combine cylinder and hex shaft
result = cylinder.union(hex_shaft)

# Add fillet to the end of the hex shaft
result = (
    result
    .edges(">X")
    .fillet(2.5)
)