import cadquery as cq

# Define the outer ring dimensions
outer_diameter = 40
outer_radius = outer_diameter / 2
inner_diameter = 30
inner_radius = inner_diameter / 2
thickness = 10

# Create the outer ring
ring = (cq.Workplane("XY")
        .circle(outer_radius)
        .circle(inner_radius)
        .extrude(thickness))

# Define the cylinder dimensions
cylinder_length = 60
cylinder_radius = 7

# Create the cylinder and position it
cylinder = (cq.Workplane("XY")
            .workplane(offset=thickness)
            .circle(cylinder_radius)
            .extrude(cylinder_length))

# Union the ring and cylinder
result = ring.union(cylinder)