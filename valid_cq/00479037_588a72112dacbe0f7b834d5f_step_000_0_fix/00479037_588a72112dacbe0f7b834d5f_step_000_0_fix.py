import cadquery as cq

# Parameters
R = 10      # radius of end bosses
hole_d = 6  # diameter of holes
L = 50      # center-to-center distance between bosses
T = 10      # thickness of part

# Create the main body as a box spanning from X=0 to X=L, Y=-R to R, Z=0 to Z=T
body = cq.Workplane("XY").box(L, 2*R, T, centered=(False, True, False))

# Create the two end cylinders and union them with the body
c1 = cq.Workplane("XY").center(0, 0).circle(R).extrude(T)
c2 = cq.Workplane("XY").center(L, 0).circle(R).extrude(T)
combined = body.union(c1).union(c2)

# Drill holes through the thickness at the two boss centers
result = combined.faces(">Z").workplane().center(0, 0).hole(hole_d, T).center(L, 0).hole(hole_d, T)