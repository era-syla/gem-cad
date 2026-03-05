import cadquery as cq

# Define parametric dimensions
length = 200.0  # Length of the bar
width = 10.0    # Width of the bar
thickness = 5.0 # Thickness of the bar

# Create the rectangular bar geometry
result = cq.Workplane("XY").box(length, width, thickness)