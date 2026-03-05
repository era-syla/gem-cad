import cadquery as cq

# Parametric dimensions
rod_length = 200.0  # Length of the rod
rod_diameter = 5.0  # Diameter of the rod

# Create the cylindrical rod
# We start with a workplane (XY plane is standard)
# Draw a circle with the specified radius
# Extrude it to the specified length
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)