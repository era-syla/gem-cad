import cadquery as cq

# Parameters
w = 20.0
h = 20.0
t = 1.8      # wall thickness
slotW = 6.0  # slot opening width
slotD = 6.0  # slot depth
length = 200.0
holeD = 6.0  # central hole diameter

# Outer extrusion
outer = cq.Workplane("XY").rect(w, h).extrude(length)

# Inner cut to make hollow profile
inner = (
    cq.Workplane("XY")
    .rect(w - 2 * t, h - 2 * t)
    .extrude(length + 2)
    .translate((0, 0, -1))
)
result = outer.cut(inner)

# Central through hole
result = result.faces(">Z").workplane().circle(holeD / 2).cutThruAll()

# Cut T-slots on each side
# +Y face
result = result.faces(">Y").workplane().rect(slotW, length).cutBlind(-slotD)
# -Y face
result = result.faces("<Y").workplane().rect(slotW, length).cutBlind(-slotD)
# +X face
result = result.faces(">X").workplane().rect(length, slotW).cutBlind(-slotD)
# -X face
result = result.faces("<X").workplane().rect(length, slotW).cutBlind(-slotD)