import cadquery as cq

# Create the base shape
base = cq.Workplane("XY").circle(15).extrude(3)

# Create the cutouts for the arms
for angle in [0, 120, 240]:
    base = base.faces(">Z").workplane().transformed(offset=(0,0,0), rotate=(0,0,angle)).rect(5, 20).cutThruAll()

# Create tabs on the base
tabs = (cq.Workplane("XY")
        .rect(30, 60)
        .extrude(2)
        .faces(">Z")
        .workplane()
        .rarray(30, 1, 2, 1)
        .circle(2.5)
        .cutThruAll()
        )

# Create the arms
arms = cq.Workplane("XZ").moveTo(20, 0).circle(2).extrude(60)

# Assemble the parts
result = base.union(tabs).union(arms)