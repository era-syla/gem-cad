import cadquery as cq

# Define parametric dimensions
# Based on visual estimation, this is a long, thin rectangular bar.
length = 200.0  # Total height of the bar
width = 5.0     # Width of the bar (facing the viewer more directly)
thickness = 2.0 # Thickness of the bar (the very thin side profile)

# Create the 3D model
# We create a simple box centered on the XY plane but extending in Z
result = cq.Workplane("XY").box(width, thickness, length)

# Alternatively, if the image implies a specific orientation where 'length' is along Y:
# result = cq.Workplane("XY").box(width, length, thickness)
# But a vertical standing bar usually implies Z-axis height.

# Export or display is handled by the platform using the 'result' variable