import cadquery as cq

# Base box
base = cq.Workplane("XY").box(80, 80, 10)

# Walls
walls = (cq.Workplane("XY")
         .box(80, 80, 40)
         .cut(cq.Workplane("XY").box(76, 76, 40).translate((0, 0, 2))))

# Cutouts in walls
cutout = cq.Workplane("XY").box(5, 10, 2).translate((0, 34, 5))
walls = walls.cut(cutout)
walls = walls.cut(cutout.translate((0, -68, 0)))

# Combine base and walls
box = base.union(walls)

# Tab
tab = (cq.Workplane("XY")
       .rect(30, 5)
       .extrude(3)
       .edges("|Y")
       .fillet(1))
tab = tab.translate((0, 42.5, 6.5))
box = box.union(tab)

# Dividers
divider = cq.Workplane("XY").box(5, 10, 30).translate((0, 34, 15))
box = box.union(divider)
box = box.union(divider.translate((0, -68, 0)))

result = box.translate((0, 0, 5))