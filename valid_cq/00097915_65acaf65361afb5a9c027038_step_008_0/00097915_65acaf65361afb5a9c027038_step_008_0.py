import cadquery as cq

# Parametric definitions for the panel
panel_width = 150.0      # Width of the panel (X axis)
panel_height = 250.0     # Height of the panel (Y axis)
panel_thickness = 12.0   # Thickness of the panel (Z axis)
hole_diameter = 5.0      # Diameter of the corner mounting holes
hole_inset = 15.0        # Distance from the edge to the center of the hole

# Create the main rectangular body
# The box is centered at the origin
base = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)

# Calculate the spacing for the hole pattern based on dimensions and inset
x_spacing = panel_width - (2 * hole_inset)
y_spacing = panel_height - (2 * hole_inset)

# Select the top face, create a construction rectangle for positioning, and cut the holes
result = (
    base
    .faces(">Z")
    .workplane()
    .rect(x_spacing, y_spacing, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)