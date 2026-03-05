import cadquery as cq

R_outer = 10
R_inner = 5
thickness = 5

c1 = cq.Vector(-30, 30, 0)
c2 = cq.Vector(30, -30, 0)

# define a smooth S-shaped path between the two circle centers
path = cq.Workplane("XY").spline([c1, cq.Vector(0, 0, 0), c2]).wire().val()

# sweep a flat bar (width = 2*R_outer, thickness) along the path
connector = cq.Workplane("XY").rect(2 * R_outer, thickness).sweep(path)

# create end plates as extruded circles
plate1 = cq.Workplane("XY").center(c1.x, c1.y).circle(R_outer).extrude(thickness)
plate2 = cq.Workplane("XY").center(c2.x, c2.y).circle(R_outer).extrude(thickness)

# combine connector and plates
result = connector.union(plate1).union(plate2)

# drill through-holes in each plate
result = result.faces(">Z").workplane().center(c1.x, c1.y).hole(2 * R_inner, thickness)
result = result.faces(">Z").workplane().center(c2.x, c2.y).hole(2 * R_inner, thickness)