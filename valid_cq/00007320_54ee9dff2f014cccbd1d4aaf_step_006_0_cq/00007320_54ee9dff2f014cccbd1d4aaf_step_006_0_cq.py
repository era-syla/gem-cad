import cadquery as cq

# Define parameters for the shape
# The shape appears to be a loft between a circle and a rectangle.
height = 50.0  # Distance between the two profiles
circle_radius = 10.0  # Radius of the circular top profile
rect_width = 30.0     # Width of the rectangular bottom profile
rect_height = 20.0    # Height/depth of the rectangular bottom profile

# Create the circular profile on the top plane (offset by height)
# We create a workplane, offset it, draw a circle
top_profile = (
    cq.Workplane("XY")
    .workplane(offset=height)
    .circle(circle_radius)
)

# Create the rectangular profile on the base plane (XY)
# We create a workplane, draw a rectangle
bottom_profile = (
    cq.Workplane("XY")
    .rect(rect_width, rect_height)
)

# Loft the two profiles together to create the solid body
result = bottom_profile.add(top_profile).toPending().loft()

# If the orientation needs to match the image exactly (tilted), 
# we can rotate it, but usually, standard isometric views are assumed 
# for the model definition itself. The image shows a generic perspective.
# The code produces the canonical geometry.