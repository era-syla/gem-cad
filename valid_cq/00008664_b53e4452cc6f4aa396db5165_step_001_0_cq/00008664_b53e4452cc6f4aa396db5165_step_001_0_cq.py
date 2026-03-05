import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
total_length = 120.0  # Estimated length
bar_width = 10.0      # Width of the long narrow section
bar_height = 10.0     # Height of the long narrow section
bar_length = 90.0     # Length of just the narrow section

# Head (mounting block) dimensions
head_width = 25.0
head_length = total_length - bar_length
head_height = 10.0    # Looks same height in the image, but let's be flexible
head_fillet_radius = 3.0 # Fillet on the transition and corners

# Hole dimensions
# Two large holes on the head
head_hole_diam = 6.0
head_hole_spacing = 14.0
head_hole_c_bore_diam = 10.0
head_hole_c_bore_depth = 3.0

# Small side holes on the bar tip
tip_hole_diam = 2.5
tip_hole_spacing = 8.0
tip_first_hole_dist = 5.0
tip_end_hole_diam = 2.0 # Hole on the very end face

# --- Modeling ---

# 1. Create the main bar
# We'll align the bar along the X axis
bar = cq.Workplane("XY").box(bar_length, bar_width, bar_height) \
    .translate((bar_length/2, 0, bar_height/2))

# 2. Create the head (mounting block)
# It's wider than the bar and located at the end
head = cq.Workplane("XY").box(head_length, head_width, head_height) \
    .translate((bar_length + head_length/2, 0, head_height/2))

# 3. Fuse them together
part = bar.union(head)

# 4. Add the transition fillet
# The image shows a smooth transition between the narrow bar and the wider head.
# We select the vertical edges at the junction (X = bar_length)
part = part.faces(">X[0]").edges("|Z").fillet(head_fillet_radius)

# 5. Add fillets to the outer corners of the head
part = part.edges(">X and |Z").fillet(head_fillet_radius)


# 6. Add Holes to the Head
# Two counterbored holes
# Calculate positions based on head center
head_center_x = bar_length + head_length/2
hole1_pos = (head_center_x, 0) # Center
# Actually, the image shows them side-by-side along the width or length?
# Looking at the image, the head is wider. The holes are aligned along the Y axis relative to the bar?
# No, looking closely, the holes are aligned along the length (X axis) of the head part?
# Let's re-examine. The head looks wider than the bar (Y axis). The holes are arranged along the X-axis of the head?
# Or maybe side by side in Y?
# Let's assume they are along the centerline of the head (X-axis) for standard mounting straps,
# but the image shows them somewhat separated. Let's look at the proportion.
# The head is a rectangle. The holes seem to be along the long axis of the head piece?
# Wait, the head is wider (Y) than the bar, but maybe shorter in X?
# Let's assume the holes are aligned along the Y axis (perpendicular to the bar length) 
# OR aligned along the X axis. 
# Looking at the reflection/shading: The holes are side-by-side relative to the long axis of the *bar*.
# So, they are displaced in Y. But the head is not that wide.
# Let's try placing them along the X axis of the head block.
hole_x_offset = head_length / 4.0
pos1 = (bar_length + head_length/2 - hole_x_offset, 0)
pos2 = (bar_length + head_length/2 + hole_x_offset, 0)

# Re-evaluating based on typical sensor bracket design: 
# Often these have two holes along the long axis of the block.
part = part.faces(">Z").workplane() \
    .pushPoints([pos1, pos2]) \
    .cboreHole(head_hole_diam, head_hole_c_bore_diam, head_hole_c_bore_depth)


# 7. Add small holes to the tip of the bar
# Side holes (Y axis direction)
part = part.faces(">Y").workplane(centerOption="CenterOfBoundBox") \
    .center(-total_length/2 + tip_first_hole_dist, 0) \
    .hole(tip_hole_diam) \
    .center(tip_hole_spacing, 0) \
    .hole(tip_hole_diam)

# End hole (X axis direction)
part = part.faces("<X").workplane() \
    .hole(tip_end_hole_diam, depth=10)

result = part