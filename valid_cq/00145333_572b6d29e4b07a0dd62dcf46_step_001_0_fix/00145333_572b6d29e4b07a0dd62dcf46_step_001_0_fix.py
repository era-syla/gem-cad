import cadquery as cq
import math

# Gear parameters
teeth = 32
module = 2.0
pressure_angle = 20.0  # degrees
thickness = 10.0       # gear thickness
bore_dia = 10.0        # central hole diameter
hub_dia = 20.0         # hub outer diameter
hub_length = 15.0      # hub length extending from gear

# Derived dimensions
pitch_dia = module * teeth
pitch_radius = pitch_dia / 2.0
base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
addendum = module
dedendum = 1.25 * module
outer_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum

# Function to generate involute points from base circle to outer circle
def involute_points(base_r, outer_r, num=20):
    theta_max = math.sqrt((outer_r**2 - base_r**2) / base_r**2)
    pts = []
    for i in range(num):
        t = theta_max * i / (num - 1)
        x = base_r * (math.cos(t) + t * math.sin(t))
        y = base_r * (math.sin(t) - t * math.cos(t))
        pts.append((x, y))
    return pts

# Build one tooth profile (2D)
half_tooth_angle = math.pi / (2*teeth)  # half tooth thickness angle at pitch circle
inv_pts = involute_points(base_radius, outer_radius, num=20)
# First flank: rotate involute back by half tooth angle
flank1 = []
for x, y in inv_pts:
    ang = math.atan2(y, x) - half_tooth_angle
    r = math.hypot(x, y)
    flank1.append((r*math.cos(ang), r*math.sin(ang)))
# Second flank: mirror and rotate forward
flank2 = []
for x, y in reversed(inv_pts):
    x_m, y_m = x, -y
    ang = math.atan2(y_m, x_m) + half_tooth_angle
    r = math.hypot(x_m, y_m)
    flank2.append((r*math.cos(ang), r*math.sin(ang)))
# Root intersection points
p1 = flank1[0]
theta1 = math.atan2(p1[1], p1[0])
root1 = (root_radius*math.cos(theta1), root_radius*math.sin(theta1))
p2 = flank2[-1]
theta2 = math.atan2(p2[1], p2[0])
root2 = (root_radius*math.cos(theta2), root_radius*math.sin(theta2))
# Complete profile
profile = [root1] + flank1 + flank2 + [root2]

# Create blank cylinder for gear body
gear = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# Create and place teeth by rotating a single tooth
tooth = cq.Workplane("XY").polyline(profile).close().extrude(thickness)
for i in range(teeth):
    angle = i * 360.0 / teeth
    gear = gear.union(tooth.rotate((0,0,0),(0,0,1),angle))

# Add hub cylinder on top of gear
hub = cq.Workplane("XY").circle(hub_dia/2).extrude(hub_length)
gear = gear.union(hub.translate((0, 0, thickness)))

# Drill through-hole
hole = cq.Workplane("XY").circle(bore_dia/2).extrude(thickness + hub_length)
result = gear.cut(hole)  # final geometry in 'result'