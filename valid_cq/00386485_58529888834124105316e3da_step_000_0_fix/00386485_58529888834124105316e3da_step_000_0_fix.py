import cadquery as cq

# Base hexagon
base = cq.Workplane("XY").polygon(6, 60).extrude(5)

# Nut-shaped hexagon on top of base
nut = cq.Workplane("XY").workplane(offset=5).polygon(6, 30).extrude(5)

# Central pivot cylinder with a through hole
pivot = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .circle(10)
    .extrude(15)
    .faces(">Z")
    .hole(6)
)

# Top plate, rotated and positioned above the pivot
top_plate = (
    cq.Workplane("XY")
    .rect(80, 80)
    .extrude(5)
    .rotate((0, 0, 0), (0, 0, 1), 20)
    .translate((10, 0, 25))
)

# Lever arm intersecting the pivot
lever = (
    cq.Workplane("XY")
    .box(50, 5, 5)
    .translate((25, 0, 17.5))
)

# Side rod extending out from the pivot
rod = (
    cq.Workplane("XZ")
    .workplane(origin=(15, 0, 20))
    .circle(3)
    .extrude(60)
)

# Combine all parts into the final result
result = base.union(nut).union(pivot).union(top_plate).union(lever).union(rod)