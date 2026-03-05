import cadquery as cq

# Parametric dimensions
head_radius = 5.0
head_length = 3.0
shaft_radius = 2.0
shaft_length = 12.0
tip_radius = 1.0
chamfer_length = 1.5

# Define the 2D profile points for the revolve operation
# The profile is created in the XY plane, to be revolved around the Y-axis
pts = [
    (0, 0),
    (head_radius, 0),
    (shaft_radius, head_length),
    (shaft_radius, head_length + shaft_length),
    (tip_radius, head_length + shaft_length + chamfer_length),
    (0, head_length + shaft_length + chamfer_length)
]

# Create the solid by revolving the profile 360 degrees around the Y-axis
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)