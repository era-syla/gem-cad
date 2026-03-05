import cadquery as cq

# Dimensions
# Based on visual estimation, the object is a tall rectangular prism
# with a square base.
width = 10.0   # X-axis dimension
depth = 10.0   # Y-axis dimension
height = 40.0  # Z-axis dimension

# Create the box
# Using centered=False so it sits on the XY plane, similar to typical CAD origin placement
# or centered=(True, True, False) to center X/Y but have Z start at 0.
# Let's use simple box centered at origin for simplicity.
result = cq.Workplane("XY").box(width, depth, height)