import cadquery as cq

# Parameters
lever_length = 60.0
lever_width = 15.0
lever_thickness = 5.0
boss_dia = 20.0
boss_height = 5.0
big_hole_dia = 12.0
small_hole_dia = 6.0

# Create boss cylinder
boss = cq.Workplane("XY").circle(boss_dia / 2).extrude(boss_height).translate((0, 0, -boss_height))

# Create lever body by union of two end-circles and a rectangle
c1 = cq.Workplane("XY").circle(lever_width / 2).extrude(lever_thickness)
c2 = cq.Workplane("XY").center(lever_length, 0).circle(lever_width / 2).extrude(lever_thickness)
rect = cq.Workplane("XY").center(lever_length / 2, 0).rect(lever_length, lever_width).extrude(lever_thickness)

lever = c1.union(c2).union(rect)

# Combine boss and lever
result = lever.union(boss)

# Drill holes
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(big_hole_dia)
    .center(lever_length, 0)
    .hole(small_hole_dia)
)

# 'result' now contains the final solid
