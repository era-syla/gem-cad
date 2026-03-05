import cadquery as cq

# Parametric dimensions
frame_height = 200.0  # Overall height of the frame
frame_width = 80.0    # Overall width of the frame
frame_thickness = 10.0 # Depth of the extrusion
border_width = 8.0    # Width of the frame border material

# Create the frame geometry
# Method: Sketch a rectangle and offset it inwards to create the frame profile, then extrude.

result = (
    cq.Workplane("XY")
    .rect(frame_width, frame_height)  # Create the outer rectangle
    .rect(frame_width - 2 * border_width, frame_height - 2 * border_width) # Create the inner rectangle (cutout)
    .extrude(frame_thickness) # Extrude the difference
)

# Alternative method (Difference of two boxes):
# outer_box = cq.Workplane("XY").box(frame_width, frame_height, frame_thickness)
# inner_box = cq.Workplane("XY").box(frame_width - 2*border_width, frame_height - 2*border_width, frame_thickness)
# result = outer_box.cut(inner_box)