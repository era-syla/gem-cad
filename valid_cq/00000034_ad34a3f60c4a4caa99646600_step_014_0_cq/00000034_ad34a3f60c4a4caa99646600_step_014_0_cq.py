import cadquery as cq

# Define parametric dimensions
main_box_width = 40.0   # X-axis
main_box_depth = 40.0   # Y-axis
main_box_height = 80.0  # Z-axis

tab_width = 5.0         # Protrusion distance from the face
tab_thickness = 2.0     # Z-height of the tab
tab_length = 10.0       # Y-length of the tab
tab_height_location = main_box_height / 2 + 5.0 # Location on Z-axis

# Create the main body
main_body = cq.Workplane("XY").box(main_box_width, main_box_depth, main_box_height)

# Create the small tab on the right face (+X face)
# We select the face, work on it, and extrude a small rectangle
result = (
    main_body
    .faces(">X")
    .workplane()
    .center(0, 5) # Slight offset from vertical center if needed, based on visual estimate
    .rect(tab_length, tab_thickness)
    .extrude(tab_width)
)

# Alternatively, just union a second box if specific positioning is easier
# But the workplane method is more robust for face-relative features.
# Let's refine the tab creation to match the image better.
# The image shows a small, thin tab sticking out of the side, roughly halfway up.

# Re-creating with a simple union approach for clarity and control over absolute position
main_block = cq.Workplane("XY").box(main_box_width, main_box_depth, main_box_height)

# Create a small tab. 
# It needs to be positioned on the +X face.
# X position: center of main block + width/2 + tab_width/2
# Y position: center (0)
# Z position: slightly above center? Let's assume near center.
tab = (
    cq.Workplane("XY")
    .box(tab_width, tab_length, tab_thickness)
    .translate((main_box_width/2 + tab_width/2, 0, 5))
)

result = main_block.union(tab)