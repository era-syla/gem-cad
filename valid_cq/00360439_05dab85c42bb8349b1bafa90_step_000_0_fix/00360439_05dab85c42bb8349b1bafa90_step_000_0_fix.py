import cadquery as cq

# Create the base block
base = cq.Workplane("XY").box(50, 25, 5)

# Create the curved structure on top of the base
curved_structure = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .rect(50, 10)
    .extrude(15)
    .edges(">Y")
    .fillet(5)
)

# Create the circular end
circular_end = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .center(-20, 10)
    .circle(10)
    .extrude(5)
)

# Union all parts together
result = base.union(curved_structure).union(circular_end)