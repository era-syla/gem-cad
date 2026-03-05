import cadquery as cq

# Define dimensions
outer_radius = 10
inner_radius = 8
ring_thickness = 2
spacing = 18

# Create a single ring
ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(ring_thickness)
)

# Create three rings with spacing
result = ring.translate((0, -spacing, 0)).union(
    ring.translate((0, spacing, 0))
).union(
    ring
)

# Optional: Add fillets to round the edges
result = result.edges("|Z").fillet(1.0)