import cadquery as cq

# Define parameters for the sphere
radius = 50.0  # Radius of the sphere

# Create the sphere
# The cq.Workplane("XY").sphere(radius) creates a sphere centered at the origin
result = cq.Workplane("XY").sphere(radius)

# If you were running this in an environment like CQ-Editor, 
# you would typically inspect the result with:
# show_object(result)