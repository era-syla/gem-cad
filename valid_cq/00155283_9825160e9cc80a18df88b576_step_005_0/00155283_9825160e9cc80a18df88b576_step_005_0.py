import cadquery as cq

# Parametric dimensions for the rod
length = 300.0  # Total length of the rod
diameter = 6.0  # Diameter of the rod cross-section

# Create the cylindrical rod geometry
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)