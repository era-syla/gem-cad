import cadquery as cq

# Parametric dimensions based on visual estimation
base_width = 100.0     # Width of the wider back section
base_depth = 60.0      # Depth of the wider back section
thickness = 10.0       # Thickness of the plate
tab_width = 40.0       # Width of the narrower front section
tab_length = 40.0      # Length of the protrusion

# Create the main body (the wider rectangle)
# We center it on the XY plane for symmetry
result = cq.Workplane("XY").box(base_width, base_depth, thickness)

# Create the tab (protrusion)
# 1. Select the front face (negative Y direction)
# 2. Create a new workplane on that face
# 3. Draw a rectangle representing the cross-section of the tab
# 4. Extrude it outwards
result = (
    result
    .faces("<Y")
    .workplane()
    .center(0, 0)  # Ensure we are centered on the face
    .rect(tab_width, thickness)
    .extrude(tab_length)
)