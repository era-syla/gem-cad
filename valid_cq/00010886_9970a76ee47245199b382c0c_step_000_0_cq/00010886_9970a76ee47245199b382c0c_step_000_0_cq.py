import cadquery as cq

# --- Parametric Dimensions ---

# Handle (Rectangular part)
handle_length = 60.0
handle_width = 15.0
handle_thickness = 10.0
handle_chamfer = 2.0

# Shaft (Cylindrical part)
shaft_length = 50.0
shaft_diameter = 6.0

# Head (Teardrop shape)
head_radius = 9.0  # Radius of the large circular part
head_thickness = 8.0
head_length_overall = 25.0 # Approximate length from center of circle to tip
head_tip_width = shaft_diameter # Width where it meets the shaft (or slightly wider)

# --- Geometry Construction ---

# 1. Create the Handle
# A rectangular block centered on the X-axis for length
handle = (cq.Workplane("XY")
          .box(handle_length, handle_width, handle_thickness)
          .edges("|X") # Select edges running along X
          .chamfer(handle_chamfer) # Chamfer the long edges for grip
          .translate((handle_length / 2 + shaft_length, 0, 0)) # Position it at the end of the shaft
          )

# 2. Create the Shaft
# A cylinder connecting the head area to the handle
shaft = (cq.Workplane("YZ")
         .circle(shaft_diameter / 2)
         .extrude(shaft_length + handle_length / 2) # Extrude into the handle slightly
         .rotate((0,0,0), (0,1,0), 90) # Rotate to align with X axis
         .translate((0, 0, 0)) # Start near origin
         )

# 3. Create the Head
# The head has a specific "teardrop" or ratchet head shape.
# We will construct it by lofting or extruding a sketch.
# Let's try a simple extrusion of a composite 2D shape on the XY plane.

# Center of the circular part of the head
head_center_x = 0
head_center_y = 0

# Define the 2D profile of the head
# It consists of a circle and a tapered section leading to the shaft.
head_sketch = (cq.Workplane("XY")
               .moveTo(-head_radius, 0) # Start somewhat left
               .circle(head_radius)     # The main round part
               # We need to blend this circle into the shaft connection point
               # A simple convex hull or lofting approach is robust
               )

# Let's make the head more specifically shaped like the image (teardrop)
# We can use a hull of two circles: the main head circle and a smaller circle at the shaft connection.
head_circle = (cq.Workplane("XY")
               .circle(head_radius)
               .extrude(head_thickness)
               )

# We create a transition shape to blend the head circle to the shaft
# The image shows a smooth transition.
# Let's define points for a custom polygon that mimics the tangent lines.
transition_length = head_radius * 1.5
transition_width = shaft_diameter

pts = [
    (0, head_radius),                 # Top of big circle
    (transition_length, transition_width/2), # Top of shaft connection
    (transition_length, -transition_width/2),# Bottom of shaft connection
    (0, -head_radius)                 # Bottom of big circle
]

head_transition = (cq.Workplane("XY")
                   .moveTo(0, head_radius)
                   .lineTo(transition_length, transition_width/2)
                   .lineTo(transition_length, -transition_width/2)
                   .lineTo(0, -head_radius)
                   .close()
                   .extrude(head_thickness)
                   )

# Combine the circle and the transition wedge
# And position it correctly. The shaft starts at x=0.
# The head should be to the left of x=0 mostly.
head_solid = head_circle.union(head_transition)

# Now assemble everything relative to a common origin.
# Let's say the connection point between shaft and head is at (0,0,0).

# Re-positioning for final assembly
# Move head so its "transition" end is at origin
head_final = head_solid.translate((-head_radius, 0, -head_thickness/2))

# Shaft starts at origin and goes +X
shaft_final = (cq.Workplane("YZ")
               .circle(shaft_diameter/2)
               .extrude(shaft_length)
               .translate((head_radius * 0.5, 0, 0)) # Overlap slightly with head
               )

# Handle starts at end of shaft
handle_final = (cq.Workplane("XY")
                .box(handle_length, handle_width, handle_thickness)
                .edges("|X")
                .chamfer(handle_chamfer)
                .translate((shaft_length + head_radius * 0.5 + handle_length/2, 0, 0))
                )

# Combine all parts
result = head_final.union(shaft_final).union(handle_final)

# Refinement: The image shows the head might be slightly tapered or chamfered.
# Let's apply fillets to the head-shaft junction and the head edges.
try:
    result = result.edges(cq.selectors.NearestToPointSelector((-head_radius, 0, head_thickness/2))).fillet(1.0)
    result = result.edges(cq.selectors.NearestToPointSelector((-head_radius, 0, -head_thickness/2))).fillet(1.0)
except:
    pass # If fillet fails due to geometry complexity, skip

# Adjust the head orientation to match the image (flat part vertical or horizontal?)
# In the image, the flat faces of the handle are roughly parallel to the flat faces of the head.
# The current model aligns them on the XY plane (flat faces normal to Z). This matches.

# Final check of positions
# Head is centered roughly at -head_radius
# Shaft runs from approx 0 to 50
# Handle runs from 50 to 110