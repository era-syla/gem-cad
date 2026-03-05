import cadquery as cq

# A shaft/pin with multiple cylindrical sections and a small hole
# From the image: a stepped shaft with larger middle section, smaller end stubs, and a small radial hole

# Dimensions (estimated from image proportions)
# Main body (large cylinder): length ~40, radius ~6
# Left stub: length ~12, radius ~3.5
# Right stub: length ~10, radius ~3
# Small hole: radius ~1.5, positioned on main body

result = (
    cq.Workplane("YZ")
    .circle(3.5)
    .extrude(12)
)

# Main large cylinder
main_body = (
    cq.Workplane("YZ")
    .workplane(offset=12)
    .circle(6.5)
    .extrude(40)
)

# Right taper/step - slightly smaller
right_step = (
    cq.Workplane("YZ")
    .workplane(offset=52)
    .circle(5)
    .extrude(8)
)

# Right small stub
right_stub = (
    cq.Workplane("YZ")
    .workplane(offset=60)
    .circle(3)
    .extrude(14)
)

# Combine all parts
shaft = result.union(main_body).union(right_step).union(right_stub)

# Add small radial hole through the main body
# Hole positioned roughly in center-left of main body
result = (
    shaft
    .faces(">X")
    .workplane()
    .center(-14, 0)
    .circle(1.5)
    .cutThruAll()
)