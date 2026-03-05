import cadquery as cq

# Bottom bracket spindle
spindle = cq.Workplane("XY").circle(12.5).extrude(80)

# Crank arm profile and extrusion
crank_profile = [(0, 0), (150, 0), (200, 20), (180, 40), (20, 40)]
crank = (
    cq.Workplane("XY")
    .polyline(crank_profile)
    .close()
    .extrude(15)
    .translate((0, 0, 40))
)

# Function to create a simple chainring with rectangular teeth
def make_chainring(teeth, r_inner, r_outer, thickness):
    ring = cq.Workplane("XY").circle(r_outer).circle(r_inner).extrude(thickness)
    # single tooth
    tooth = (
        cq.Workplane("XY")
        .box(2, thickness, 5)
        .translate((r_outer + 2.5, 0, thickness / 2))
    )
    # replicate teeth around the ring
    for i in range(teeth):
        ring = ring.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * (360.0 / teeth)))
    return ring

# Three chainrings of different sizes
chain1 = make_chainring(30, 60, 70, 5)
chain2 = make_chainring(40, 80, 90, 5)
chain3 = make_chainring(50, 100, 110, 5)
chainset = (chain1.union(chain2).union(chain3)).translate((0, 0, 50))

# Assemble crankset
crankset = spindle.union(crank).union(chainset)

# Pedal assembly (simple platform pedal)
axle = cq.Workplane("XY").circle(8).extrude(60)

plate1 = (
    cq.Workplane("XY")
    .box(70, 100, 5)
    .translate((0, 15, 20))
    .faces(">Z")
    .workplane()
    .rect(40, 60)
    .cutThruAll()
)

plate2 = (
    cq.Workplane("XY")
    .box(70, 100, 5)
    .translate((0, -15, 20))
    .faces(">Z")
    .workplane()
    .rect(40, 60)
    .cutThruAll()
)

pedal = axle.union(plate1).union(plate2)

# Position pedal next to the crankset
result = crankset.union(pedal.translate((-200, 0, 0)))