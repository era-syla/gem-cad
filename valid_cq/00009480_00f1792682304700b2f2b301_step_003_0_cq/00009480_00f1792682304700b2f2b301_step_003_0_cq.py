import cadquery as cq

# Parametric dimensions
rod_length = 300.0   # Main length of the rod
rod_diameter = 6.0   # Diameter of the main rod body
tip_diameter = 3.0   # Diameter of the reduced tip (e.g., for threading)
tip_length = 8.0     # Length of the reduced tip section

# Create the main rod body
# We start by drawing a circle and extruding it
rod = cq.Workplane("XY").circle(rod_diameter / 2).extrude(rod_length)

# Create the reduced tip on top
# We select the top face of the rod, draw a smaller circle, and extrude it
tip = (
    rod.faces(">Z")
    .workplane()
    .circle(tip_diameter / 2)
    .extrude(tip_length)
)

# If needed, a chamfer could be added to the transition or the very top, 
# but the image shows a fairly simple step. 
# Let's add a small chamfer to the very top for realism.
result = tip.faces(">Z").chamfer(0.5)

# Export or visualization usually happens outside this script in a CQ environment,
# but 'result' is the required variable name.