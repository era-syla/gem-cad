import cadquery as cq

# Parameters based on visual estimation of proportions
length = 100.0         # Total length of the link
width = 25.0           # Width of the flat section
thickness = 5.0        # Thickness of the plate
offset = 25.0          # Vertical offset between the left and right axes
transition_len = 30.0  # Horizontal length of the angled transition section
hole_diameter = 10.0   # Diameter of the mounting holes
hole_margin = 15.0     # Distance from the end edge to the hole center

# Calculated coordinates relative to center (0,0)
x_end = length / 2.0
x_trans = transition_len / 2.0
y_left = -offset / 2.0
y_right = offset / 2.0
half_width = width / 2.0

# Define the profile points (Counter-Clockwise starting from bottom-left)
points = [
    (-x_end, y_left - half_width),           # Bottom-left corner of left pad
    (-x_trans, y_left - half_width),         # Start of bottom slope
    (x_trans, y_right - half_width),         # End of bottom slope (right pad)
    (x_end, y_right - half_width),           # Bottom-right corner
    (x_end, y_right + half_width),           # Top-right corner
    (x_trans, y_right + half_width),         # Start of top slope
    (-x_trans, y_left + half_width),         # End of top slope (left pad)
    (-x_end, y_left + half_width)            # Top-left corner
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-x_end + hole_margin, y_left),
        (x_end - hole_margin, y_right)
    ])
    .hole(hole_diameter)
)