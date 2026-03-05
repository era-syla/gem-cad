import cadquery as cq

# Parameter definitions
length = 100.0        # Total length of the plate
width = 25.0          # Width of the plate
thickness = 4.0       # Thickness of the plate
hole_dia = 5.0        # Diameter of the through-hole
csk_dia = 10.0        # Diameter of the countersink top
csk_angle = 90.0      # Angle of the countersink
num_holes = 4         # Number of holes

# Calculate hole spacing
# We assume equal spacing between holes, centered on the plate
# Distance from the edge to the center of the first/last hole
margin = width / 2.0 
# Distance between centers of adjacent holes
pitch = (length - 2 * margin) / (num_holes - 1)

# Calculate positions for the holes along the X axis
# The plate is centered at (0,0), so we generate points from left to right
hole_points = []
start_x = -(length / 2) + margin
for i in range(num_holes):
    hole_points.append((start_x + i * pitch, 0))

# Generate the CAD model
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(diameter=hole_dia, cskDiameter=csk_dia, cskAngle=csk_angle)
)