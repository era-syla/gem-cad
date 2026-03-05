import cadquery as cq

# Parametric dimensions based on visual estimation
# The object is a simple rectangular prism (plate/panel)
panel_height = 150.0
panel_width = 100.0
panel_thickness = 10.0

# Create the 3D model
# We create a box centered on the XY plane.
# Orientation: Width along X, Thickness along Y, Height along Z to match the upright appearance.
result = cq.Workplane("XY").box(panel_width, panel_thickness, panel_height)