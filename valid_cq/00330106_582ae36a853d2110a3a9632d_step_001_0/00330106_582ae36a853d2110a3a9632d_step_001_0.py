import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
length = 100.0  # Length of the rectangular prism
width = 30.0    # Width of the rectangular prism
thickness = 10.0 # Thickness/Height of the rectangular prism

# Create the rectangular prism (box)
# Centered at the origin by default
result = cq.Workplane("XY").box(length, width, thickness)