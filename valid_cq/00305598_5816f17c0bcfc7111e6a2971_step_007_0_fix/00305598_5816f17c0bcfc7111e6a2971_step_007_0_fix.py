import cadquery as cq

# Shaft
shaft = cq.Workplane("YZ", origin=(-4, 0, 0)).circle(2).extrude(68)

# Base block
block = cq.Workplane("YZ", origin=(-8, 0, 0)).box(8, 20, 20)

# Pivot cylinder
pivot = cq.Workplane("YZ", origin=(-4, 0, 0)).circle(4).extrude(6)

# Arm plate
arm = (
    cq.Workplane("YZ", origin=(2, 0, 0))
    .rect(40, 8, centered=(False, True))
    .extrude(3)
    .faces("<X").workplane(centerOption="CenterOfBoundBox")
    .circle(4).cutThruAll()
    .faces(">X").workplane(centerOption="CenterOfBoundBox")
    .circle(4).cutThruAll()
)

# Flange at arm end
flange = cq.Workplane("YZ", origin=(5, 0, 0)).circle(8).extrude(5)

# Discs and spacers along shaft
disc1 = cq.Workplane("YZ", origin=(10, 0, 0)).circle(6).extrude(4)
spacer = cq.Workplane("YZ", origin=(16, 0, 0)).circle(3).extrude(2)
disc2 = cq.Workplane("YZ", origin=(20, 0, 0)).circle(5).extrude(3)
disc3 = cq.Workplane("YZ", origin=(25, 0, 0)).circle(7).extrude(3)
washer = (
    cq.Workplane("YZ", origin=(30, 0, 0))
    .circle(9).extrude(2)
    .faces(">X").workplane(centerOption="CenterOfBoundBox")
    .circle(3).cutThruAll()
)

# Combine all parts
result = (
    shaft
    .union(block)
    .union(pivot)
    .union(arm)
    .union(flange)
    .union(disc1)
    .union(spacer)
    .union(disc2)
    .union(disc3)
    .union(washer)
)