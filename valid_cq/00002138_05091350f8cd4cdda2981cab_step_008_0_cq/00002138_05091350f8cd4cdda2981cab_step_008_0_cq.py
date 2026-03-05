import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
height = 15.0    # Height of the cylinder
fillet_radius = 2.0 # Radius of the fillet on the top edge

# Create the base cylinder
result = cq.Workplane("XY").circle(diameter / 2).extrude(height)

# Apply fillet to the top edge
# We select the faces in the Z direction (top face) and then get its outer wire
result = result.faces(">Z").edges().fillet(fillet_radius)