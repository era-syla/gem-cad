import cadquery as cq

# Define parameters for the block dimensions
height = 100.0  # Height of the block
width = 100.0   # Width of the block
thickness = 10.0 # Thickness of the block

# Create the 3D block geometry
# We start with a workplane. Assuming the front face is on the XY plane.
# We create a box centered on the workplane.
result = cq.Workplane("XY").box(width, height, thickness)

# Alternatively, if you want it standing upright on the XZ plane as shown in the isometric view:
# result = cq.Workplane("XZ").box(width, height, thickness)
# However, the standard .box() call usually centers the object.
# Let's stick to the simplest representation which is a centered box.