import cadquery as cq

# Parametric dimensions based on visual estimation of the pin
head_diameter = 18.0
head_height = 8.0
shaft_diameter = 10.0
shaft_length = 30.0
neck_fillet_radius = 1.5
tip_chamfer_size = 1.0

# Create the base head cylinder
# We align the bottom of the head with the XY plane
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# Create the shaft extruding from the top face of the head
# We select the top face (>Z), create a new workplane, draw the shaft circle, and extrude
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# Apply a fillet at the transition between the head and the shaft (the neck)
# We select the edge using a geometric selector that finds the edge closest to 
# the point on the shaft's base perimeter.
# Point: (shaft_radius, 0, head_height)
neck_edge_selector = cq.selectors.NearestToPointSelector(
    (shaft_diameter / 2.0, 0, head_height)
)
result = result.edges(neck_edge_selector).fillet(neck_fillet_radius)

# Apply a chamfer to the very tip of the shaft
# Select the edges of the highest face in the Z direction
result = result.faces(">Z").edges().chamfer(tip_chamfer_size)