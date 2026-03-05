import cadquery as cq

# Parametric dimensions
rod_length = 100.0  # Total length of the cylindrical rod
rod_diameter = 10.0 # Diameter of the rod

# Create the 3D model
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)