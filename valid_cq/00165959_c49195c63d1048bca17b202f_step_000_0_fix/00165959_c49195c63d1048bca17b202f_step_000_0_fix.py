import cadquery as cq

# Parameters
D = 20.0        # cylinder diameter
H = 50.0        # cylinder height
slot_w = 8.0    # slot width
slot_d = 20.0   # slot depth
hole_d = 6.0    # side hole diameter
hole_z = H/2.0  # side hole vertical position

# Build base cylinder
result = cq.Workplane("XY").circle(D/2).extrude(H)

# Cut the U-shaped slot from the top
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(slot_w, D*2)
    .cutBlind(-slot_d)
)

# Cut the side hole through the cylinder
hole_cut = (
    cq.Workplane("YZ", origin=(0, 0, hole_z))
    .circle(hole_d/2)
    .extrude(D*2)
)
result = result.cut(hole_cut)