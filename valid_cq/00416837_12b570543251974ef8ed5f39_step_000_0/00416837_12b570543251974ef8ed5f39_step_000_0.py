import cadquery as cq

# Parametric dimensions
length = 120.0
width = 20.0
thickness = 6.0
taper_length = 30.0

# Create the model by sketching the side profile and extruding
# We sketch on the XZ plane to define the length and thickness/taper profile
# Then extrude along Y to define the width
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),                                # Bottom-left corner
        (length, 0),                           # Bottom-right tip (sharp edge)
        (length - taper_length, thickness),    # Top start of the taper
        (0, thickness)                         # Top-left corner
    ])
    .close()
    .extrude(width / 2.0, both=True)           # Extrude symmetrically to create the width
)