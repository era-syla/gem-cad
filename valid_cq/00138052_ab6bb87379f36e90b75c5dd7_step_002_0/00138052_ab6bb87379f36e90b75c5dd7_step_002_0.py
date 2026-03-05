import cadquery as cq

# Parametric dimensions for the model
head_diameter = 24.0
head_thickness = 10.0
shaft_diameter = 12.0
shaft_length = 40.0
fillet_radius = 2.0

# Generate the geometry
result = (
    cq.Workplane("XY")
    # Create the head cylinder
    .circle(head_diameter / 2.0)
    .extrude(head_thickness)
    # Select the top face of the head to draw the shaft
    .faces(">Z")
    .workplane()
    # Create the shaft cylinder
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    # Select the edge at the junction of head and shaft for filleting
    # We select the edge closest to a point on the circumference of the shaft base
    .edges(cq.selectors.NearestToPointSelector((shaft_diameter / 2.0, 0, head_thickness)))
    .fillet(fillet_radius)
)