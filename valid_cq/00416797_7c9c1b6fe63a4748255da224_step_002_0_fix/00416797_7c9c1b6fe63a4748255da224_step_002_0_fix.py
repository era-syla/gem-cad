import cadquery as cq
import math

R = 70
t = 5
h = 40
angle_deg = 120
start_angle = -angle_deg/2
end_angle = angle_deg/2

# Calculate arc points
p1 = (R * math.cos(math.radians(start_angle)), R * math.sin(math.radians(start_angle)))
p2 = (R * math.cos(math.radians(end_angle)),   R * math.sin(math.radians(end_angle)))
r2 = R - t
p3 = (r2 * math.cos(math.radians(end_angle)),  r2 * math.sin(math.radians(end_angle)))
p4 = (r2 * math.cos(math.radians(start_angle)),r2 * math.sin(math.radians(start_angle)))

# Create the curved shell profile
profile = (
    cq.Workplane("XY")
      .moveTo(*p1)
      .radiusArc(p2, R)
      .lineTo(*p3)
      .radiusArc(p4, r2)
      .close()
)

# Extrude to make the wall
result = profile.extrude(h)

# Create a notch and cut it out
notch_width = 15
notch_depth = t + 2
notch_height = 15
notch_angle = -40
cx = (r2 + t/2) * math.cos(math.radians(notch_angle))
cy = (r2 + t/2) * math.sin(math.radians(notch_angle))

notch = (
    cq.Workplane("XY")
      .transformed(offset=(cx, cy, 0))
      .box(notch_width, notch_depth, notch_height, centered=(True, True, False))
)

result = result.cut(notch)