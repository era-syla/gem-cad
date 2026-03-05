import cadquery as cq

# Define parametric dimensions
# Based on the visual proportions, the object is a long, thin rectangular prism.
# Let's assume a square cross-section for simplicity, as is common for stock material.
length = 100.0  # Total length of the bar
width = 5.0     # Width of the cross-section
height = 5.0    # Height of the cross-section

# Create the 3D model
# We create a box centered on the XY plane for convenience, but you can center it however you like.
# Using centered=True centers the box at the origin (0,0,0).
# Using centered=(True, True, False) would center X and Y but start Z at 0.
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want the long axis aligned with X as usually depicted:
# result = cq.Workplane("XY").box(length, width, height) 

# If you want to be very specific about alignment (e.g. corner at origin):
# result = cq.Workplane("XY").box(length, width, height, centered=False)