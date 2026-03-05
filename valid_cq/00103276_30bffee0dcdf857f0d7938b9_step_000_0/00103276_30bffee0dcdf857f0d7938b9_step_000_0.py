import cadquery as cq

# Parametric dimensions based on the image proportions
plate_length = 100.0
plate_height = 50.0
plate_thickness = 5.0
hole_diameter = 2.5
hole_depth = 15.0

# Create the 3D model
# 1. Create a box representing the main plate body (Length along X, Thickness along Y, Height along Z)
# 2. Select the top face (+Z)
# 3. Create a workplane on that face (automatically centered)
# 4. Cut a hole into the top face
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_thickness, plate_height)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter, hole_depth)
)