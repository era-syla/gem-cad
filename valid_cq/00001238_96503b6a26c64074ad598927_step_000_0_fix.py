import cadquery as cq

# Base disk
base = cq.Workplane("XY").circle(22).extrude(2)

# Add notches cut from edge of base disk (4 notches at 90 degree intervals)
notch_offset = 22
base = (base
    .workplane(offset=0)
    .transformed(offset=(notch_offset, 0, 0))
    .rect(4, 4)
    .cutBlind(-2)
)
base = (base
    .workplane(offset=0)
    .transformed(offset=(-notch_offset, 0, 0))
    .rect(4, 4)
    .cutBlind(-2)
)
base = (base
    .workplane(offset=0)
    .transformed(offset=(0, notch_offset, 0))
    .rect(4, 4)
    .cutBlind(-2)
)
base = (base
    .workplane(offset=0)
    .transformed(offset=(0, -notch_offset, 0))
    .rect(4, 4)
    .cutBlind(-2)
)

# Central raised hub
hub = cq.Workplane("XY").workplane(offset=2).circle(11).extrude(5)

# Cut a ring groove in the hub (annular groove)
hub_with_groove = (hub
    .workplane(offset=0)
    .circle(11)
    .circle(9)
    .cutBlind(-2)
)

# Actually, let's build hub as a solid cylinder and cut features
hub2 = cq.Workplane("XY").workplane(offset=2).circle(11).extrude(5)

# Cut center hole
hub2 = hub2.workplane(offset=7).circle(2.5).cutBlind(-5)

# Cut two circular holes (left and right of center)
hub2 = (hub2
    .workplane(offset=2)
    .center(-5.5, 0)
    .circle(2)
    .cutBlind(-7)
)

# Cut rectangular slots (top and bottom)
hub2 = (hub2
    .workplane(offset=2)
    .center(5.5, 0)
    .rect(3, 3)
    .cutBlind(-3)
)

hub2 = (hub2
    .workplane(offset=2)
    .center(0, 5.5)
    .rect(3, 3)
    .cutBlind(-3)
)

hub2 = (hub2
    .workplane(offset=2)
    .center(0, -5.5)
    .rect(3, 3)
    .cutBlind(-3)
)

# Cut a cross-shaped slot through the hub
hub2 = (hub2
    .workplane(offset=7)
    .rect(14, 3)
    .cutBlind(-5)
)
hub2 = (hub2
    .workplane(offset=7)
    .rect(3, 14)
    .cutBlind(-5)
)

# Add annular step/groove around base of hub
# Cut ring channel at base of hub
hub2 = (hub2
    .workplane(offset=2)
    .circle(11)
    .circle(8.5)
    .cutBlind(-1.5)
)

# Combine base and hub
result = base.union(hub2)

# Cut notches from the outer edge of the base disk
result = (result
    .workplane(offset=0)
    .transformed(offset=(22, 0, 0))
    .rect(5, 5)
    .cutBlind(-2)
)
result = (result
    .workplane(offset=0)
    .transformed(offset=(-22, 0, 0))
    .rect(5, 5)
    .cutBlind(-2)
)
result = (result
    .workplane(offset=0)
    .transformed(offset=(0, 22, 0))
    .rect(5, 5)
    .cutBlind(-2)
)
result = (result
    .workplane(offset=0)
    .transformed(offset=(0, -22, 0))
    .rect(5, 5)
    .cutBlind(-2)
)