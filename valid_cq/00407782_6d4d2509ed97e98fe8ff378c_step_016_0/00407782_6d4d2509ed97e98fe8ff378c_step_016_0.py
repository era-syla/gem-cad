import cadquery as cq

# Parametric dimensions
length = 100.0       # External length of the frame
width = 60.0         # External width of the frame
thickness = 2.0      # Thickness of the plate
border_width = 10.0  # Width of the frame border

# Create the frame geometry
# We sketch the outer rectangle, then the inner rectangle, 
# and extrude the area between them.
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .rect(length - 2 * border_width, width - 2 * border_width)
    .extrude(thickness)
)