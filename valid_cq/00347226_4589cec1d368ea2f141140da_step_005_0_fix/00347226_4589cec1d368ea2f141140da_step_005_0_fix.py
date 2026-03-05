import cadquery as cq

handle = cq.Workplane("XY").circle(8).extrude(100)
for x in [10,20,30,40,50,60,70,80]:
    handle = handle.cut(
        cq.Workplane("XY").circle(7).extrude(2).translate((0,0,x-1))
    )

guard = cq.Workplane("XY").box(4,20,6).translate((102,0,0))

ring = cq.Workplane("YZ").workplane(offset=100).moveTo(0,12).circle(2).revolve(360, (0,0,0), (1,0,0))

blade = cq.Workplane("XZ").polyline([
    (0,-1.5),
    (100,-1.5),
    (106,0),
    (100,1.5),
    (0,1.5)
]).close().extrude(4).translate((104,-2,0))

for x in [20,30,40,50,60,70,80]:
    blade = blade.cut(
        cq.Workplane("XY").box(2,4,1).translate((104+x,0,1.0))
    )

blade = blade.cut(
    cq.Workplane("XY").box(4,4,3).translate((174,0,0))
)

result = handle.union(guard).union(ring).union(blade)