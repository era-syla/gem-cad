import cadquery as cq

# Parametric dimensions based on visual estimation
# The object appears to be composed of two side-by-side square sections
section_depth = 50.0
section_width = 50.0
total_width = section_width * 2.0
total_height = 80.0
hole_diameter = 12.0

# Create the 3D model
# 1. Create the main rectangular block defined by total width, depth, and height
# 2. Select the top face (+Z)
# 3. Create a workplane on the top face
# 4. Move the center to the right half of the block to position the hole
#    (Since the box is centered at 0,0, moving +total_width/4 positions it in the center of the right section)
# 5. Cut the hole
result = (
    cq.Workplane("XY")
    .box(total_width, section_depth, total_height)
    .faces(">Z")
    .workplane()
    .center(total_width / 4.0, 0)
    .hole(hole_diameter)
)