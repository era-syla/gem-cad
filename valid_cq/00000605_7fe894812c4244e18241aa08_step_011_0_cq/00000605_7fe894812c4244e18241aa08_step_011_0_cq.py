import cadquery as cq

# Parametric dimensions for the box
length = 40.0
width = 20.0
height = 15.0

# Create a simple box using the Workplane and box operation
# This centers the box at the origin for simpler positioning
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want it resting on the XY plane:
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))