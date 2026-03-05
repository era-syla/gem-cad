import cadquery as cq
import math

# Parameters
R = 100.0                # Bend radius
angle_deg = 30.0         # Bend angle in degrees
outer_radius = 20.0      # Outer radius of tube
thickness = 2.0          # Wall thickness
inner_radius = outer_radius - thickness

# Compute arc points in XZ-plane
angle = math.radians(angle_deg)
p0 = (0.0, 0.0)
p_mid = (R * math.sin(angle / 2), R * (1 - math.cos(angle / 2)))
p_end = (R * math.sin(angle), R * (1 - math.cos(angle)))

# Create the arc path
path = (
    cq.Workplane("XZ")
      .moveTo(p0[0], p0[1])
      .threePointArc(p_mid, p_end)
      .wire()
)

# Create the tube profile on the YZ-plane (normal = X axis)
profile = (
    cq.Workplane("YZ")
      .circle(outer_radius)
      .circle(inner_radius)
)

# Sweep the profile along the path to create the hollow bent tube
result = profile.sweep(path, isFrenet=True)