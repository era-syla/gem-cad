import cadquery as cq

# Parametric dimensions for the triangular prism
length = 60.0        # The length of the prism (extrusion depth)
base_width = 40.0    # The width of the triangular base
height = 25.0        # The height of the triangular profile
peak_offset = 15.0   # The horizontal position of the top peak relative to the base (0 to base_width)

# Create the triangular prism
# Sketch the triangular profile on the YZ plane and extrude along the X axis
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                   # Start point (bottom-left of triangle)
        (base_width, 0),          # Bottom-right of triangle
        (peak_offset, height)     # Top peak vertex
    ])
    .close()                      # Close the profile to form a wire
    .extrude(length)              # Extrude to form the solid prism
)