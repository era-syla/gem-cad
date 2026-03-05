import cadquery as cq

# Parameters defining the geometry
base_diameter = 10.0
base_length = 60.0
post_diameter = 10.0
post_height = 25.0
post_spacing = 30.0
start_offset = 15.0  # Distance from the end of the base to the first post

# Create the horizontal base cylinder
# Drawn on the YZ plane and extruded along the X-axis
base = cq.Workplane("YZ").circle(base_diameter / 2.0).extrude(base_length)

# Create the vertical posts
# Drawn on the XY plane (at Z=0) to intersect the base, extruded upwards in Z
# Using pushPoints to create both cylinders in one operation
posts = (
    cq.Workplane("XY")
    .pushPoints([
        (start_offset, 0), 
        (start_offset + post_spacing, 0)
    ])
    .circle(post_diameter / 2.0)
    .extrude(post_height)
)

# Combine the base and posts into the final solid
result = base.union(posts)