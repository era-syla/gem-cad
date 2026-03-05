import cadquery as cq

# Parametric dimensions based on visual estimation of the rectangular panel
height = 60.0      # Vertical dimension
width = 40.0       # Horizontal dimension
thickness = 3.0    # Depth/Thickness dimension

# Create the 3D model
# We create a box centered on the XY plane.
# To match the upright orientation shown in the image:
# - X axis corresponds to the width
# - Y axis corresponds to the thickness
# - Z axis corresponds to the height
result = cq.Workplane("XY").box(width, thickness, height)