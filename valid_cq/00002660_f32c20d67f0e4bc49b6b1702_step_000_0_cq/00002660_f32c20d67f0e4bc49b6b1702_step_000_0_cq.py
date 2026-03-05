import cadquery as cq

# Define parametric dimensions for the box
# Based on visual estimation, the object is a rectangular prism
# appearing roughly square in plan view, with a thickness
length = 100.0  # Dimension along X axis
width = 100.0   # Dimension along Y axis
thickness = 30.0 # Dimension along Z axis (height)

# Create the box geometry
# centered=True centers the box at the origin (0,0,0) which is standard practice
result = cq.Workplane("XY").box(length, width, thickness, centered=True)

# Alternatively, if you want it sitting on the XY plane:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))