import cadquery as cq

# Define parameters for the rectangular bar
# Based on the image, the object is a long, thin, narrow rectangular prism
length = 100.0  # The long dimension
width = 10.0    # The "height" or width of the strip
thickness = 2.0 # The thin dimension

# Create the rectangular bar
# Workplane("XY") creates the sketch plane
# box() creates a centered rectangular prism
result = (
    cq.Workplane("XY")
    .box(length, thickness, width)
)

# Alternatively, if alignment to a corner is preferred (though center is standard):
# result = cq.Workplane("XY").box(length, thickness, width, centered=False)