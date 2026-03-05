import cadquery as cq

# Create a coin/disc-like object with a slight dome on top and a rim around the edge

# Parameters
outer_radius = 50
inner_radius = 47
total_height = 8
rim_height = 3
dome_height = 2

# Create the base disc (rim portion)
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rim_height)
)

# Create the inner raised portion (slightly smaller radius, sits on top of base)
inner_disc = (
    cq.Workplane("XY")
    .workplane(offset=rim_height)
    .circle(inner_radius)
    .extrude(total_height - rim_height)
)

# Combine base and inner disc
result = base.union(inner_disc)

# Add a subtle dome/curve on the top face by creating a sphere-based cut
# The top surface should be slightly convex
# We achieve this by intersecting with a large sphere from above
sphere_radius = 800
sphere_center_z = total_height - dome_height + sphere_radius

dome_sphere = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .sphere(sphere_radius)
)

# Intersect to create domed top
result = result.intersect(dome_sphere)

# Add a groove line on top (the diagonal line visible in image)
# Create a thin cutting plane to simulate the seam line
groove_cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height - 0.5)
    .center(-60, 10)
    .rect(120, 0.8)
    .extrude(2)
    .rotate((0, 0, 0), (0, 0, 1), -20)
)

result = result.cut(groove_cutter)