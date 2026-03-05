import cadquery as cq

# -- Parametric Dimensions --
# Vertical Post
post_width = 10.0
post_depth = 10.0
post_height = 90.0

# Horizontal Beams
beam_length = 50.0       # Total length (X-axis)
beam_depth = 14.0        # Y-axis depth (thicker than post to create depth step)
beam_arm_height = 8.0    # Z-axis height of the arms
beam_hub_height = 12.0   # Z-axis height of the central intersection (creates the shoulder notch)
beam_hub_width = 10.0    # X-axis width of the hub (matches post width)

# Assembly Layout
beam_spacing = 35.0      # Vertical distance between beam centers

# -- Geometry Construction --

# 1. Create the vertical post
# Centered at the origin, aligned with Z-axis
post = cq.Workplane("XY").box(post_width, post_depth, post_height)

# 2. Define the Horizontal Beam Geometry
# The beam consists of the main arms and a thicker central hub
# Create the arms (spanning X-axis)
arms = cq.Workplane("XY").box(beam_length, beam_depth, beam_arm_height)

# Create the central hub (taller in Z, matches arm depth in Y)
# This creates the "stepped" look at the intersection
hub = cq.Workplane("XY").box(beam_hub_width, beam_depth, beam_hub_height)

# Combine arm and hub into a single beam object
beam_geometry = arms.union(hub)

# 3. Instantiate and Position Beams
# Create top beam by moving up
beam_top = beam_geometry.translate((0, 0, beam_spacing / 2))

# Create bottom beam by moving down
beam_bottom = beam_geometry.translate((0, 0, -beam_spacing / 2))

# 4. Final Boolean Union
# Combine the post and both beams into a single solid
result = post.union(beam_top).union(beam_bottom)