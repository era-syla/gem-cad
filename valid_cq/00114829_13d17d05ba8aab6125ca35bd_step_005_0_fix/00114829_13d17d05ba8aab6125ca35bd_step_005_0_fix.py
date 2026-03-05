import cadquery as cq
from math import sin, cos, radians

# Parameters
R = 50             # radius of main arc
band_w = 10        # band width
band_h = 4         # band thickness in Z
point_h = 75       # distance of bottom point from center
tab_w = 2          # tab width (radial direction)
tab_d = 4          # tab length (tangential direction)
tab_h = 3          # tab height above band
tab_count = 6      # number of tabs

# Build the band profile (inner wire)
wp = cq.Workplane("XY")
start_ang = -150
end_ang = 150
p1 = (R * cos(radians(start_ang)), R * sin(radians(start_ang)))
p2 = (R * cos(radians(end_ang)),   R * sin(radians(end_ang)))
wp = wp.moveTo(*p1)
wp = wp.threePointArc((0, R), p2)
wp = wp.lineTo(0, -point_h)
wp = wp.close()

# Offset to create band cross‐section and extrude
band = wp.offset2D(band_w).extrude(band_h)

# Create and union tabs
angles = [ start_ang + i * (end_ang - start_ang) / (tab_count - 1) for i in range(tab_count) ]
result = band
for ang in angles:
    rad = radians(ang)
    cx = (R - band_w/2) * cos(rad)
    cy = (R - band_w/2) * sin(rad)
    tab = (
        cq.Workplane("XY")
          .transformed(offset=(cx, cy, band_h), rotate=(0, 0, ang))
          .rect(tab_d, tab_w)
          .extrude(tab_h)
    )
    result = result.union(tab)