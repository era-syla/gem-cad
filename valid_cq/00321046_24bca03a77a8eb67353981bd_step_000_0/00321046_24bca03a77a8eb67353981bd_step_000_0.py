import cadquery as cq

# Parametric dimensions
plate_width = 100.0     # Width of the square plate
plate_height = 100.0    # Height of the square plate
thickness = 5.0         # Thickness of the plate
hole_diameter = 70.0    # Diameter of the center hole

# Create the 3D model
# 1. Start on the XY plane
# 2. Define the outer rectangular profile
# 3. Define the inner circular profile (CadQuery interprets nested wires as holes)
# 4. Extrude the profile to create the solid geometry
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .circle(hole_diameter / 2.0)
    .extrude(thickness)
)