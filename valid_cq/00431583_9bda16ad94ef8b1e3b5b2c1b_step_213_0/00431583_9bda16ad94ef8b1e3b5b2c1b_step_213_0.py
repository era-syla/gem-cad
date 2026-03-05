import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0  # Long dimension
height = 20.0   # Vertical dimension
thickness = 2.0 # Thickness dimension

# Create a rectangular prism (strip) 
# We orient it to stand vertically to match the isometric view: 
# Length along X, Thickness along Y, Height along Z
result = cq.Workplane("XY").box(length, thickness, height)