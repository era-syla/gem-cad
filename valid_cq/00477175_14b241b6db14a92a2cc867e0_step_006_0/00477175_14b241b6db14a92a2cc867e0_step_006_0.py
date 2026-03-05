import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the cylinder
radius = 20.0   # Radius of the cylinder

# Create the solid geometry
# Using the YZ plane to draw the circular profile and extruding along the X-axis
# to match the horizontal orientation shown in the image.
result = cq.Workplane("YZ").circle(radius).extrude(length)