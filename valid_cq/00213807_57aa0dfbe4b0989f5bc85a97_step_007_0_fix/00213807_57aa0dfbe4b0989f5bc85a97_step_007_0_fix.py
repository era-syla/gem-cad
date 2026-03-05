import cadquery as cq
import math

rod_count = 12
rod_diameter = 1.0
rod_radius_from_center = 4.5
rod_height = 80.0
cap_diameter = 10.0
cap_height = 5.0

result = None
for i in range(rod_count):
    angle_deg = 360.0 / rod_count * i
    angle_rad = math.radians(angle_deg)
    x = rod_radius_from_center * math.cos(angle_rad)
    y = rod_radius_from_center * math.sin(angle_rad)
    rod = (
        cq.Workplane("XY")
          .transformed(offset=(x, y, 0))
          .circle(rod_diameter / 2)
          .extrude(rod_height)
    )
    result = rod if result is None else result.union(rod)

cap = (
    cq.Workplane("XY")
      .transformed(offset=(0, 0, rod_height))
      .circle(cap_diameter / 2)
      .extrude(cap_height)
)

result = result.union(cap)