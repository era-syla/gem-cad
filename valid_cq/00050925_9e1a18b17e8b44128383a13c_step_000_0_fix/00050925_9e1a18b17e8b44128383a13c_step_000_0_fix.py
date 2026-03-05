import cadquery as cq

# Base plate with half-circle extension
plate = cq.Workplane("XY").rect(40, 20).extrude(5)
half_circle = cq.Workplane("XY").circle(10).translate((20, 0, 0)).extrude(5)
base = plate.union(half_circle)

# Cylindrical boss under the half-circle
boss = cq.Workplane("XY").workplane(offset=-10).circle(15).translate((20, 0, 0)).extrude(10)

# Side cylinder on the left of the rectangle
side_cyl = cq.Workplane("XY").circle(5).translate((-20, 0, 0)).extrude(5)

# Two posts at front corners
post1 = cq.Workplane("XY").circle(2.5).translate((-20, -10, 0)).extrude(8)
post2 = cq.Workplane("XY").circle(2.5).translate((20, -10, 0)).extrude(8)

# Pin on top of the plate
pin = cq.Workplane("XY").circle(1).extrude(4)

# U-shaped clamp (ring minus two wedges)
clamp_outer = cq.Workplane("XY").center(-50, 0).circle(17).extrude(5)
clamp = clamp_outer.faces(">Z").shell(-2)
cut1 = cq.Workplane("XY").center(-50, 0).box(30, 50, 10).rotate((0, 0, 0), (0, 0, 1), 60)
cut2 = cq.Workplane("XY").center(-50, 0).box(30, 50, 10).rotate((0, 0, 0), (0, 0, 1), -60)
clamp = clamp.cut(cut1).cut(cut2)

# Separate cylinder piece
cylinder2 = cq.Workplane("XY").circle(6).translate((25, 0, 0)).extrude(5)

# Small cross-shaped connector
connector = cq.Workplane("XY").center(40, 0).box(10, 3, 3).union(
    cq.Workplane("XY").center(40, 0).box(3, 10, 3)
)

# Combine all parts
result = base.union(boss).union(side_cyl).union(post1).union(post2).union(pin).union(clamp).union(cylinder2).union(connector)