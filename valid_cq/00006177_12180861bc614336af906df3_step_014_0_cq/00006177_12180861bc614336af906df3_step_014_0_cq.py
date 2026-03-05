import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
inner_diameter = 8.0
thickness = 3.0

# Create the washer geometry
# Method 1: Create a cylinder and cut a hole
# result = cq.Workplane("XY").cylinder(thickness, outer_diameter/2).faces(">Z").hole(inner_diameter)

# Method 2: Create a sketch with two concentric circles and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)