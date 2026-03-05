import cadquery as cq

# Parametric dimensions
vertical_height = 100.0      # Total height of the vertical section
vertical_width = 20.0        # Width of the vertical section
horizontal_length = 60.0     # Length of the horizontal section protruding from the vertical one
horizontal_width = 20.0      # Width of the horizontal section
thickness = 10.0             # Thickness of the plate

# Define the vertices of the T-shape profile
# The profile is drawn on the XY plane.
# The vertical bar is aligned along the Y-axis, positioned to the right of the Y-axis.
# The horizontal bar protrudes to the left (negative X).
points = [
    (0, horizontal_width / 2),                 # Inner top corner
    (0, vertical_height / 2),                  # Top left of vertical bar
    (vertical_width, vertical_height / 2),     # Top right of vertical bar
    (vertical_width, -vertical_height / 2),    # Bottom right of vertical bar
    (0, -vertical_height / 2),                 # Bottom left of vertical bar
    (0, -horizontal_width / 2),                # Inner bottom corner
    (-horizontal_length, -horizontal_width / 2), # Bottom tip of horizontal bar
    (-horizontal_length, horizontal_width / 2)   # Top tip of horizontal bar
]

# Create the 3D solid
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)