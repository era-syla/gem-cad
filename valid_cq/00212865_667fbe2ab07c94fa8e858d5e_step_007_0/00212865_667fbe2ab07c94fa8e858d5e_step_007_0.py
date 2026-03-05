import cadquery as cq

# Parametric dimensions for the table-like object
top_diameter = 100.0   # Diameter of the large top plate
top_thickness = 2.0    # Thickness of the top plate
base_diameter = 40.0   # Diameter of the central support base
base_height = 25.0     # Height of the base

# Generate the 3D model
# 1. Start on the XY plane and create the base cylinder
# 2. Select the top face of the base
# 3. Create the wider top plate and extrude it upwards
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    .faces(">Z")
    .workplane()
    .circle(top_diameter / 2.0)
    .extrude(top_thickness)
)