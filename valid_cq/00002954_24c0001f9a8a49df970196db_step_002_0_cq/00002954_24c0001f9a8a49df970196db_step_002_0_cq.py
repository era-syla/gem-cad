import cadquery as cq

# Parameters
width = 60.0    # Overall width of the block
depth = 30.0    # Overall depth of the block
height = 20.0   # Overall height of the block
top_radius = 20.0 # Radius of the top circular cutout
side_radius = 8.0 # Radius of the side semi-circular cutouts

# Create the base block
base = cq.Workplane("XY").box(width, depth, height)

# Create the top cutout
# We create a cylinder along the Y axis (depth direction) and cut it from the top
# The cylinder needs to be centered on the top face
top_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=-depth/2) # Start from the front face equivalent
    .moveTo(0, height/2)        # Move to the top center edge
    .circle(top_radius)
    .extrude(depth)             # Extrude through the depth
)

# Create the side cutouts
# These look like vertical cuts on the ends of the block.
# Let's re-examine the image. The cuts are on the short ends (width-wise).
# They are semi-circles removed from the left and right ends.
# Cylinder axis is Z (vertical).

# Left cutout
left_cutout = (
    cq.Workplane("XY")
    .moveTo(-width/2, 0)
    .circle(side_radius)
    .extrude(height)
)

# Right cutout
right_cutout = (
    cq.Workplane("XY")
    .moveTo(width/2, 0)
    .circle(side_radius)
    .extrude(height)
)

# Combine operations
# We start with the base, cut the top, then cut the sides.
# Note: For the top cutout, since I defined it on XZ plane and extruded in Y, 
# I need to ensure the orientation matches. 
# Let's simplify by using the cut method directly on the base workplane faces if possible,
# or just boolean subtraction which is robust.

result = (
    base
    .cut(top_cutout)
    .cut(left_cutout)
    .cut(right_cutout)
)

# To visualize nicely in an environment that supports it, or just export
# show_object(result)