import cadquery as cq

# Parametric dimensions
outer_radius = 12.0
inner_radius = 7.0
thickness = 5.0
center_distance = 21.0  # Distance between the centers of the two rings

# Create the first ring (left side)
# We define concentric circles to create a hollow cylinder
left_ring = (
    cq.Workplane("XY")
    .moveTo(-center_distance / 2, 0)
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

# Create the second ring (right side)
right_ring = (
    cq.Workplane("XY")
    .moveTo(center_distance / 2, 0)
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

# Combine the two intersecting rings into a single solid
result = left_ring.union(right_ring)