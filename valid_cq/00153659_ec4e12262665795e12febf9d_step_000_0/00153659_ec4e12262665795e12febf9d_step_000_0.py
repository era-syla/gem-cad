import cadquery as cq

# Parametric dimensions
length = 100.0        # Total length of the part
width = 20.0          # Width (depth) of the part
height = 20.0         # Total height of the part
cutout_length = 20.0  # Length of the step cutout
cutout_height = 10.0  # Height of the step cutout

# Create the model by drawing the side profile on the XZ plane and extruding
# The profile represents the 'L' shape of the side view
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),                                      # Bottom-left corner
        (length - cutout_length, 0),                 # Bottom edge to start of cut
        (length - cutout_length, cutout_height),     # Vertical step up
        (length, cutout_height),                     # Horizontal step to right edge
        (length, height),                            # Right edge to top
        (0, height)                                  # Top edge to top-left
    ])
    .close()
    .extrude(width)
)