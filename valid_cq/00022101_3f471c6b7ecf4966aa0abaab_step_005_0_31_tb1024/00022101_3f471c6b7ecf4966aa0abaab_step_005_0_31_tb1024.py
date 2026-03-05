import cadquery as cq

# Parameters
radius = 1.0
height = 100.0

# Create the 3D model
result = cq.Workplane("XY").circle(radius).extrude(height)