import cadquery as cq

# Parameters
L = 100    # rod length
W = 10     # rod width
T = 4      # rod thickness

boss1_d = 16
boss1_t = 4

boss2_d = 12
boss2_t = 4

hole_d = 5

ear_y_thickness = 3
ear_height = 10

bush_outer = 8
bush_inner = 4
bush_h = 6

# Main rod
main = cq.Workplane("XY").rect(L, W).extrude(T)

# Left boss and hole
main = main.faces("<X").workplane().circle(boss1_d/2).extrude(boss1_t)
main = main.faces("<X").workplane().hole(hole_d)

# Right boss and hole
main = main.faces(">X").workplane().circle(boss2_d/2).extrude(boss2_t)
main = main.faces(">X").workplane().hole(hole_d)

# Right ears
for sign in (1, -1):
    offset_y = sign * (hole_d/2 + ear_y_thickness/2)
    main = main.faces(">X").workplane().center(0, offset_y).rect(ear_y_thickness, ear_height).extrude(boss2_t)

# Separate bush
bush = cq.Workplane("XY").center(0, 20).circle(bush_outer/2).extrude(bush_h)
bush = bush.faces(">Z").workplane().hole(bush_inner)

# Combine into final result
result = main.union(bush)