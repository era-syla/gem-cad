import cadquery as cq

base = cq.Workplane("XY").box(10, 10, 10)
path = cq.Workplane("XY").center(0, 0).move(0, 0).move(5, 0).threePointArc((7.5, 7.5), (10, 0))
sweep_shape = base.faces(">Z").workplane().move(2, 0).rect(2, 2).sweep(path)

result = base.union(sweep_shape)