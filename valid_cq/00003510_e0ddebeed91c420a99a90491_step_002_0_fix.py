import cadquery as cq

# Main cylinder body
main_radius = 20
main_height = 40

# Create the main vertical cylinder
body = cq.Workplane("XY").cylinder(main_height, main_radius)

# Add a cap/flange on top
cap = cq.Workplane("XY").workplane(offset=main_height/2).circle(main_radius * 0.85).extrude(3)

# Side port 1 - going in the +X direction (right side), positioned in upper area
port1_radius = 8
port1_length = 15
port1_z = 5

side1 = (cq.Workplane("YZ")
         .workplane(offset=main_radius)
         .center(0, port1_z)
         .circle(port1_radius)
         .extrude(port1_length))

# Side port 2 - going in the -X direction (left side), positioned lower
port2_radius = 8
port2_length = 15
port2_z = -8

side2 = (cq.Workplane("YZ")
         .workplane(offset=-main_radius)
         .center(0, port2_z)
         .circle(port2_radius)
         .extrude(-port2_length))

# Combine all parts
result = body.union(cap).union(side1).union(side2)

# Add fillets to smooth the intersections - select edges at port junctions
# Use small fillet on top edge of cap
result = result.edges(">Z").fillet(1.5)