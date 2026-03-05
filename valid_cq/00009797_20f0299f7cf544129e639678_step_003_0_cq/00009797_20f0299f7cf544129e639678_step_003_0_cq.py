import cadquery as cq

# Define parameters for the rod
length = 100.0  # Length of the rod
diameter = 5.0  # Diameter of the rod
radius = diameter / 2.0

# Create the cylindrical rod
# We extrude a circle along the Z axis to create the rod
result = cq.Workplane("XY").circle(radius).extrude(length)