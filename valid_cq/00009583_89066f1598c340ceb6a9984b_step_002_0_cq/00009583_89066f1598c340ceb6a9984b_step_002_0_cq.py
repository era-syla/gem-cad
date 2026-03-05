import cadquery as cq

# Parametric dimensions
main_cylinder_radius = 15.0
main_cylinder_height = 40.0

base_flange_radius = 18.0
base_flange_thickness = 3.0

bottom_pin_radius = 5.0
bottom_pin_height = 8.0

fillet_radius = 1.0

# Create the main cylinder
main_body = cq.Workplane("XY").circle(main_cylinder_radius).extrude(main_cylinder_height)

# Create the base flange at the bottom of the main cylinder
# We select the bottom face ("<Z"), draw the larger circle, and extrude downwards
flange = (
    main_body.faces("<Z")
    .workplane()
    .circle(base_flange_radius)
    .extrude(base_flange_thickness)
)

# Create the small pin at the very bottom
# We select the new bottom face (the bottom of the flange), draw the small circle, and extrude
# Note: extrude is positive because the workplane normal on the bottom face points away from the solid
result = (
    flange.faces("<Z")
    .workplane()
    .circle(bottom_pin_radius)
    .extrude(bottom_pin_height)
)

# Add the fillet between the main cylinder and the flange
# We select the edge that is formed by the intersection of the main cylinder and the flange.
# This edge is on the top face of the flange, specifically the circle corresponding to the main cylinder radius.
# A robust way is to select edges on the top face of the flange that match the main cylinder radius.
result = result.edges(
    cq.selectors.RadiusNthSelector(1) # Selects the second smallest radius edges (the main body connection)
).fillet(fillet_radius)

# Alternatively, selecting by position is often safer if dimensions are known:
# result = result.faces(">Z[1]").edges().fillet(fillet_radius) 
# But RadiusNthSelector is a good programmatic approach for this specific topology.