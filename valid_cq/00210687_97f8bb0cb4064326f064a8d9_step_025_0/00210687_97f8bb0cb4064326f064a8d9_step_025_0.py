import cadquery as cq

# Parametric dimensions based on visual estimation of the image
# The object is a simple rectangular plate/panel
panel_width = 50.0    # Width of the panel
panel_height = 80.0   # Height of the panel
panel_thickness = 4.0 # Thickness of the panel

# Create the solid geometry
# box(length, width, height) creates a rectangular prism. 
# We orient it such that width corresponds to x, height to y, and thickness to z.
result = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)