import cadquery as cq

t = 4

# Prongs
prong1 = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (60, 0), (100, 20), (105, 30), (100, 35), (50, 40), (0, 40)])
    .close()
    .extrude(t)
)
prong2 = prong1.mirror("XZ")
prongs = prong1.union(prong2)

# Pivot block
block = cq.Workplane("XY").workplane(offset=5).box(10, 12, 10)
# Holes for pivot pin
holes = (
    cq.Workplane("XZ")
    .workplane(offset=5)
    .pushPoints([(-4, 0), (4, 0)])
    .circle(2)
    .extrude(12)
)
block = block.cut(holes)

# Shaft
shaft = cq.Workplane("XY").workplane(offset=10).circle(3).extrude(60)

# Top bracket plates
flange1 = cq.Workplane("XY").workplane(offset=70).center(0, 5).box(12, 2, 8)
flange2 = cq.Workplane("XY").workplane(offset=70).center(0, -5).box(12, 2, 8)

# Hinge pin
pin = (
    cq.Workplane("XZ")
    .workplane(offset=70)
    .circle(1.5)
    .extrude(6, both=True)
)

# Combine all
result = prongs.union(block).union(shaft).union(flange1).union(flange2).union(pin)