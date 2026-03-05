import cadquery as cq

# Define parameters for the rectangular prism
# Based on the image, the object is a tall, relatively thin rectangular block.
# Dimensions are estimated to represent the proportions seen in the image.
height = 100.0  # The vertical dimension
width = 40.0    # The wider horizontal dimension
thickness = 15.0 # The narrower horizontal dimension

# Create the rectangular prism (box)
# centered=True centers the box at the origin (0,0,0)
result = cq.Workplane("XY").box(width, thickness, height)

# Alternatively, if you want it standing on the XY plane:
# result = cq.Workplane("XY").box(width, thickness, height, centered=(True, True, False))