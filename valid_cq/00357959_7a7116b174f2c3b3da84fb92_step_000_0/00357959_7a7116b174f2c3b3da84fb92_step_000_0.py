import cadquery as cq

# Parametric dimensions
plate_length = 120.0
plate_width = 80.0
plate_thickness = 5.0
hole_spacing_x = 40.0  # Distance between hole centers along X
hole_spacing_y = 30.0  # Distance between hole centers along Y
hole_diameter = 3.0

# Create the plate with 4 mounting holes
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .rect(hole_spacing_x, hole_spacing_y, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)