import cadquery as cq

# Parameters
module = 5.0
num_teeth = 40
length = module * num_teeth
base_thickness = 2.0
tooth_height = 3.0
width = 10.0

# Build 2D profile in the X-Z plane
points = [(0, base_thickness)]
for i in range(num_teeth):
    points.append((i*module + module/2, base_thickness + tooth_height))
    points.append(((i+1)*module, base_thickness))
points.append((length, 0))
points.append((0, 0))

# Extrude profile to create the 3D rack
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(width)
)