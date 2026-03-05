import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
height = 600.0        # Total height of the panel
width = 350.0         # Total width of the panel
thickness = 25.0      # Total thickness of the frame
frame_width = 40.0    # Width of the surrounding frame
recess_depth = 10.0   # Depth of the center indentation

# Create the geometry
# 1. Start with a solid box representing the outer dimensions
# 2. Select the front face (Z max)
# 3. Sketch a rectangle offset by the frame width for the inner panel
# 4. Cut the material to create the recess
result = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .faces(">Z")
    .workplane()
    .rect(width - 2 * frame_width, height - 2 * frame_width)
    .cutBlind(-recess_depth)
)