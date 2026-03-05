import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the box
width = 50.0    # Width of the box
height = 40.0   # Height of the box
fillet_radius = 2.0 # Radius of the fillets

# Create the base rectangular prism
# We center it on X and Y, but keep Z starting from 0 for easier visualization
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# Apply fillets
# Based on the image, the top face edges and vertical edges are filleted.
# This often implies all edges are filleted or just the vertical ones and the top loop.
# Let's look closer at the image:
# - The top perimeter is clearly rounded.
# - The vertical corners are clearly rounded.
# - The bottom perimeter looks sharp in this specific rendering style, 
#   but often in such simple blocks, it's either just vertical+top or all.
#   However, a common "enclosure" or "cap" style often fillets vertical edges and the top face edges.
#   Let's select vertical edges and the top face edges.

# Select vertical edges
result = result.edges("|Z").fillet(fillet_radius)

# Select top face edges
# After filleting verticals, the top face is still a single face (mostly), 
# but the edge loop is now tangent continuous.
result = result.faces(">Z").edges().fillet(fillet_radius)

# If the bottom was also supposed to be filleted, we would just do result.edges().fillet(radius)
# But strictly following the visual cue where bottom lines look sharp compared to the top highlight:
# This generates a box with rounded vertical corners and rounded top edges.