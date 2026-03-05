import cadquery as cq

# Parameters
outer_r = 8
inner_r = 4
base_h = 6

wing_w = 6
wing_l = 20
wing_h = base_h
mid_l = wing_l - wing_w

# Central nut body
base = (
    cq.Workplane("XY")
    .circle(outer_r)
    .extrude(base_h)
    .faces(">Z")
    .workplane()
    .circle(inner_r)
    .cutThruAll()
)

# Single wing profile
rect = (
    cq.Workplane("XY")
    .center(mid_l/2, 0)
    .rect(mid_l, wing_w)
    .extrude(wing_h)
)
circ = (
    cq.Workplane("XY")
    .center(mid_l + wing_w/2, 0)
    .circle(wing_w/2)
    .extrude(wing_h)
)
wing = rect.union(circ)

# Position and union two wings
wing1 = wing
wing2 = wing.rotate((0,0,0), (0,0,1), 180)
result = base.union(wing1).union(wing2)