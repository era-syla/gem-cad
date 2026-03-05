import cadquery as cq

# Parametric dimensions
flange_diameter = 30.0    # Diameter of the wider base/flange
flange_thickness = 5.0    # Thickness of the flange part
body_diameter = 25.0      # Diameter of the main cylindrical body
body_length = 25.0        # Length of the main cylindrical body
fillet_radius = 1.0       # Radius for the fillet between flange and body

# Create the model
# 1. Start with the flange
result = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2.0)
    .extrude(flange_thickness)
)

# 2. Add the main cylindrical body on top of the flange
# Note: We select the top face (>Z) of the current geometry
result = (
    result.faces(">Z")
    .workplane()
    .circle(body_diameter / 2.0)
    .extrude(body_length)
)

# 3. Add a fillet at the junction between the flange and the body
# We select the edge that is at the intersection. 
# A robust way is to select edges near the Z-height of the flange top.
# The flange top is at Z = flange_thickness.
result = result.edges(cq.selectors.NearestToPointSelector((0, body_diameter/2, flange_thickness))).fillet(fillet_radius)