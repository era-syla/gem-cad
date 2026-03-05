import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the strip
width = 10.0    # Width of the strip
thickness = 1.0 # Thickness of the strip (very thin plate)

# Create the 3D model
# We create a simple box centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if the specific orientation in the image is desired (diagonal look), 
# we keep it axis-aligned as is standard for CAD parts, 
# but the view in the screenshot is just an isometric perspective of this flat bar.