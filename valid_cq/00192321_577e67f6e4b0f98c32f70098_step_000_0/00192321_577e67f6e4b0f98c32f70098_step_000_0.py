import cadquery as cq

# Parametric dimensions
length = 100.0      # Length of the box
width = 40.0        # Width of the box
height_high = 50.0  # Height at the back (taller end)
height_low = 25.0   # Height at the front (shorter end)
thickness = 2.0     # Wall thickness

# Create the geometry
result = (
    cq.Workplane("XZ")  # Draw on the Front plane
    .polyline([
        (0, 0),                 # Bottom-left
        (length, 0),            # Bottom-right
        (length, height_high),  # Top-right
        (0, height_low)         # Top-left
    ])
    .close()
    .extrude(width)             # Extrude along Y axis to create the block
    .faces("+Z")                # Select the top slanted face (normal points generally up)
    .shell(-thickness)          # Shell inwards, removing the selected top face
)