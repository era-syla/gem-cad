import cadquery as cq

# Base block
result = cq.Workplane("XY").box(140, 20, 10)

# Half‐cylindrical cavity in the middle
cav1 = cq.Workplane("YZ", origin=(0, 0, 10)).cylinder(80, 7)
result = result.cut(cav1)

# Rectangular slot toward the right end
result = result.faces(">Z").workplane().center(45, 0).rect(4, 1.5).cutBlind(-3)

# Tool‐shaped cavity on the left end
cav2 = (
    cq.Workplane("YZ", origin=(-60, 0, 10))
    .circle(2).extrude(6)                    # small tip
    .workplane(offset=6).circle(4).extrude(30)  # main shaft
    .workplane(offset=36).circle(6).extrude(4)  # larger boss
)
result = result.cut(cav2)