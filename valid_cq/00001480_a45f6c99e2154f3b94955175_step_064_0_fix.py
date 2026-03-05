import cadquery as cq

# Main block dimensions
width = 60   # X
depth = 40   # Y
height = 60  # Z

# Create the main rectangular block
main_block = cq.Workplane("XY").box(width, depth, height)

# Add a horizontal slot/gap in the middle (cutting a slot around the middle)
# The slot appears to be a horizontal cut going through the front face
slot_height = 4
slot_depth = 30
slot_width = width + 2  # full width

# Cut a horizontal slot at mid-height from the front
main_block = (
    main_block
    .faces(">Z").workplane(offset=-height/2 + 2)
    .workplane(origin=(0, 0, 0))
)

# Let's approach differently - create two blocks with a gap between them
# Upper block
upper_height = 30
lower_height = 28
gap = 4
total = upper_height + gap + lower_height

upper_block = cq.Workplane("XY").box(width, depth, upper_height).translate((0, 0, lower_height + gap + upper_height/2))
lower_block = cq.Workplane("XY").box(width, depth, lower_height).translate((0, 0, lower_height/2))

# Combine them
result = upper_block.union(lower_block)

# Now cut a slot through the middle area (the gap between blocks, but add a thin tab/slot feature)
# The slot appears to go through the side faces horizontally
slot_cut = (
    cq.Workplane("XY")
    .box(width * 0.6, depth + 2, gap)
    .translate((0, 0, lower_height + gap/2))
)

# Don't cut the full gap - leave a thin slot opening on the right side
# The slot appears to be a rectangular cutout visible from the front/right
# Cut full gap but leave it as open space (already done by two separate blocks)

# Add the slot cut through one side (the elongated slot visible on front face)
slot_feature = (
    cq.Workplane("XY")
    .box(width * 0.5, 5, gap * 0.6)
    .translate((0, depth/2 - 2, lower_height + gap/2))
)

result = result.cut(slot_feature)

# Add holes - top face hole (left side)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-width/4, 0)])
    .hole(8)
)

# Right face holes
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(width/4, upper_height/2 + gap/2 + lower_height - total/2 + total/2 - lower_height - gap/2),
                 (width/4, -total/2 + lower_height/2)])
    .hole(8)
)

# Apply chamfer to top edges
result = (
    result
    .edges("|Z")
    .chamfer(2)
)