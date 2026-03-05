import cadquery as cq

# Create a sphere-like bowl shape - appears to be a sphere with the top cut off
# and hollowed out to create a bowl/vase shape

r = 50  # radius of the sphere

# Start with a sphere
sphere = cq.Workplane("XY").sphere(r)

# Cut the top portion to create a flat opening
# The opening appears to be roughly at 70% up the sphere
cut_height = r * 0.3  # cut from this height upward

top_cut = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, cut_height))
    .box(r * 3, r * 3, r * 2, centered=(True, True, False))
)

bowl_outer = sphere.cut(top_cut)

# Now hollow out the inside - create an inner sphere slightly smaller
inner_r = r * 0.88

inner_sphere = cq.Workplane("XY").sphere(inner_r)

# Also cut the inner sphere top
inner_top_cut = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, cut_height - 3))
    .box(r * 3, r * 3, r * 2, centered=(True, True, False))
)

inner_cavity = inner_sphere.cut(inner_top_cut)

# Subtract inner cavity from outer bowl
result = bowl_outer.cut(inner_cavity)

# Add slight fillet to the rim edge
result = (
    result
    .edges(">Z")
    .fillet(2)
)