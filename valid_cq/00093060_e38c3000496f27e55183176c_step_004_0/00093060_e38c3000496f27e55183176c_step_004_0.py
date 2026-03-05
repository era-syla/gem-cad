import cadquery as cq

# Parametric dimensions for the plates
length = 20.0      # Length of the rectangular plate
width = 14.0       # Width of the rectangular plate
thickness = 1.0    # Thickness of the plate
offset_x = 15.0    # X-axis offset from center
offset_y = 12.0    # Y-axis offset from center

# Define the centers for the two disjoint plates
# Positioned diagonally from each other
points = [
    (-offset_x, -offset_y),
    (offset_x, offset_y)
]

# Create the model
# 1. Initialize workplane on XY plane
# 2. Push the two center points onto the stack
# 3. Create a rectangle at each point
# 4. Extrude the rectangles to create 3D solids
result = (
    cq.Workplane("XY")
    .pushPoints(points)
    .rect(length, width)
    .extrude(thickness)
)