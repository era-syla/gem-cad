import cadquery as cq

# Parameters
base_d = 10
base_h = 12
rod_d = 4
rod_h = 80
tab_w = 4
tab_d = 2
tab_h = 5

# Create base and rod
base_and_rod = (
    cq.Workplane("XY")
    .circle(base_d / 2)
    .extrude(base_h)
    .faces(">Z")
    .circle(rod_d / 2)
    .extrude(rod_h)
)

# Create tab on side of base
tab = (
    cq.Workplane("XY", origin=(0, 0, base_h))
    .center(0, base_d / 2 - tab_d / 2)
    .rect(tab_w, tab_d)
    .extrude(tab_h)
)

# Combine into final result
result = base_and_rod.union(tab)