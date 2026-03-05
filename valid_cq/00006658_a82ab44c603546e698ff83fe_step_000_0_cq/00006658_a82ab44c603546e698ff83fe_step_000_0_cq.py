import cadquery as cq

# --- Parametric Dimensions ---
# These values are estimated from the visual proportions of the image.
disk_diameter = 100.0  # Overall diameter of the disk
disk_thickness = 5.0   # Thickness of the disk
center_hole_diameter = 8.0 # Diameter of the central through-hole

# The central black section looks wider than the side sections.
# Let's define the width of the central strip.
center_strip_width = 40.0 

# There are narrow grooves separating the central strip from the side segments.
groove_width = 1.5
groove_depth = 2.0  # Depth of the groove (looks like it doesn't go all the way through)

# --- Modeling Strategy ---
# 1. Create a base cylinder (disk).
# 2. Cut the central hole.
# 3. Cut two parallel grooves to separate the central region from the side "wings".
#    Based on the image, the black part is slightly recessed or just colored differently, 
#    but geometrically it looks like a flat disk with grooves. 
#    However, looking closely at the shadow lines, the grooves are distinct cuts.
#    The black coloration is likely a surface finish attribute, but for geometry, 
#    we just need the cuts.

# --- CadQuery Construction ---

# 1. Base Disk
result = cq.Workplane("XY").circle(disk_diameter / 2).extrude(disk_thickness)

# 2. Center Hole
result = result.faces(">Z").workplane().hole(center_hole_diameter)

# 3. Create the parallel grooves
# We need to cut slots. The easiest way is to sketch rectangles on the top face
# positioned correctly and cut down into the material.

# Calculate the position of the grooves.
# The central strip is centered. So the inner edge of the groove starts at center_strip_width/2.
y_pos_groove_1 = (center_strip_width / 2) + (groove_width / 2)
y_pos_groove_2 = -((center_strip_width / 2) + (groove_width / 2))

# We need rectangles long enough to cut through the entire width of the circle at those Y positions.
rect_length = disk_diameter + 10.0 # Make it slightly larger to ensure a clean cut

# Cut Groove 1 (Top)
# We position the workplane on the top face
result = (
    result.faces(">Z")
    .workplane()
    .center(0, y_pos_groove_1)
    .rect(rect_length, groove_width)
    .cutBlind(-groove_depth)
)

# Cut Groove 2 (Bottom)
# We position the workplane on the top face again (or reuse the previous one logically, 
# but starting fresh is often clearer)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, y_pos_groove_2)
    .rect(rect_length, groove_width)
    .cutBlind(-groove_depth)
)

# Alternatively, we could have done both rectangles in one operation:
# result = (
#     result.faces(">Z")
#     .workplane()
#     .rect(rect_length, groove_width).translate((0, y_pos_groove_1))
#     .rect(rect_length, groove_width).translate((0, y_pos_groove_2)) # This syntax is tricky in chaining
# )
# Sticking to sequential cuts is safer and more readable.

# 4. Optional: If the central black part is slightly raised or lowered relative to the grey sides,
# the image is ambiguous. It looks coplanar with just grooves. 
# However, sometimes these designs imply a slight recess for the side plates or the center.
# Given the "flat" look across the top highlight, I will assume they are flush and the grooves define the separation.

# Final check of the geometry
# - Disk shape: Yes
# - Center hole: Yes
# - Two parallel linear cuts: Yes