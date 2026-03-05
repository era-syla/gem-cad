import cadquery as cq

# Parametric dimensions
base_length = 50.0  # Length of the base plate
base_width = 30.0   # Width of the base plate
base_height = 2.0   # Thickness of the base plate

top_length = 25.0   # Length of the top block
top_width = 20.0    # Width of the top block
top_height = 4.0    # Height of the top block

# Create the base plate
# Centered on XY plane initially for easier reasoning, then offset if needed.
# Let's align the bottom-left corner to (0,0) for simplicity.
base = cq.Workplane("XY").box(base_length, base_width, base_height, centered=(False, False, False))

# Create the top block
# It needs to be positioned on top of the base.
# Based on the image, the top block is aligned with the top-right corner.
# The base is from (0,0,0) to (base_length, base_width, base_height).
# We want the top block to end at x=base_length and y=base_width.
# So its starting position would be:
# x = base_length - top_length
# y = base_width - top_width
# z = base_height

top_x_pos = base_length - top_length
top_y_pos = base_width - top_width

top = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .moveTo(top_x_pos, top_y_pos)
    .box(top_length, top_width, top_height, centered=(False, False, False))
)

# Combine the two parts into a single object
result = base.union(top)

# Alternative approach using relative positioning which might be cleaner:
# 1. Create base centered.
# 2. Select top face.
# 3. Draw rectangle anchored to a corner.
# However, the absolute positioning above is very robust for this simple shape.