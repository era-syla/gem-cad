import cadquery as cq

# Parameter definitions based on visual estimation of the image
panel_length = 80.0
panel_height = 40.0
panel_thickness = 5.0
vertical_gap = 40.0  # Gap between the two panels

# Calculate the center-to-center spacing
# Spacing = (Height/2) + Gap + (Height/2)
spacing = panel_height + vertical_gap
offset = spacing / 2.0

# Create the result by pushing two location points on the XY plane
# and generating a box at each point.
# The separation aligns with the 'height' dimension (Y-axis).
result = (
    cq.Workplane("XY")
    .pushPoints([
        (0, -offset),
        (0, offset)
    ])
    .box(panel_length, panel_height, panel_thickness)
)