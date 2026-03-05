import cadquery as cq

# Parametric definitions for the model dimensions
bar_height = 300.0      # Total length of the bar
bar_width = 15.0        # Width of the face with notches
bar_thickness = 15.0    # Thickness/depth of the bar
notch_height = 15.0     # Vertical span of the notch
notch_depth = 8.0       # Depth of the cut into the bar width
end_offset = 25.0       # Distance from the top/bottom ends to the start of the notch

# Calculate the Y-axis center positions for the top and bottom notches
# The bar is centered at the origin, so top is at +height/2
top_notch_center_y = (bar_height / 2.0) - end_offset - (notch_height / 2.0)
bottom_notch_center_y = -top_notch_center_y

# Generate the geometry
result = (
    cq.Workplane("XY")
    # Create the main vertical bar centered at the origin
    .box(bar_width, bar_thickness, bar_height)
    # Select the front face to sketch the cuts
    .faces(">Y")
    .workplane()
    # Position the sketch cursors at the notch locations on the left edge (-X)
    .pushPoints([
        (-bar_width / 2.0, top_notch_center_y),
        (-bar_width / 2.0, bottom_notch_center_y)
    ])
    # Draw rectangles for the notches.
    # Width is 2x depth because the rectangle is centered on the edge;
    # half will be outside the part, half will cut inside.
    .rect(notch_depth * 2.0, notch_height)
    # Cut through the entire thickness of the bar
    .cutThruAll()
)