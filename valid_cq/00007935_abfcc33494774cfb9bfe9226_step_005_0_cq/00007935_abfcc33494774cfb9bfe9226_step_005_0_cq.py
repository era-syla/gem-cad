import cadquery as cq

# -- Parametric Dimensions --
# Main shaft dimensions
shaft_bottom_dia = 10.0
shaft_bottom_len = 10.0

shaft_middle_dia = 12.0
shaft_middle_len = 60.0

shaft_top_dia = 9.0
shaft_top_len = 50.0

# Feature dimensions
# Two flat cuts (like a 'double-D' or parallel flats) at the very top
flat_width = 7.0  # Distance between the two flat faces
flat_length = 15.0 # Length of the flats from the top down
chamfer_size = 0.5 # Chamfer for edges

# -- Modeling --

# 1. Start with the bottom section
result = (cq.Workplane("XY")
          .circle(shaft_bottom_dia / 2.0)
          .extrude(shaft_bottom_len)
          )

# 2. Add the middle section on top of the bottom section
result = (result.faces(">Z")
          .workplane()
          .circle(shaft_middle_dia / 2.0)
          .extrude(shaft_middle_len)
          )

# 3. Add the top section on top of the middle section
result = (result.faces(">Z")
          .workplane()
          .circle(shaft_top_dia / 2.0)
          .extrude(shaft_top_len)
          )

# 4. Create the flats on the top section
# We move to the top face, then create a cut that slices off the sides.
# A simple way is to define a rectangle that represents the remaining material
# and intersect, or better, define rectangles outside and cut.
# However, a common machining operation is side milling.
# Let's use a cut based on a sketch on the top face.

# We want to leave a `flat_width` in the center.
# The radius is `shaft_top_dia / 2`.
# We need to cut away material where x > flat_width/2 and x < -flat_width/2
# or y > flat_width/2 ... looking at the image, it seems like two parallel flats.

cut_depth = flat_length

# Create a workplane on the top face
wp_top = result.faces(">Z").workplane()

# We will cut two rectangles on either side of the center strip.
# The rectangles need to be large enough to clear the circle.
cut_rect_width = shaft_top_dia  # Large enough to clear
cut_rect_offset = (flat_width / 2.0) + (cut_rect_width / 2.0)

# Cut 1
result = (result.faces(">Z")
          .workplane()
          .center(cut_rect_offset, 0)
          .rect(cut_rect_width, shaft_top_dia * 2) # Make height generous
          .cutBlind(-cut_depth)
          )

# Cut 2
result = (result.faces(">Z")
          .workplane()
          .center(-cut_rect_offset, 0)
          .rect(cut_rect_width, shaft_top_dia * 2)
          .cutBlind(-cut_depth)
          )

# 5. Add chamfers (optional but adds realism based on image rendering style)
# Chamfer the top edge
result = result.faces(">Z").edges().chamfer(chamfer_size)

# Chamfer the bottom edge
result = result.faces("<Z").edges().chamfer(chamfer_size)

# Chamfer the transition steps (should select the circular edges at the steps)
# Middle-to-Bottom step is at Z = shaft_bottom_len
# Top-to-Middle step is at Z = shaft_bottom_len + shaft_middle_len
# Since automatic edge selection can be tricky with specific coordinates,
# we can try selecting by Z position range if needed, or just leave as sharp corners
# which is common for lathed parts unless specified. 
# Looking at the image, the transitions look fairly sharp or have small fillets.
# Let's add a small fillet to the step transitions for good measure.
try:
    result = result.edges(f"|Z and >Z[{shaft_bottom_len - 0.1}] and <Z[{shaft_bottom_len + 0.1}]").fillet(0.2)
    result = result.edges(f"|Z and >Z[{shaft_bottom_len + shaft_middle_len - 0.1}] and <Z[{shaft_bottom_len + shaft_middle_len + 0.1}]").fillet(0.2)
except:
    pass # Skip if selection fails

# Show the result
# show_object(result)