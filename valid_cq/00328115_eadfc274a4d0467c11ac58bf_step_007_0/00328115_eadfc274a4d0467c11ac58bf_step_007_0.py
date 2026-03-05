import cadquery as cq

# Parametric dimensions for the part
bar_height = 150.0      # Length of the main vertical section
bar_width = 8.0         # Width of the main section
bar_thickness = 3.0     # Thickness of the material
tenon_length = 4.0      # Length of the protruding tabs (tenons)
tenon_width = 4.0       # Width of the protruding tabs

# Generate the CAD model
# 1. Create the main rectangular body centered on the origin
# 2. Select the top face (>Z), draw the tenon profile, and extrude upwards
# 3. Select the bottom face (<Z), draw the tenon profile, and extrude downwards
result = (
    cq.Workplane("XY")
    .box(bar_width, bar_thickness, bar_height)
    .faces(">Z").workplane()
    .rect(tenon_width, bar_thickness)
    .extrude(tenon_length)
    .faces("<Z").workplane()
    .rect(tenon_width, bar_thickness)
    .extrude(tenon_length)
)