import cadquery as cq

# Define parametric dimensions
# Main body dimensions
height = 100.0
width = 20.0  # X dimension
depth = 20.0  # Y dimension

# Notch dimensions (located on top edge)
notch_width = 2.0
notch_depth = 2.0
notch_height = 2.0

# Create the main rectangular prism
# Using centered=False for Z so it grows upwards from the XY plane,
# centered=True for X and Y for symmetry around the origin.
result = cq.Workplane("XY").box(width, depth, height, centered=(True, True, False))

# Create the small notch on the top face
# We need to position a cutting tool or select the edge/face to cut.
# Looking at the image, the notch is on one of the top edges.
# Let's target the top face, and cut a small rectangle on one of the edges.

# Move to the top face
# Select the top face (Z max)
# Create a sketch for the cut
result = (
    result.faces(">Z")
    .workplane()
    # Move to the edge. Let's pick the "back" edge (Y max) or side edge.
    # Based on the isometric view, it looks like the back-left corner/edge area.
    # Let's put it on the edge at Y=depth/2.
    .center(0, depth/2) 
    .rect(notch_width, notch_depth * 2) # Create a rectangle that overlaps the edge
    .cutBlind(-notch_height) # Cut down into the object
)

# Alternatively, a more specific positioning if it's a corner notch or mid-edge:
# The image shows it's likely centered on one of the top edges.
# Let's refine the notch position to match the image better. 
# It looks like a tiny notch on the "back" edge (relative to the view).

# Reset and try a cleaner approach for the specific visual match
result = cq.Workplane("XY").box(width, depth, height)

# Create a small cutting box positioned at the top edge
# Notch position: Top face (Z=height/2), Back edge (Y=depth/2), Center X (X=0)
notch = (
    cq.Workplane("XY")
    .workplane(offset=height/2) # Move to top
    .center(0, depth/2)         # Move to back edge
    .box(notch_width, notch_depth, notch_height*2, centered=(True, True, True))
)

# Perform the cut
result = result.cut(notch)