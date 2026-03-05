import cadquery as cq

# Base vertical cylinder
cyl = cq.Workplane("XY").circle(25).extrude(70)

# Left vertical mounting plate
left_plate = cq.Workplane("XY").center(-27, 0).box(6, 80, 70, centered=(True, True, False))

# Right horizontal mounting tab
right_tab = cq.Workplane("XY").center(32.5, 0).box(25, 30, 10, centered=(True, True, False))

# Combine the main bodies
result = cyl.union(left_plate).union(right_tab)

# Inner circular hole (cut through all)
result = result.faces(">Z").workplane().circle(20).cutThruAll()

# Add the flat inner wall on the left side (creates the D-shape hole)
# Create a full solid cylinder, then cut away the right portion
fill_solid = cq.Workplane("XY").circle(25).extrude(70)
cut_right = cq.Workplane("XY").center(25, 0).box(70, 70, 70, centered=(True, True, False))
fill_solid = fill_solid.cut(cut_right)
result = result.union(fill_solid)

# Add fillet to the right tab where it meets the main cylinder
# Bounding box targets the specific intersection arc on the top face of the tab
result = result.edges(cq.selectors.BoxSelector((19, -16, 9), (26, 16, 11))).fillet(8)

# Bottom archway cut (cylindrical cut along the Y axis)
archway = cq.Workplane("XZ").circle(20).extrude(100, both=True)
result = result.cut(archway)

# Right tab mounting hole
hole_cut = cq.Workplane("XY").center(38, 0).circle(3.5).extrude(20)
result = result.cut(hole_cut)