import cadquery as cq

# Ring part
ring = cq.Workplane("XY") \
    .circle(10) \
    .circle(7) \
    .extrude(10)

# Lever base cylinder
base = cq.Workplane("XY") \
    .center(-40, 0) \
    .circle(6) \
    .extrude(12)

# Rectangular arm on top of the cylinder
# Base cylinder center x = -40, radius = 6, so rim at -34
bar = cq.Workplane("XY") \
    .transformed(offset=(-34, 0, 14)) \
    .box(30, 4, 4, centered=(False, True, True))

# Small pin at end of the arm, extruded along the arm direction (X-axis)
pin = cq.Workplane("YZ", origin=(-4, 0, 16)) \
    .circle(2) \
    .extrude(6)

# Combine all parts into one result
result = cq.Workplane("XY") \
    .add(ring.val()) \
    .add(base.val()) \
    .add(bar.val()) \
    .add(pin.val())