import cadquery as cq

# Define parametric dimensions
diameter = 20.0
length = 60.0

# Create the cylinder by drawing a circle on the XY plane and extruding it
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)