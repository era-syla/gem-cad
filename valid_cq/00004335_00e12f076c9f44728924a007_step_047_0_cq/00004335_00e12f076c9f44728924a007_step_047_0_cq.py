import cadquery as cq

# Define parameters for the box dimensions
# These are estimated based on the visual proportions of the image
length = 100.0  # X-axis dimension
width = 60.0    # Y-axis dimension
height = 40.0   # Z-axis dimension

# Create the box
# We center it on the XY plane for convenience, but the Z starts at 0 and goes up
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want it resting on the XY plane (z=0 is bottom face):
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# The default .box() centers on all axes, which is fine for the requested geometry representation.