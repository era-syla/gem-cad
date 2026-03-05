import cadquery as cq

# Parametric dimensions
length = 600.0      # Total length of the plate
height = 150.0      # Total height of the plate
thickness = 6.0     # Thickness of the material
hole_diameter = 8.0 # Diameter of the mounting holes
num_holes = 5       # Total number of holes
margin_top = 12.0   # Distance from hole center to top edge
margin_side = 20.0  # Distance from hole center to side edges

# Calculate hole coordinates
# The plate is centered at (0,0,0)
# Y position relative to the center of the face
y_pos = (height / 2.0) - margin_top

# X positions for evenly spaced holes
start_x = -(length / 2.0) + margin_side
end_x = (length / 2.0) - margin_side

hole_points = []
if num_holes > 1:
    step = (end_x - start_x) / (num_holes - 1)
    for i in range(num_holes):
        hole_points.append((start_x + i * step, y_pos))
else:
    hole_points.append((0, y_pos))

# Create the 3D model
# Used XZ plane to orient the plate vertically as shown in the image
result = (
    cq.Workplane("XZ")
    .box(length, height, thickness)
    .faces(">Y")  # Select the front face (normal to Y axis)
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)