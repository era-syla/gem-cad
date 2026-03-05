import cadquery as cq

# Parameters
length = 100.0
base_width = 20.0
base_thickness = 10.0
rib_count = 3
rib_width = 3.0
rib_depth = 5.0
top_overhang = 6.0  # total overhang on one side
top_thickness = 3.0

# Derived
top_width = base_width + top_overhang
spacing = (length - rib_count * rib_width) / (rib_count + 1)
rib_positions = [
    -length/2 + spacing*(i+1) + rib_width*i + rib_width/2
    for i in range(rib_count)
]

# Base block, bottom flush on Z=0
base = cq.Workplane("XY").box(length, base_width, base_thickness, centered=(True, True, False))

# Ribs on the +Y face of the base
ribs = base.faces(">Y").workplane()
for x in rib_positions:
    ribs = ribs.pushPoints([(x, 0)]).rect(rib_width, base_thickness).extrude(rib_depth)

# Top plate, overhanging on the negative Y side only
top = (
    cq.Workplane("XY")
    .transformed(offset=(0, -(top_width-base_width)/2, base_thickness))
    .box(length, top_width, top_thickness, centered=(True, True, False))
)

# Combine all parts
result = base.union(ribs).union(top)