import cadquery as cq

# Parametric dimensions
rod_length = 200.0  # Length of the rod
rod_diameter = 4.0  # Diameter of the rod

# Create the rod geometry
# We extrude a circle to create the cylindrical rod
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2)
    .extrude(rod_length)
)

# Alternatively, using the dedicated cylinder creation method which is more direct:
# result = cq.Workplane("XY").cylinder(rod_length, rod_diameter / 2)