import cadquery as cq
import math

# --- Parameter Definitions ---
# Main body dimensions
diameter = 100.0        # Overall diameter of the disk
thickness = 30.0        # Height of the cylinder
fillet_radius = 2.0     # Radius of the top edge fillet

# Hole pattern parameters
hole_pairs = 8          # Number of pairs of holes around the circumference
hole_radius = 2.5       # Radius of the small holes
# We need two concentric circles of holes or paired radial holes.
# Looking at the image, it looks like pairs of holes aligned radially.
outer_hole_bcd = 85.0   # Bolt Circle Diameter for the outer hole of the pair
inner_hole_bcd = 70.0   # Bolt Circle Diameter for the inner hole of the pair
hole_depth = 10.0       # Depth of the holes (assuming blind, based on shading)
countersink_angle = 90.0 # Angle for countersink
countersink_dia = 5.0   # Diameter of the countersink opening

# --- Geometry Construction ---

# 1. Create the base cylinder
base = cq.Workplane("XY").circle(diameter / 2).extrude(thickness)

# 2. Add the top edge fillet
# We select edges on the top face (Z max)
base = base.edges(">Z").fillet(fillet_radius)

# 3. Create the hole pattern
# The pattern consists of 8 pairs. Each pair has an inner and an outer hole.
# We will create a list of points for the centers of these holes.

hole_centers = []
angle_step = 360.0 / hole_pairs

for i in range(hole_pairs):
    angle_rad = math.radians(i * angle_step)
    
    # Calculate position for outer hole
    outer_x = (outer_hole_bcd / 2) * math.cos(angle_rad)
    outer_y = (outer_hole_bcd / 2) * math.sin(angle_rad)
    hole_centers.append((outer_x, outer_y))
    
    # Calculate position for inner hole
    inner_x = (inner_hole_bcd / 2) * math.cos(angle_rad)
    inner_y = (inner_hole_bcd / 2) * math.sin(angle_rad)
    hole_centers.append((inner_x, inner_y))

# 4. Drill the holes
# We use the hole centers on the top face to create countersunk holes.
result = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_centers)
    .cskHole(diameter=hole_radius * 2, cskDiameter=countersink_dia, cskAngle=countersink_angle, depth=hole_depth)
)

# If the holes need to be through-holes instead, simply use .cskHole with depth=None or thickness
# But looking at the image, the shading inside suggests blind holes or specific inserts.
# The code above uses a finite depth. For through holes, remove the 'depth' argument.