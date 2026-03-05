import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0  # Long dimension
width = 30.0    # Medium dimension
height = 15.0   # Short dimension

# Create the rectangular prism (box)
# Workplane("XY") aligns the base with the XY plane
# .box() centers the object at the origin by default
result = cq.Workplane("XY").box(length, width, height)