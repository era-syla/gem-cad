import cadquery as cq
import math

R = 15   # radius of large hole
r = 7    # radius of small hole
d = 60   # distance between hole centers
th = 8   # thickness of part

# compute tangent points
theta = math.acos((R - r)/d)
x1 = R * math.cos(theta)
y1 = R * math.sin(theta)
x4 = R * math.cos(-theta)
y4 = R * math.sin(-theta)
x2 = d + r * math.cos(theta)
y2 = r * math.sin(theta)
x3 = d + r * math.cos(-theta)
y3 = r * math.sin(-theta)

result = (
    cq.Workplane("XY")
      .moveTo(x1, y1)
      .threePointArc((0, R), (x4, y4))
      .lineTo(x3, y3)
      .threePointArc((d + r, 0), (x2, y2))
      .close()
      .extrude(th)
)