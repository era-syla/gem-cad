import cadquery as cq

# Parameters
R = 100
tube_dia = 5
tube_radius = tube_dia / 2
ring_inner = tube_radius + 0.3
ring_outer = ring_inner + 1.0
ring_height = tube_dia + 4

# Create the arc path in the XY plane
path = (
    cq.Workplane("XY")
    .moveTo(R, 0)
    .threePointArc((0, R), (-R, 0))
    .wire()
    .val()
)

# Sweep a circular profile (in the XZ plane) along the arc to make the rod
rod = (
    cq.Workplane("XZ")
    .circle(tube_radius)
    .sweep(path)
)

# Create a ring (washer) at the midpoint of the arc
ring = (
    cq.Workplane("XY")
    .moveTo(0, R)
    .circle(ring_outer)
    .circle(ring_inner)
    .extrude(ring_height)
)

# Combine rod and ring into the final result
result = rod.union(ring)