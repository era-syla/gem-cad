import cadquery as cq

# Dimensions
height = 100.0  # Height of the pillar
width = 10.0    # Width of the base (x-axis)
depth = 10.0    # Depth of the base (y-axis)

# Create the solid geometry
# We create a simple box centered on the XY plane but extending upwards in Z
result = cq.Workplane("XY").box(width, depth, height, centered=(True, True, False))