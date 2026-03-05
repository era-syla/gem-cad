import cadquery as cq
import math

# Parameters
rim_outer_radius = 50.0
rim_inner_radius = 48.0
rim_width = 5.0

hub_outer_radius = 5.0
hub_inner_radius = 3.0
hub_width = 6.0

num_spokes = 16
spoke_radius = 0.5

# Create rim
rim = (
    cq.Workplane("XY")
    .circle(rim_outer_radius)
    .circle(rim_inner_radius)
    .extrude(rim_width)
)

# Create hub
hub = (
    cq.Workplane("XY")
    .circle(hub_outer_radius)
    .circle(hub_inner_radius)
    .extrude(hub_width)
)

# Create spokes
spokes = cq.Workplane("XY")
for i in range(num_spokes):
    angle = i * (360.0 / num_spokes)
    spoke = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .center(hub_outer_radius - 0.5, 0)
        .circle(spoke_radius)
        .extrude(rim_inner_radius - hub_outer_radius + 1.0)
    )
    # Adjust position to be centered in Z
    spoke = spoke.translate((0, 0, rim_width / 2.0 - spoke_radius))
    
    if i == 0:
        spokes = spoke
    else:
        spokes = spokes.union(spoke)

# Combine parts
result = rim.union(hub).union(spokes)

# Center the whole assembly
result = result.translate((0, 0, -rim_width / 2.0))