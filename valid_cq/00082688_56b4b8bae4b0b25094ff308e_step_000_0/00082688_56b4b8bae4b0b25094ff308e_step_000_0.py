import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0       # Outer length of the frame
width = 80.0         # Outer width of the frame
thickness = 5.0      # Thickness (height) of the frame
border_width = 10.0  # Width of the frame walls

# Create the frame geometry
# The strategy is to draw the outer rectangle and the inner rectangle 
# in the same sketch operation, then extrude. CadQuery automatically 
# detects the inner rectangle as a hole.
result = (
    cq.Workplane("XY")
    .rect(length, width)                                     # Outer profile
    .rect(length - 2*border_width, width - 2*border_width)   # Inner profile (hole)
    .extrude(thickness)
)