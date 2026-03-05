import cadquery as cq

# Parametric dimensions
frame_width = 100.0       # Total width of the frame
frame_height = 100.0      # Total height of the frame
border_width = 4.0        # Width of the frame material (the visible thickness of the rim)
thickness = 4.0           # Depth of extrusion

# Create the frame
# We draw the outer rectangle and the inner rectangle on the same workplane.
# CadQuery automatically interprets nested wires as a shape with a hole when extruding.
result = (
    cq.Workplane("XY")
    .rect(frame_width, frame_height)
    .rect(frame_width - 2 * border_width, frame_height - 2 * border_width)
    .extrude(thickness)
)