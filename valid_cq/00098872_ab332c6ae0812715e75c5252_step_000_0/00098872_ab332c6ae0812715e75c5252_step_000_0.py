import cadquery as cq

# Parameters for the plate geometry
plate_length = 140.0
plate_width = 100.0
plate_thickness = 5.0

# Parameters for the holes
hole_diameter = 6.0
hole_spacing = 50.0       # Distance between the two hole centers
hole_edge_offset = 30.0   # Distance from the near edge to the first hole center

# Calculate hole coordinates
# Assuming the plate is centered at (0,0), the near edge (along X) starts at -plate_length/2
x1 = -(plate_length / 2.0) + hole_edge_offset
x2 = x1 + hole_spacing

# Create the model
# 1. Create a base box centered on the XY plane
# 2. Select the top face (>Z)
# 3. Define the points for the holes along the centerline (y=0)
# 4. Cut the holes through the plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(x1, 0), (x2, 0)])
    .hole(hole_diameter)
)