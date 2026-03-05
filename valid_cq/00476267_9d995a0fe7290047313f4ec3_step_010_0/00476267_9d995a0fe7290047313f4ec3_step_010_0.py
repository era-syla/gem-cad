import cadquery as cq

# Parametric dimensions
height = 60.0    # Total length of the cylinder
diameter = 10.0  # Diameter of the cylinder
radius = diameter / 2.0

# Create the solid geometry
# Start on the XY plane, draw the circular profile, and extrude to height
result = cq.Workplane("XY").circle(radius).extrude(height)