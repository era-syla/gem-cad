import cadquery as cq

# Parametric dimensions based on visual estimation of the image
diameter = 50.0
height = 10.0

# Create the cylindrical disc
# - Start a workplane on the XY plane
# - Draw a circle with the specified radius
# - Extrude to the specified height
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(height)