import cadquery as cq

# Parametric dimensions
diameter = 10.0  # Diameter of the cylinder
height = 40.0    # Height of the cylinder

# Create the cylinder
# Workplane("XY") creates a plane on the XY axes.
# circle(diameter/2) draws the base circle.
# extrude(height) extrudes the circle into a 3D cylinder.
result = cq.Workplane("XY").circle(diameter / 2).extrude(height)

# Alternatively, using the dedicated primitive method for cleaner syntax:
# result = cq.Workplane("XY").cylinder(height, diameter / 2)