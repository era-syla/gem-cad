import cadquery as cq

# Parametric dimensions
head_diameter = 40.0
head_thickness = 5.0
shaft_diameter = 15.0
shaft_length = 15.0
hole_diameter = 8.0
fillet_radius = 4.0

# Create the main body
# 1. Start with the shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Add the head on top of the shaft
# The shaft was extruded upwards (positive Z), so we work on the top face
head = (
    shaft.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_thickness)
)

# 3. Create the through-hole
# This cuts through the entire object
body_with_hole = head.faces(">Z").workplane().hole(hole_diameter)

# 4. Add the large fillet/countersink style rounding on the top hole edge
# Select the top circular edge of the hole
result = body_with_hole.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).fillet(fillet_radius)

# Note: The RadiusNthSelector(0) is used to select the smallest radius edge on the top face,
# which corresponds to the hole's edge.