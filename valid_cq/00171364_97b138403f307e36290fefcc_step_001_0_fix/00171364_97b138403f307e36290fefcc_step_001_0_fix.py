import cadquery as cq

# Create the lower part with the hexagonal base
base = (
    cq.Workplane("XY")
    .polygon(6, 30)
    .extrude(20)
)

# Create the tapered section
tapered_section = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .circle(15)
    .workplane(offset=100)
    .circle(10)
    .loft(combine=True)
)

# Create the horizontal top cylinder
top_cylinder = (
    cq.Workplane("YZ")
    .workplane(offset=120)
    .circle(5)
    .extrude(40, combine=False)
    .translate((0, -20, 0))
)

# Union all parts
result = base.union(tapered_section).union(top_cylinder)