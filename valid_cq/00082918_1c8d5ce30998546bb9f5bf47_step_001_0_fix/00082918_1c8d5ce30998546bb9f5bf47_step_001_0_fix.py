import cadquery as cq
import math

R_outer = 50
R_inner = 45
thickness = 5
depth = 2
angleSpan = 120
theta = angleSpan/2
num_teeth = 6

# Outer arc points
p1 = (R_outer*math.cos(math.radians(-theta)), R_outer*math.sin(math.radians(-theta)))
pm = (R_outer, 0)
p2 = (R_outer*math.cos(math.radians(theta)), R_outer*math.sin(math.radians(theta)))

# Inner zigzag points
step = angleSpan/(num_teeth*2)
angles_inner = [ -theta + i*step for i in range(num_teeth*2+1) ]
inner_pts = []
for idx, a in enumerate(angles_inner):
    r = R_inner + (depth if idx % 2 == 0 else 0)
    inner_pts.append((r*math.cos(math.radians(a)), r*math.sin(math.radians(a))))

# Base ring with zigzag inner
profile = cq.Workplane("XY").moveTo(*p1).threePointArc(pm, p2).lineTo(*inner_pts[-1])
for pt in reversed(inner_pts[:-1]):
    profile = profile.lineTo(*pt)
base = profile.close().extrude(thickness)

# Platform at inner start
platform_radius = 6
platform_thickness = 2
plate = cq.Workplane("XY").workplane(offset=thickness).moveTo(*inner_pts[0]).circle(platform_radius).extrude(platform_thickness)

# Pin
pin_radius = 1.5
pin_height = 5
pin = cq.Workplane("XY").workplane(offset=thickness+platform_thickness).moveTo(*inner_pts[0]).circle(pin_radius).extrude(pin_height)

result = base.union(plate).union(pin)