import cadquery as cq

# Define parameters for the plate
length = 100.0  # Length of the plate
width = 100.0   # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the plate
# Using a box is the simplest way to create this rectangular prism shape.
# centered=(True, True, False) centers the plate on X and Y, 
# but starts Z from 0 going up, which is a common convention.
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, using rectangle and extrude:
# result = cq.Workplane("XY").rect(length, width).extrude(thickness)