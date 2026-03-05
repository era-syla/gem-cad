import cadquery as cq

# Parametric dimensions for the model
circle_radius = 25.0
handle_width = 20.0
handle_length = 55.0  # Length from the circle center downwards
thickness = 10.0
fillet_radius = 5.0

# 1. Create the top circular section
# We draw on the XY plane and extrude along Z
head = cq.Workplane("XY").circle(circle_radius).extrude(thickness)

# 2. Create the rectangular handle section
# The handle is centered horizontally (X=0).
# Vertically, we want it to extend from the center (Y=0) downwards.
# We move the workplane center to (0, -handle_length/2) and draw a rectangle 
# of height 'handle_length', so it spans from Y=0 to Y=-handle_length.
handle = (
    cq.Workplane("XY")
    .center(0, -handle_length / 2)
    .rect(handle_width, handle_length)
    .extrude(thickness)
)

# 3. Combine the two shapes into one solid
result = head.union(handle)

# 4. Apply fillets to the bottom corners
# We select edges that are parallel to the Z axis (|Z) to get the vertical edges,
# and use the <Y selector to find the ones at the lowest Y coordinate (the bottom of the handle).
result = result.edges("|Z and <Y").fillet(fillet_radius)