import cadquery as cq

# Parametric dimensions
# Based on visual estimation, the object is a rectangular prism (box)
# It appears taller than it is wide or deep.
# Let's assume a square base for simplicity, but allow for rectangularity.
length = 50.0  # X-axis dimension
width = 50.0   # Y-axis dimension
height = 100.0 # Z-axis dimension (appears roughly 2x the base width)

# Create the solid geometry
# We use Workplane("XY") to start drawing on the ground plane
# box() creates a centered box by default, which is usually convenient
result = cq.Workplane("XY").box(length, width, height)

# If you preferred the box to sit on top of the plane rather than be centered:
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))