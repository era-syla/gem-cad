import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the box
width = 60.0    # Width of the box
thickness = 20.0 # Thickness/Height of the box

# Create the solid block
# We use Workplane("XY") to start drawing on the XY plane
# .box() creates a centered box by default, or we can use rect().extrude()
result = cq.Workplane("XY").box(length, width, thickness)

# If centering is not desired, one could use:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(False, False, False))