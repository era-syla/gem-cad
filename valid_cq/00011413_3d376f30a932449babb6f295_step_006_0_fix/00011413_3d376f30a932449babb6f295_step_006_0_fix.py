import cadquery as cq
import math

# Parameters
thickness = 10        # profile thickness in X direction
depth = 8             # extrusion depth (Y direction)
arc_radius = 50       # radius of the arch
leg_height = 20       # vertical height of the legs
hole_dia = 5          # diameter of all holes
num_arc_holes = 7     # number of holes along the arch

# Create the 2D profile in the XZ plane
profile = (
    cq.Workplane("XZ")
      .moveTo(-arc_radius, leg_height)
      .threePointArc(( arc_radius, leg_height), (0, leg_height+arc_radius))
      .lineTo( arc_radius, 0)
      .lineTo(-arc_radius, 0)
      .close()
)

# Extrude the profile in the Y direction
result = profile.extrude(depth)

# Compute hole positions along the arch
arc_hole_positions = []
for i in range(num_arc_holes):
    theta = math.pi - i * (math.pi / (num_arc_holes - 1))
    x = arc_radius * math.cos(theta)
    z = leg_height + arc_radius * math.sin(theta)
    arc_hole_positions.append((x, z))

# Add holes at the bottom of each leg
leg_hole_positions = [(-arc_radius, 0), (arc_radius, 0)]

# Drill all holes through the depth
all_hole_positions = arc_hole_positions + leg_hole_positions
result = result.faces(">Y").workplane().pushPoints(all_hole_positions).hole(hole_dia, depth)