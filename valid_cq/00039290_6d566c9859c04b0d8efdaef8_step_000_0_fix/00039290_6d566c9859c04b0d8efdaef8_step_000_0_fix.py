import cadquery as cq

step = 10
width = 60
height = 30

base = cq.Workplane("XY").box(width, step * 5, height)

cutout = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .center(-width/2, 0)
    .rect(width, step)
    .extrude(height, combine=False)
)

cuts = base.faces(">Z").rect(width, step).cutThruAll()

result = base.cut(cutout).cut(cuts)