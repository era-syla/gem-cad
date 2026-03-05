import cadquery as cq

outer = 20.0
thickness = 1.0
inner = outer - 2*thickness
tube_len = 100.0
cap_len = 20.0

# Create hollow tube
outer_tube = cq.Workplane("XY").rect(outer, outer).extrude(tube_len)
inner_tube = cq.Workplane("XY").rect(inner, inner).extrude(tube_len)
tube = outer_tube.cut(inner_tube)

# Create hollow end cap
cap = (
    cq.Workplane("XY")
    .box(outer, outer, cap_len)
    .faces(">Z").workplane()
    .rect(inner, inner)
    .cutBlind(cap_len)
)

# Position end caps
cap_front = cap.translate((0, 0, tube_len + cap_len/2))
cap_back = cap.translate((0, 0, -cap_len/2))

# Combine everything
result = tube.union(cap_front).union(cap_back)