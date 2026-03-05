import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the extrusion
width = 50.0     # Width of the channel (flange length)
height = 25.0    # Height of the channel (web height)
thickness = 4.0  # Wall thickness

# Create the C-channel profile on the YZ plane and extrude along X
# The sketch traces the solid wall cross-section
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                                      # Bottom-left tip (open end)
        (width, 0),                                  # Bottom-right corner (outer web)
        (width, height),                             # Top-right corner (outer web)
        (0, height),                                 # Top-left tip (open end)
        (0, height - thickness),                     # Top-left inner tip
        (width - thickness, height - thickness),     # Top-right inner corner
        (width - thickness, thickness),              # Bottom-right inner corner
        (0, thickness),                              # Bottom-left inner tip
        (0, 0)                                       # Close the loop
    ])
    .close()
    .extrude(length)
)