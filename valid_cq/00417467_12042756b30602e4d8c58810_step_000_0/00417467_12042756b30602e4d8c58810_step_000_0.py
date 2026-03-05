import cadquery as cq

# Parametric dimensions
overall_length = 50.0
width = 30.0
thickness = 15.0
tip_length = 15.0

# Calculate the length of the rectangular section
rect_length = overall_length - tip_length

# Define the points for the base profile (a 5-sided polygon)
# Starting from the back-left corner (0,0)
points = [
    (0, 0),
    (rect_length, 0),                 # Bottom edge to the start of the tip
    (overall_length, width / 2.0),    # The point of the tip
    (rect_length, width),             # Top edge from the start of the tip
    (0, width)                        # Top back corner
]

# Create the workplane, draw the polyline profile, close it, and extrude
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)