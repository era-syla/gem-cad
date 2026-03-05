import cadquery as cq

# --- Parametric Dimensions ---
# Based on the visual proportions of the image (05-8 text likely implies size)
shaft_diameter = 5.0     # The "05" usually denotes diameter
shaft_length = 35.0      # Estimated length relative to diameter
head_diameter = 8.0      # The "8" likely denotes head size or type, 8mm fits proportions
head_height = 5.0        # Thickness of the top cylinder
text_string = "05-8"
text_size = 2.5          # Font size
text_depth = 0.5         # How much the text sticks up

# --- Modeling ---

# 1. Create the Shaft
# A simple cylinder along the Z-axis
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)

# 2. Create the Head
# A larger cylinder on top of the shaft
# We select the top face of the shaft to start drawing the head
head = (
    shaft.faces(">Z")
    .workplane()
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# 3. Add the Embossed Text
# The text is on the top face of the head
# We need to rotate it slightly to match the image orientation
result = (
    head.faces(">Z")
    .workplane()
    .transformed(rotate=(0, 0, 45))  # Rotate text 45 degrees to match view
    .text(text_string, text_size, text_depth)
)

# Note: The text creates a separate solid object combined with the main body.
# If a boolean union is strictly required, .text() usually handles it, 
# but sometimes combining explicitly is safer depending on the CQ version.
# In standard CQ, .text() adds material by default.

# If you were running this in an interactive environment (like CQ-editor):
# show_object(result)