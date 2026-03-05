import cadquery as cq

# Parameters for the hinge leaf
length = 90.0        # Length along the hinge axis
width = 50.0         # Width of the plate
thickness = 4.0      # Thickness of the plate
barrel_od = 12.0     # Outer diameter of the hinge barrel
barrel_id = 6.0      # Inner diameter of the hinge barrel (pin hole)
fillet_radius = 4.0  # Radius of the fillet between barrel and plate

# Hole parameters
hole_spacing_x = 55.0 # Distance between hole centers
hole_pos_y = 30.0     # Distance from hinge center axis to holes
hole_diameter = 6.0
csk_diameter = 12.0   # Countersink diameter
csk_angle = 90.0

# 1. Create the Hinge Barrel
# Cylinder oriented along the X-axis
# Positioned so its bottom tangent aligns with Z=0 (approximate)
# Center of barrel is at Z = barrel_od / 2
barrel = (
    cq.Workplane("XY")
    .cylinder(length, barrel_od / 2.0, direct=(1, 0, 0))
    .translate((0, 0, barrel_od / 2.0))
)

# 2. Create the Flat Plate
# Box sized to dimensions
# Positioned to connect tangentially/intersect the barrel
# Starts from Y=0 (center of barrel) and extends to Y=width
plate = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .translate((0, width / 2.0, thickness / 2.0))
)

# 3. Combine Barrel and Plate
base = barrel.union(plate)

# 4. Add Fillet at the connection
# Calculate the approximate intersection point on the top surface
# Intersection Y is roughly where the flat top meets the cylinder curve
# Equation: y^2 + (z - R)^2 = R^2 at z = thickness
# y = sqrt(R^2 - (thickness - R)^2)
R = barrel_od / 2.0
intersect_y = (R**2 - (thickness - R)**2)**0.5
intersect_z = thickness

# Select the edge running along X at that intersection
base = base.edges(
    cq.selectors.NearestToPointSelector((0, intersect_y, intersect_z))
).fillet(fillet_radius)

# 5. Create Countersunk Holes
# We define points on the top face relative to the center
hole_points = [
    (-hole_spacing_x / 2.0, hole_pos_y),
    (hole_spacing_x / 2.0, hole_pos_y)
]

# Select top face and cut holes
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

# 6. Cut the Barrel Pin Hole
# Cut a cylinder through the entire length along the X-axis
result = (
    result
    .faces("<X")
    .workplane()
    .circle(barrel_id / 2.0)
    .cutThruAll()
)