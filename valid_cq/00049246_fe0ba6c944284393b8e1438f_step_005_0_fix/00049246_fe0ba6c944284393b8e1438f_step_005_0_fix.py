import cadquery as cq
import math

# Parameters
R = 20          # outer radius of clamp
innerR = 13     # inner radius (tube clearance)
t = 5           # thickness
tabDepth = 20   # how far the tab extends from the clamp face
tabWidth = 12   # width of the tab in the Y direction
baseHoleDia = 5
tabHoleDia = 10

# Create the base semicircular clamp
base = cq.Workplane("XY").circle(R).extrude(t)
# Cut away the right half to make it a semicircle with flat face at x=0
base = base.cut(
    cq.Workplane("XY")
      .box(R + 2, 2 * R + 2, 2 * t + 2)
      .translate((R/2, 0, t))
)
# Subtract inner cylinder to make the U-shape
base = base.cut(
    cq.Workplane("XY")
      .circle(innerR)
      .extrude(t)
)

# Add mounting holes on the curved part of the base
holeRadiusPos = R - 5
angles = [120, 180, 240]  # degrees around the semicircle
for a in angles:
    x = holeRadiusPos * math.cos(math.radians(a))
    y = holeRadiusPos * math.sin(math.radians(a))
    base = base.faces(">Z").workplane().pushPoints([(x, y)]).hole(baseHoleDia)

# Create the flat mounting tab
tab = (
    cq.Workplane("XY")
      .workplane(offset=t)              # start at top of the base
      .center(tabDepth/2, 0)            # move right so the tab starts at x=0
      .rect(tabDepth, tabWidth)
      .extrude(t)                       # extrude upward
)
# Add a hole in the tab
tab = tab.faces(">Z").workplane().hole(tabHoleDia)

# Combine base and tab
result = base.union(tab)