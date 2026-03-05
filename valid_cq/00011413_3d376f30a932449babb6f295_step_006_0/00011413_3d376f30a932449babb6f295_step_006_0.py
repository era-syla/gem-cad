import cadquery as cq
import math

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------
thickness = 15.0         # Thickness of the plate
width = 40.0             # Width of the flange face
inner_radius = 80.0      # Inner radius of the arch
leg_height = 80.0        # Length of the straight vertical legs
hole_diameter = 10.0     # Diameter of the mounting holes
num_arc_holes = 6        # Number of holes on the curved section
leg_hole_margin = 20.0   # Distance of leg holes from the bottom edge

# Derived Dimensions
outer_radius = inner_radius + width
pitch_radius = (inner_radius + outer_radius) / 2.0

# ------------------------------------------------------------------------------
# Hole Calculation
# ------------------------------------------------------------------------------
hole_points = []

# 1. Calculate positions for holes on the vertical legs
# Located at the center of the width, offset from the bottom
hole_points.append((pitch_radius, -leg_height + leg_hole_margin))   # Right leg
hole_points.append((-pitch_radius, -leg_height + leg_hole_margin))  # Left leg

# 2. Calculate positions for holes on the semi-circular arc
# Distribute holes evenly over the 180-degree arch centered at (0,0)
# For 6 holes, the spacing is 30 degrees, starting at 15 degrees.
angle_step = 180.0 / num_arc_holes
start_angle = angle_step / 2.0

for i in range(num_arc_holes):
    angle_deg = start_angle + (i * angle_step)
    angle_rad = math.radians(angle_deg)
    
    # Polar to Cartesian conversion
    hx = pitch_radius * math.cos(angle_rad)
    hy = pitch_radius * math.sin(angle_rad)
    hole_points.append((hx, hy))

# ------------------------------------------------------------------------------
# Geometry Construction
# ------------------------------------------------------------------------------

# Create the main profile outline and extrude
# Path follows: Inner Leg Right -> Outer Leg Right -> Outer Arc -> Outer Leg Left 
#               -> Inner Leg Left -> Inner Arc -> Close
result = (
    cq.Workplane("XY")
    .moveTo(inner_radius, -leg_height)
    .lineTo(outer_radius, -leg_height)
    .lineTo(outer_radius, 0)
    .threePointArc((0, outer_radius), (-outer_radius, 0))
    .lineTo(-outer_radius, -leg_height)
    .lineTo(-inner_radius, -leg_height)
    .lineTo(-inner_radius, 0)
    .threePointArc((0, inner_radius), (inner_radius, 0))
    .close()
    .extrude(thickness)
)

# Cut the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)