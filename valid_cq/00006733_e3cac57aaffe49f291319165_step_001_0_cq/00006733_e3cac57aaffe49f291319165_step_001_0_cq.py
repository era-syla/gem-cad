import cadquery as cq

# Parametric dimensions
cylinder_diameter = 50.0
cylinder_length = 50.0
hole_diameter = 5.0

# Create the main cylinder
main_body = cq.Workplane("XY").circle(cylinder_diameter / 2).extrude(cylinder_length)

# Create the center hole
# We select the face on the XY plane (bottom) or we can just cut through the whole object from the same workplane
# Since we extruded along Z, "XY" is the base.
result = main_body.faces(">Z").workplane().hole(hole_diameter)

# Alternatively, a more robust way to ensure it goes all the way through if intended:
# result = main_body.faces(">Z").workplane().circle(hole_diameter / 2).cutThruAll() 
# But looking at the simple shading, .hole() is cleaner and implies a standard drilling operation.

# Final geometry
result = result