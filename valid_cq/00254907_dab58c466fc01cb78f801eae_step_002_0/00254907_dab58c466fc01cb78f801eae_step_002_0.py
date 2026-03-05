import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
total_height = 80.0       # Overall height of the object
lower_height = 25.0       # Height of the straight vertical section
width = 20.0              # Width of the object (extrusion depth)
thickness = 5.0           # Thickness of the profile (side view width)
lean_offset = 8.0         # Horizontal displacement of the top relative to the vertical section

# Generate the model
# Strategy: Sketch the side profile (L-shape/bent shape) on the YZ plane and extrude along the X axis.
# - Z axis is height
# - Y axis is the thickness/lean direction
# - X axis is the width direction
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                                # Bottom-left corner
        (thickness, 0),                        # Bottom-right corner
        (thickness, lower_height),             # Outer bend point
        (thickness + lean_offset, total_height), # Top-right corner (leaning)
        (lean_offset, total_height),           # Top-left corner (leaning)
        (0, lower_height),                     # Inner bend point
        (0, 0)                                 # Close back to start
    ])
    .close()
    .extrude(width)
)