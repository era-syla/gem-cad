import cadquery as cq

# Parametric dimensions for the trapezoidal frame
length = 100.0        # Overall length of the part
width_start = 50.0    # Width at the wider end
width_end = 25.0      # Width at the narrower end
height = 15.0         # Height of the extrusion
thickness = 3.0       # Wall thickness

# Define the points of the trapezoid base profile
# Centered around the origin
pts = [
    (-length / 2.0, -width_start / 2.0), # Bottom-left
    (length / 2.0, -width_end / 2.0),    # Bottom-right
    (length / 2.0, width_end / 2.0),     # Top-right
    (-length / 2.0, width_start / 2.0)   # Top-left
]

# Create the result
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
    # Select faces parallel to the Z plane (Top and Bottom)
    .faces("|Z")
    # Shell inwards (negative thickness) to hollow out the solid and remove selected faces
    .shell(-thickness)
)