import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the disc
thickness = 10.0 # Thickness (height) of the disc

# Create the cylinder
result = cq.Workplane("XY").circle(diameter / 2).extrude(thickness)