import cadquery as cq

# Ring with a stepped/groove profile
# Outer ring with a smaller raised inner ring on top

outer_radius = 50
inner_radius = 38
height_main = 10
height_raised = 3
groove_outer_radius = 47
groove_inner_radius = 41

# Create the main ring (outer annulus)
main_ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height_main)
)

# Create the raised inner ring (groove/step on top)
raised_ring = (
    cq.Workplane("XY")
    .workplane(offset=height_main)
    .circle(groove_outer_radius)
    .circle(groove_inner_radius)
    .extrude(height_raised)
)

result = main_ring.union(raised_ring)