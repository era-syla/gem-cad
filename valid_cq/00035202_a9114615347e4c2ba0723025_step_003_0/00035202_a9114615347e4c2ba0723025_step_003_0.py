import cadquery as cq

# Parametric dimensions
plate_width = 100.0    # Width of the square plate
plate_length = 100.0   # Length of the square plate
thickness = 5.0        # Thickness of the plate
hole_diameter = 60.0   # Diameter of the central hole

# Generate the CAD model
# 1. Initialize workplane on XY axis
# 2. Draw the outer rectangular profile
# 3. Draw the inner circular profile (which becomes a hole when extruded with the outer profile)
# 4. Extrude the sketch to create the solid
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .circle(hole_diameter / 2.0)
    .extrude(thickness)
)