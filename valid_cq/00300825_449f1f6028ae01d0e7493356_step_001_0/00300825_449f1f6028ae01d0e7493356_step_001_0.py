import cadquery as cq

# Parametric dimensions
frame_width = 100.0
frame_height = 60.0
frame_depth = 5.0     # Thickness of the extrusion
border_width = 5.0    # Width of the frame edges

# Create the rectangular frame geometry
# We sketch on the XZ plane so the frame stands upright in standard isometric views
result = (
    cq.Workplane("XZ")
    .rect(frame_width, frame_height)
    .rect(frame_width - 2 * border_width, frame_height - 2 * border_width)
    .extrude(frame_depth)
)