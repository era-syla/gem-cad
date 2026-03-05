import cadquery as cq

# Parametric dimensions based on the visual aspect ratio of the line
height = 50.0
diameter = 1.0

# Create a vertical cylinder to represent the line as a solid object
# We use a thin cylinder to mimic the appearance of a line segment in 3D
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(height)
)