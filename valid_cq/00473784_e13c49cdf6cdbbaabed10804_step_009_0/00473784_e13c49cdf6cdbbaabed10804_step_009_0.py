import cadquery as cq

# Geometric parameters for the model
length = 400.0      # Total length of the bar
width = 20.0        # Width of the square profile
height = 20.0       # Height of the square profile
hole_diameter = 5.0 # Diameter of the central hole

# Create the base geometry: a solid rectangular bar
# The box is centered at the origin, aligned along the X-axis
result = cq.Workplane("XY").box(length, width, height)

# Create the hole feature
# Select the top face (+Z), create a workplane, and cut a hole through the part
result = result.faces("+Z").workplane().hole(hole_diameter)