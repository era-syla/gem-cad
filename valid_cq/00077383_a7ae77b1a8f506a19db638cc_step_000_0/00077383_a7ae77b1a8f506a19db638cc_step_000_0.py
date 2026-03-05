import cadquery as cq

# Parametric dimensions
width = 72.0          # Width of the phone (X axis)
length = 148.0        # Length of the phone (Y axis)
thickness = 8.0       # Thickness of the phone (Z axis)
corner_radius = 10.0  # Radius of the vertical corners
edge_fillet = 1.5     # Fillet radius for the top and bottom edges

# Speaker slot parameters
speaker_w = 14.0      # Length of the speaker slot
speaker_h = 1.5       # Width of the speaker slot
speaker_d = 0.5       # Depth of the cut
speaker_offset = (length / 2) - 12.0  # Offset from center to top

# 1. Generate the main body
# Start with a simple block
body = cq.Workplane("XY").box(width, length, thickness)

# 2. Apply rounding
# Fillet the four vertical corners first to create the rounded rectangle profile
body = body.edges("|Z").fillet(corner_radius)

# Fillet the top and bottom perimeter edges for a smooth finish
# Selecting faces >Z (top) and <Z (bottom) ensures we get the boundary loops
body = body.faces(">Z or <Z").edges().fillet(edge_fillet)

# 3. Create the earpiece speaker slot
# Select the top face, create a workplane, move to position, sketch slot, and cut
result = (
    body.faces(">Z")
    .workplane()
    .center(0, speaker_offset)
    .slot2D(speaker_w, speaker_h)
    .cutBlind(-speaker_d)
)