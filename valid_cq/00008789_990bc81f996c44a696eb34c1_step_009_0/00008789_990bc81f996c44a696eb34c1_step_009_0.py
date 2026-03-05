import cadquery as cq

# Parameters for the geometry
length = 140.0        # Total length of the plate
width = 100.0         # Total width of the plate
thickness = 10.0      # Thickness of the plate
chamfer_w = 60.0      # Horizontal dimension of the corner cut
chamfer_h = 50.0      # Vertical dimension of the corner cut
hole_diam = 12.0      # Diameter of the 4 holes
margin = 20.0         # Margin from edges for hole placement

# Define vertices for the base shape (counter-clockwise)
# The shape is a rectangle with the top-right corner chamfered
points = [
    (0, 0),                           # Bottom-left
    (length, 0),                      # Bottom-right
    (length, width - chamfer_h),      # Start of chamfer on right edge
    (length - chamfer_w, width),      # End of chamfer on top edge
    (0, width)                        # Top-left
]

# Define hole positions
# 1. Bottom-Left
# 2. Top-Left
# 3. Bottom-Right
# 4. Top-Right (shifted inwards to account for the chamfer)
hole_locations = [
    (margin, margin),
    (margin, width - margin),
    (length - margin, margin),
    (length - chamfer_w - 15, width - margin)
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diam)
)