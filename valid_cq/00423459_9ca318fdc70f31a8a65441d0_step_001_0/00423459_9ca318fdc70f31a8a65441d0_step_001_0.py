import cadquery as cq
import math

# Geometric Parameters
radius = 50.0          # Radius of the circular sectors
thickness = 5.0        # Thickness of the plate
sector_angle = 80.0    # Angle of the wedge (degrees)

# Helper calculations
half_angle_rad = math.radians(sector_angle / 2.0)

# Calculate key points for the right-side sector
# Center of the shape
pt_center = (0.0, 0.0)

# End points of the straight edges on the circumference
pt_upper = (radius * math.cos(half_angle_rad), radius * math.sin(half_angle_rad))
pt_lower = (radius * math.cos(-half_angle_rad), radius * math.sin(-half_angle_rad))

# Midpoint for the arc definition (on the X-axis)
pt_arc_mid = (radius, 0.0)

# Create the first sector (Right side)
# We draw the outline: Center -> Lower Edge -> Arc -> Upper Edge -> Center
sector_right = (
    cq.Workplane("XY")
    .moveTo(*pt_center)
    .lineTo(*pt_lower)
    .threePointArc(pt_arc_mid, pt_upper)
    .close()
    .extrude(thickness)
)

# Create the second sector (Left side) by rotating the first one 180 degrees
sector_left = sector_right.rotate((0, 0, 0), (0, 0, 1), 180)

# Combine the two sectors into the final result
result = sector_right.union(sector_left)