import cadquery as cq

# Geometric Parameters
head_diameter = 24.0
head_height = 12.0
shaft_diameter = 12.0
shaft_length = 36.0
neck_fillet_radius = 1.5
tip_chamfer_size = 1.0

# Model Generation
result = (
    cq.Workplane("XY")
    # Create the cylindrical head
    .circle(head_diameter / 2.0)
    .extrude(head_height)
    
    # Select the top face of the head to draw the shaft
    .faces(">Z")
    .workplane()
    
    # Create the cylindrical shaft
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # Select the edge where the shaft meets the head
    # We select the edge closest to a point on the shaft's base circumference
    .edges(cq.NearestToPointSelector((shaft_diameter / 2.0, 0, head_height)))
    .fillet(neck_fillet_radius)
    
    # Select the circular edge at the very top (tip) of the shaft
    .faces(">Z")
    .edges()
    .chamfer(tip_chamfer_size)
)