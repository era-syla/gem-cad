import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
height = 60.0    # Height of the cylinder

# Create the cylinder
# cq.Workplane('XY') defines the sketching plane.
# .circle(radius) draws a circle on that plane.
# .extrude(height) extrudes the circle into a 3D solid.
result = cq.Workplane('XY').circle(diameter / 2).extrude(height)