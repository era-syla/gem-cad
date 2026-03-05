import cadquery as cq

# Parameters for the dimensions of the trapezoidal prism
length = 100.0      # Total length of the part
height = 15.0       # Height of the prism
top_width = 25.0    # Width of the top face
bottom_width = 15.0 # Width of the bottom face

# Define the points for the trapezoidal cross-section
# The profile is drawn on the YZ plane (Y is width, Z is height)
# Centered along the Y-axis for symmetry
points = [
    (-bottom_width / 2.0, 0.0),      # Bottom left corner
    (-top_width / 2.0, height),      # Top left corner
    (top_width / 2.0, height),       # Top right corner
    (bottom_width / 2.0, 0.0)        # Bottom right corner
]

# Create the solid geometry
# 1. Initialize a Workplane on the YZ plane
# 2. Draw the polyline using the defined points
# 3. Close the profile to form a face
# 4. Extrude the profile along the X axis to create the 3D shape
result = (
    cq.Workplane("YZ")
    .polyline(points)
    .close()
    .extrude(length)
)