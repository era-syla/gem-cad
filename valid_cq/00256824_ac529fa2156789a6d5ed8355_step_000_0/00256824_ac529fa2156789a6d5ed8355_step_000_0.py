import cadquery as cq

# Geometric Parameters
post_height = 100.0  # Total height of the vertical post
bar_width = 110.0    # Total length of the horizontal bars
thickness = 12.0     # Thickness (height) of the bars and width of the post
depth = 12.0         # Extrusion depth of the entire model
bar_spacing = 45.0   # Center-to-center distance between the top and middle bar

# 1. Create the Vertical Post
# Centered at the origin on the XY plane
vertical_post = cq.Workplane("XY").box(thickness, post_height, depth)

# 2. Create the Top Horizontal Bar
# Calculate the center Y position so the bar is flush with the top of the post
# Top of post is at y = post_height / 2
top_bar_y = (post_height / 2) - (thickness / 2)
top_bar = cq.Workplane("XY").center(0, top_bar_y).box(bar_width, thickness, depth)

# 3. Create the Middle Horizontal Bar
# Positioned below the top bar based on the spacing parameter
mid_bar_y = top_bar_y - bar_spacing
mid_bar = cq.Workplane("XY").center(0, mid_bar_y).box(bar_width, thickness, depth)

# 4. Combine all parts into the final result using boolean union
result = vertical_post.union(top_bar).union(mid_bar)