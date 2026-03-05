import cadquery as cq

# Define parametric dimensions for the box
# Based on the visual aspect ratio:
# Height seems to be the largest dimension.
# Width (length) seems to be the second largest.
# Depth (thickness) seems to be the smallest.
height = 20.0
width = 15.0
depth = 8.0

# Create the solid block
# We use Workplane("XY") to start on the ground plane
# box() creates a centered box by default, which is usually convenient
result = cq.Workplane("XY").box(width, depth, height)

# If the goal is to align it exactly like the image where it sits "on" the plane,
# we might want to offset it, but a centered box is standard practice unless
# origin placement is specified.
# Just to be safe and clean, let's stick to the simplest valid solid geometry.