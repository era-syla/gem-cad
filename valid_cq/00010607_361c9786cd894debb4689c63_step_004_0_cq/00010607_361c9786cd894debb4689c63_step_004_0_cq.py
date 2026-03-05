import cadquery as cq

# Parametric dimensions
# Since no specific dimensions were given, reasonable defaults are used
diameter = 20.0  # Diameter of the cylinder
length = 40.0    # Length of the cylinder

# Create the cylinder
# We create a circle on the XY plane and extrude it along the Z axis
result = cq.Workplane("XY").circle(diameter / 2).extrude(length)