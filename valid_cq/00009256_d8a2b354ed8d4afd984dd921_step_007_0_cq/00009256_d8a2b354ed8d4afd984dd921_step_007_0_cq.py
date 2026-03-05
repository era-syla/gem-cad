import cadquery as cq

# Parametric dimensions
width = 100.0   # Width of the panel
height = 100.0  # Height of the panel
thickness = 2.0 # Thickness of the panel

# Create the solid geometry
# We create a box centered on X and Y, but sitting on Z=0, or centered on all.
# Based on the image, it's just a simple rectangular plate.
result = cq.Workplane("XY").box(width, thickness, height)

# If centering is desired differently (e.g., standing upright on XZ plane):
# result = cq.Workplane("XZ").box(width, height, thickness)
# But the .box command creates a box centered at the origin by default. 
# The visual shows a thin plate standing up.
# Let's adjust orientation to match the isometric-like view where the large face is visible.
# A box with (width, thickness, height) will create a standing panel.