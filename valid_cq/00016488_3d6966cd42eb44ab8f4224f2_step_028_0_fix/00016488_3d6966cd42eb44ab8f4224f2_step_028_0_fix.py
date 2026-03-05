import cadquery as cq

# Create head and shaft
result = (
    cq.Workplane("XY")
    .circle(10)        # head radius 10
    .extrude(4)        # head thickness 4
    .faces("<Z")       # select bottom face of head
    .workplane()
    .circle(3)         # shaft radius 3
    .extrude(-30)      # shaft length 30 downward
)

# Cut radial slot in head
slot_cut = (
    cq.Workplane("XY")
    .box(3, 20, 4)     # box to cut slot: dx=3, dy=20, dz=4
    .translate((8.5, 0, 2))  # move to intersect head side at mid-height
)
result = result.cut(slot_cut)

# Cut circumferential groove in head
groove_cut = (
    cq.Workplane("XZ", origin=(0, 0, 3.5))  # sketch in XZ plane at Z=3.5
    .moveTo(9.5, 0)        # move to radius 9.5
    .rect(1, 0.5)         # rectangle width=1 (radial), height=0.5 (axial)
    .revolve(360, (0, 0, 0), (0, 0, 1))  # revolve around Z axis
)
result = result.cut(groove_cut)