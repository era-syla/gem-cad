import cadquery as cq

# Traffic cone dimensions
base_size = 80       # square base side length
base_height = 8      # height of the flat base
cone_base_radius = 35  # radius of cone at bottom
cone_top_radius = 8    # radius of cone at top
cone_height = 100    # height of the cone part
hole_radius = 5      # hole at the top
hole_depth = 80      # depth of the hole from top

# Create the square base with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_size, base_size)
    .extrude(base_height)
    .edges("|Z")
    .fillet(5)
    .edges(">Z or <Z")
    .fillet(1.5)
)

# Create a circular groove/ridge ring on top of the base
ring_outer = cone_base_radius + 4
ring_inner = cone_base_radius - 2
ring_height = 2

groove = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(ring_outer)
    .circle(ring_inner)
    .extrude(ring_height)
)

# Create the cone body using revolve
# Profile: from base to top
cone_profile = (
    cq.Workplane("XZ")
    .moveTo(0, base_height)
    .lineTo(cone_base_radius, base_height)
    .lineTo(cone_top_radius, base_height + cone_height)
    .lineTo(0, base_height + cone_height)
    .close()
)

cone = cone_profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Create the hole at the top of the cone
hole = (
    cq.Workplane("XY")
    .workplane(offset=base_height + cone_height)
    .circle(hole_radius)
    .extrude(-hole_depth)
)

# Combine base + groove + cone, then subtract hole
result = (
    base
    .union(groove)
    .union(cone)
    .cut(hole)
)