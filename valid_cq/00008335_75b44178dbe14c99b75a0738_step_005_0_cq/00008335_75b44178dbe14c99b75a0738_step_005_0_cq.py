import cadquery as cq

# Define parameters for the cylindrical rod
length = 200.0  # Total length of the rod
diameter = 5.0  # Diameter of the rod

# Create the cylindrical rod
# We align it along the X-axis for better visualization relative to the provided image
result = cq.Workplane("YZ").circle(diameter / 2).extrude(length)

# Alternatively, using the cylinder primitive directly:
# result = cq.Workplane("XY").cylinder(height=length, radius=diameter/2, direct=(1, 0, 0))