import cadquery as cq
import math

# Parametric dimensions
head_diameter = 22.0    # Diameter of the wide top of the head
shaft_diameter = 10.0   # Diameter of the cylindrical shaft
shaft_length = 40.0     # Length of the cylindrical section
head_angle = 90.0       # Included angle of the countersink (degrees)
end_chamfer = 1.0       # Size of the chamfer at the tip

# Derived dimensions
head_radius = head_diameter / 2.0
shaft_radius = shaft_diameter / 2.0
# Calculate head height based on the countersink angle
# tan(angle/2) = (Head_Radius - Shaft_Radius) / Head_Height
angle_rad = math.radians(head_angle / 2.0)
head_height = (head_radius - shaft_radius) / math.tan(angle_rad)

# Generate the geometry
# 1. Create the Countersunk Head (Loft from top diameter to shaft diameter)
result = (
    cq.Workplane("XY")
    .circle(head_radius)
    .workplane(offset=-head_height)
    .circle(shaft_radius)
    .loft(combine=True)
)

# 2. Create the Cylindrical Shaft
# Select the bottom face of the head and extrude downwards
result = (
    result
    .faces("<Z")
    .workplane()
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# 3. Apply Chamfer to the end of the shaft
# Select the bottom-most face, get its edges, and apply chamfer
result = (
    result
    .faces("<Z")
    .edges()
    .chamfer(end_chamfer)
)