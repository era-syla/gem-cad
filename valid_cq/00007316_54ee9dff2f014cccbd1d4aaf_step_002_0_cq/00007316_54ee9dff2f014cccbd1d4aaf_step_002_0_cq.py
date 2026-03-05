import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the disc
thickness = 2.0  # Thickness of the disc

# Create the disc
# Workplane("XY") creates a plane on the XY axes.
# circle(radius) creates a 2D circle profile.
# extrude(length) extrudes the 2D profile into a 3D solid.
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(thickness)