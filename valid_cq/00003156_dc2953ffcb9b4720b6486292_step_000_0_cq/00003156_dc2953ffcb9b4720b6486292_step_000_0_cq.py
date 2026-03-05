import cadquery as cq

# Define parameters for the box dimensions
# These can be adjusted to change the size of the rectangular prism
length = 50.0  # X-axis dimension
width = 30.0   # Y-axis dimension
height = 20.0  # Z-axis dimension

# Create the rectangular prism (box)
# cq.Workplane("XY") creates a workplane on the XY plane.
# .box(length, width, height) creates a centered box with the specified dimensions.
# If you want it based on a corner, you could add .center(False, False, False) beforehand 
# or translate it afterwards, but centering is standard in CadQuery.
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want the box to sit on top of the XY plane (Z > 0):
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))