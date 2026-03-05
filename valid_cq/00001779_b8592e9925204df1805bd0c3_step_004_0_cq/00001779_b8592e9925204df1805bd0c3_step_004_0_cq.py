import cadquery as cq

# -- Parametric Dimensions --
length = 50.0       # Total length along X
width = 40.0        # Total width along Y
height_back = 40.0  # Height of the taller back side
height_front = 20.0 # Height of the shorter front side
fillet_radius = 3.0 # Radius for the rounded edges

# -- Modeling Strategy --
# The shape is essentially a block with a slanted top face.
# We can create a base sketch and extrude it, then cut the top, or
# create a profile from the side and extrude it.
# A side profile extrusion (trapezoid) seems most straightforward.
#
# Profile in Y-Z plane:
# (0,0) -> (width, 0) -> (width, height_back) -> (0, height_front) -> close

# 1. Create the base solid
# Extruding a trapezoid along X is one way, but the image shows the slope 
# going "down" towards the viewer/right. Let's orient it to match the view.
#
# Let's assume:
# - X axis is roughly right/forward
# - Y axis is roughly left/back
# - Z axis is up
#
# Looking at the image:
# There is a vertical face on the left.
# There is a vertical face on the back (implied).
# There is a slanted face on top.
# There is a vertical face on the right, but it's shorter than the left one.
#
# Let's try sketching on the YZ plane and extruding along X.
# If we sketch a trapezoid on YZ:
# P1(0,0), P2(width, 0), P3(width, height_back), P4(0, height_front)
# And extrude this by 'length'.

# Create the trapezoidal profile
result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, height_back)   # Tall back edge
    .lineTo(0, height_front)      # Short front edge
    .close()
    .extrude(length)
)

# The extrusion happens along positive X.
# Based on the image, the "pointy" corner (tallest, furthest back) is rounded.
# Actually, nearly all visible edges seem to have a fillet.
# Let's select all edges and apply a fillet. 
# Looking closely, the vertical edges and the top loop edges are rounded. 
# The bottom edges might be sharp or have a smaller fillet, but usually in these 
# types of simple block models, it's a global fillet or specific edge selection.
# The image shows a very uniform rounding on the visible corners.

result = result.edges().fillet(fillet_radius)

# Note: The orientation might need rotation to match the specific isometric view 
# in the screenshot perfectly, but the topology is a trapezoidal prism.
# The code creates the solid geometry.