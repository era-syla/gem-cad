import cadquery as cq

# Parametric dimensions
plate_width = 100.0        # Total width of the plate
height_left = 130.0        # Height of the left vertical edge
height_right = 80.0        # Height of the right vertical edge
top_flat_length = 35.0     # Length of the horizontal segment at the top left
thickness = 5.0            # Thickness of the extrusion

# Define the vertices of the profile counter-clockwise from (0,0)
pts = [
    (0, 0),                           # Bottom-left
    (plate_width, 0),                 # Bottom-right
    (plate_width, height_right),      # Top-right vertical end
    (top_flat_length, height_left),   # Transition point from slope to flat
    (0, height_left)                  # Top-left
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)