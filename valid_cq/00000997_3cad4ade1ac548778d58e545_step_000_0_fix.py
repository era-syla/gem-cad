import cadquery as cq
import math

# Create a torus-like ring shape with a complex swept profile
# The image shows what appears to be a torus with an inner cutout - like a ring/gasket

# Main outer torus
outer_radius = 40  # major radius
outer_tube = 12    # minor radius

# Create the main torus by revolving a circle
outer_torus = (
    cq.Workplane("XZ")
    .transformed(offset=(outer_radius, 0, 0))
    .circle(outer_tube)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# Inner torus (smaller, to create ring-like appearance)
inner_radius = 40
inner_tube = 7

inner_torus = (
    cq.Workplane("XZ")
    .transformed(offset=(inner_radius, 0, 0))
    .circle(inner_tube)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# Subtract inner from outer to get a hollow ring
ring = outer_torus.cut(inner_torus)

# Now create the complex shape - looks like an angled/tilted torus with cutout
# Create a second torus tilted at an angle
tilted_torus = (
    cq.Workplane("XZ")
    .transformed(offset=(outer_radius * 0.85, 0, 0))
    .circle(outer_tube * 0.9)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

# Rotate the tilted torus
tilted_torus = tilted_torus.rotate((0, 0, 0), (0, 1, 0), 45)

# Create another angled torus
angled_torus = (
    cq.Workplane("YZ")
    .transformed(offset=(outer_radius * 0.9, 0, 0))
    .circle(outer_tube * 0.85)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

angled_torus = angled_torus.rotate((0, 0, 0), (1, 0, 0), 30)

# Union the shapes to create complex geometry
result = ring.union(tilted_torus).union(angled_torus)

# Add a box cut to create the distinctive opening seen in the image
cutter = (
    cq.Workplane("XY")
    .box(30, 60, 60)
    .translate((-15, 0, 0))
)

result = result.cut(cutter)