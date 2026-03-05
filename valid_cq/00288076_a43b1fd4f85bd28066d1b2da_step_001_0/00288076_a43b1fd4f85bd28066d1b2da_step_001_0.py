import cadquery as cq

# Parametric dimensions
length = 60.0
diameter = 20.0
radius = diameter / 2.0

# Create the cylinder by drawing a circle on the XY plane and extruding it
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)