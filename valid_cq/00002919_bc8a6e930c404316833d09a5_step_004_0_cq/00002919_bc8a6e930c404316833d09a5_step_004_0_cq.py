import cadquery as cq

# Define parameters for the disk
diameter = 100.0  # Diameter of the disk
thickness = 2.0   # Thickness of the disk

# Create the disk using a cylinder operation
# workplane("XY") creates a plane on the XY axes
# circle(diameter / 2) draws a circle with the specified radius
# extrude(thickness) extrudes the circle to create a solid cylinder
result = cq.Workplane("XY").circle(diameter / 2).extrude(thickness)