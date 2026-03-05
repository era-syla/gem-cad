import cadquery as cq

# Parametric dimensions
rod_length = 100.0  # Length of the rod
rod_diameter = 2.0  # Diameter of the rod

# Create the cylindrical rod model
# Start on the XY plane, draw a circle, and extrude it vertically along the Z-axis
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)