import cadquery as cq

# Parameters
R = 10          # outer radius of the cylinder
L = 80          # length of the cylinder and wedge
W = 2 * R       # width of the part (full diameter)
H = 10          # front wedge thickness
t = 2           # wall thickness of the tube
slot_length = 4 # slot length along X
slot_height = 6 # slot height along Y

# Outer solid cylinder
outer_cyl = (
    cq.Workplane("YZ", origin=(0, 0, 0))
    .center(0, R)
    .circle(R)
    .extrude(L)
)

# Wedge support
wedge = (
    cq.Workplane("XY", origin=(0, 0, -W/2))
    .polyline([
        (0, 0),
        (L, 0),
        (L, -H),
        (0, -H)
    ])
    .close()
    .extrude(W)
)

# Union of cylinder and wedge
model = outer_cyl.union(wedge)

# Hollow out the cylinder
inner_cyl = (
    cq.Workplane("YZ", origin=(0, 0, 0))
    .center(0, R)
    .circle(R - t)
    .extrude(L)
)
model = model.cut(inner_cyl)

# Slot cut on top of the cylinder
slot = (
    cq.Workplane("XY", origin=(L/2, 2*R - slot_height/2, -W/2))
    .rect(slot_length, slot_height)
    .extrude(W)
)
model = model.cut(slot)

result = model