import cadquery as cq

base = cq.Workplane("XY").rect(100, 100).extrude(10).edges("|Z").fillet(5)
shelf = cq.Workplane("XY").transformed(offset=(0, 0, 30)).rect(100, 90).extrude(10)
back = cq.Workplane("YZ").transformed(offset=(50, 0, 25)).rect(20, 60).extrude(10)
holes = back.faces(">X").workplane().rarray(80, 40, 2, 1).hole(5)

result = base.union(shelf).union(back).cut(holes)