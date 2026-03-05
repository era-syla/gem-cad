import cadquery as cq

# Parameters
L_rod = 60
rod_d = 3
flange_d = 40
flange_t = 5
col_d = 12
col_h = 25
boss1_d = 8
boss1_h = 8
boss2_d = 5
boss2_h = 4
hole_d = 3

# Build geometry
result = cq.Workplane("XY").circle(rod_d/2).extrude(L_rod)
result = result.faces(">Z").workplane().circle(flange_d/2).extrude(flange_t)
result = result.faces(">Z").workplane().circle(col_d/2).extrude(col_h)
result = result.faces(">Z").workplane().circle(boss1_d/2).extrude(boss1_h)
result = result.faces(">Z").workplane().circle(boss2_d/2).extrude(boss2_h)
result = result.faces(">Z").workplane().hole(hole_d)