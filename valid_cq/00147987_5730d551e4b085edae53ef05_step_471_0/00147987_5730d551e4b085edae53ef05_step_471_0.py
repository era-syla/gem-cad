import cadquery as cq

# Parametric dimensions based on visual estimation
total_length = 140.0  # Overall length of the stadium shape
total_width = 20.0    # Overall width (diameter of the curved ends)
thickness = 2.0       # Wall thickness of the band
height = 4.0          # Height of the extrusion

# Create the stadium-shaped band (obround loop)
result = (
    cq.Workplane("XY")
    # Create the outer boundary wire
    .slot2D(total_length, total_width)
    # Create the inner boundary wire
    # Subtracting 2*thickness from both length and width maintains a constant wall thickness
    .slot2D(total_length - 2 * thickness, total_width - 2 * thickness)
    # Extruding a shape with a nested wire automatically creates a hollow solid
    .extrude(height)
)