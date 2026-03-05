import cadquery as cq

# Parameters for the model
rod_length = 300.0
rod_diameter = 5.0
rod_spacing = 15.0
num_rods = 6

# Calculate coordinates to center the array of rods
# We arrange them spaced along the X-axis, centered at the origin
points = [
    ((i - (num_rods - 1) / 2) * rod_spacing, 0) 
    for i in range(num_rods)
]

# Create the geometry
# 1. Workplane("XZ") creates a sketch plane perpendicular to the Y-axis.
# 2. pushPoints(points) places the center of each rod.
# 3. circle() draws the cross-section of the rods.
# 4. extrude(..., both=True) creates the solid cylinders symmetric about the plane.
result = (
    cq.Workplane("XZ")
    .pushPoints(points)
    .circle(rod_diameter / 2.0)
    .extrude(rod_length / 2.0, both=True)
)