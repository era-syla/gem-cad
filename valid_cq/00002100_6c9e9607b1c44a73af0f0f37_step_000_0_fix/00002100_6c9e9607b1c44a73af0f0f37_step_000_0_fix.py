import cadquery as cq
import math

# Parameters
W = 20          # outer width of tube
T = 2           # wall thickness
vlen = 60       # length of vertical tube
alen = 70       # length of angled tube
angle = 45      # angle of the angled tube from horizontal in degrees
d_hole = 6      # diameter of holes

# Precompute for triangular pocket
angle_rad = math.radians(angle)
y3 = alen * math.cos(angle_rad)
z3 = vlen - alen * math.sin(angle_rad)

# Vertical tube (hollow)
vert_outer = cq.Workplane("XY").box(W, W, vlen, centered=(True, True, False))
vert_inner = cq.Workplane("XY").box(W - 2 * T, W - 2 * T, vlen - 2 * T, centered=(True, True, False)).translate((0, 0, T))
vertical = vert_outer.cut(vert_inner)

# Angled tube (hollow), build along Y then rotate about X and translate up
ang_outer = cq.Workplane("XY").box(W, alen, W, centered=(True, False, True))
ang_inner = cq.Workplane("XY").box(W - 2 * T, alen - 2 * T, W - 2 * T, centered=(True, False, True)).translate((0, T, 0))
tubeAng = ang_outer.cut(ang_inner).rotate((0, 0, 0), (1, 0, 0), angle).translate((0, 0, vlen))

# Top cap on vertical tube with center hole
vertCap = cq.Workplane("XY", origin=(0, 0, vlen)).rect(W, W).extrude(T)
vertCap = vertCap.faces(">Z").workplane().hole(d_hole)

# End cap on angled tube with two holes
# Use ZX plane so normal is along Y; origin at the free end of the tube before rotation/translation
angCap = cq.Workplane("ZX", origin=(0, alen, 0)).rect(W, W).extrude(-T)
angCap = angCap.faces(">Y").workplane().pushPoints([(0, 10), (0, -10)]).hole(d_hole)

# Union all parts
result = vertical.union(tubeAng).union(vertCap).union(angCap)

# Triangular cutout/pocket between tubes
tri = cq.Workplane("YZ").polyline([(0, 0), (0, vlen), (y3, z3)]).close().extrude(W, both=True)
result = result.cut(tri)