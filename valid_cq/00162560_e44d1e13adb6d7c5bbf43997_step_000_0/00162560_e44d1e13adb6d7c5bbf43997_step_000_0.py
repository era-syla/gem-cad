import cadquery as cq

# Parametric dimensions based on visual aspect ratio
length = 100.0  # Longest dimension
width = 50.0    # Intermediate dimension
height = 30.0   # Shortest dimension

# Create the rectangular prism (box)
# Centered on the origin by default, which aligns with standard CAD practices
result = cq.Workplane("XY").box(length, width, height)