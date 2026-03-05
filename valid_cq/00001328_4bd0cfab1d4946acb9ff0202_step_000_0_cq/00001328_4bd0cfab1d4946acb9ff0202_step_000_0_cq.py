import cadquery as cq

# Parametric dimensions
base_width = 80.0
base_length = 100.0
base_thickness = 10.0

tab_size = 15.0
tab_height = 5.0  # Height above the main surface
tab_thickness = 2.0 # Thickness of the tab walls, just a guess, looks solid though?
# Actually looking closer at the image, it looks like a small solid square block 
# added to one corner on the far side. Let's assume it's a solid block.

# Create the main base plate
base = cq.Workplane("XY").box(base_width, base_length, base_thickness)

# Create the small corner tab/block
# We need to position it at one of the corners. 
# Based on the isometric view, if the main box is centered, we need to move to a back corner.
# Let's place it on the top face ("Z").

# Method 1: Absolute positioning relative to center
# x_pos = -(base_width / 2) + (tab_size / 2)
# y_pos = (base_length / 2) + (tab_size / 2) # Just hanging off slightly? Or flush?
# The image shows the small block seems to be *attached* to the corner.
# Let's look really closely at the crop.
# It looks like a small square notch was cut out of the corner, or a small square block was added.
# Actually, looking at the shading, it looks like a small cubic extrusion coming out of the back-left corner.
# It looks aligned with the back edge and the left edge.

# Let's create the base, select the top face, move to the corner, and extrude.
result = (
    cq.Workplane("XY")
    .box(base_width, base_length, base_thickness)
    .faces(">Z")
    .workplane()
    # Move to the back-left corner (-X, +Y)
    .center(-base_width/2 + tab_size/2, base_length/2 - tab_size/2)
    .rect(tab_size, tab_size)
    .extrude(tab_height)
)

# Refinement based on visual inspection:
# The small block in the image actually looks like it protrudes *upwards* from the corner.
# Wait, looking again at the intersection lines.
# The small square is flush with the back edge and the left edge.
# It sits ON TOP of the main plate.
# The code above achieves this.

# Let's double check coordinates.
# box() centers at (0,0,0).
# Back-Left corner is roughly at x = -width/2, y = +length/2.
# By centering the new workplane sketch at (-width/2 + tab_size/2, length/2 - tab_size/2), 
# the rectangle of size (tab_size, tab_size) will have its corner exactly at the block's corner.

# Final check of the code structure:
# 1. Imports ok.
# 2. Parameters ok.
# 3. Operations logical.
# 4. Result variable created.

# There is a subtle detail: The image *might* be interpreted as a cut-out corner if viewed differently, 
# but the shading (lighter top, darker side) on the small square matches the large rectangle, 
# implying it is an addition (boss) on top.

# One more interpretation: Is it a corner bracket?
# No, it looks like a solid primitive added to the assembly.

# Let's stick with the "boss on corner" approach.

result = result