import cadquery as cq

# Parameters
width = 100
height = 80
thickness = 5
post_diameter = 10
post_offset = 70

# Create main panel
panel = cq.Workplane("XY").box(width, thickness, height, centered=(True, True, False))

# Create posts
post = (cq.Workplane("XY")
        .circle(post_diameter / 2)
        .extrude(thickness + 10))

# Position posts
post_1 = post.translate((width / 2 - post_offset, 0, height / 2))
post_2 = post.translate((-(width / 2 - post_offset), 0, height / 2))

# Combine parts
result = panel.union(post_1).union(post_2)