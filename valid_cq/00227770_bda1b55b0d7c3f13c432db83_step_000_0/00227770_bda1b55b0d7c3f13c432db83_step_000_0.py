import cadquery as cq

# Parametric dimensions for the wedge
length = 100.0  # Length of the base
width = 25.0    # Width/Thickness of the wedge
height = 35.0   # Vertical height at the thick end

# Generate the wedge geometry
# We define the triangular profile on the XZ plane (Front view)
# The profile consists of a horizontal base, a sloped top, and a vertical back.
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(length, 0)      # Draw base line to the tip
    .lineTo(0, height)      # Draw slope line back to the top of the vertical edge
    .close()                # Close the shape to form the vertical edge
    .extrude(width)         # Extrude along the Y axis to create the solid
)