import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the block
width = 30.0    # Width of the block
height = 15.0   # Height/Thickness of the block

# Create the solid geometry
# We create a box centered on the XY plane for convenience, but you can center it freely.
# The 'centered' parameter can be True, False, or a tuple of booleans (x, y, z).
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want it corner-aligned:
# result = cq.Workplane("XY").box(length, width, height, centered=False)