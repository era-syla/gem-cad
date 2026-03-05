import cadquery as cq

# Define parameters for the dimensions of the rectangular bar
length = 100.0  # Length of the bar
width = 25.0    # Width of the bar
thickness = 5.0 # Thickness of the bar

# Create the rectangular prism (box) on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)