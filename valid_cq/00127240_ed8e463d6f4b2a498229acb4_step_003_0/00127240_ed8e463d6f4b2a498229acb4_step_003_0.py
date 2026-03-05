import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
# The object appears to be a tall, thin rectangular plate or panel
height = 100.0
width = 50.0
thickness = 5.0

# Create the 3D model
# We create a box centered at the origin.
# To match the upright orientation shown in the image (vertical rectangle):
# - X dimension corresponds to width
# - Y dimension corresponds to thickness
# - Z dimension corresponds to height
result = cq.Workplane("XY").box(width, thickness, height)