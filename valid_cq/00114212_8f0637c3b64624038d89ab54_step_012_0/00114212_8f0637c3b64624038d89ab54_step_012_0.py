import cadquery as cq

# Parametric dimensions based on the visual proportions
# The object is a long, slender rectangular bar (prism)
width = 10.0    # X-axis dimension
depth = 10.0    # Y-axis dimension
height = 200.0  # Z-axis dimension (length of the bar)

# Create the rectangular prism centered at the origin
result = cq.Workplane("XY").box(width, depth, height)