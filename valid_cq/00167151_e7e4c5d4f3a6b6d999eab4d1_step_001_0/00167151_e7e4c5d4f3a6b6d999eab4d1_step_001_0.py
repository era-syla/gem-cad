import cadquery as cq

# Parametric dimensions
length = 100.0  # Horizontal dimension
height = 80.0   # Vertical dimension
thickness = 5.0 # Depth dimension

# Create the rectangular plate (box)
# We orient the box so the large face corresponds to the X-Z plane, 
# with thickness along the Y axis to match the upright orientation in the image.
result = cq.Workplane("XY").box(length, thickness, height)