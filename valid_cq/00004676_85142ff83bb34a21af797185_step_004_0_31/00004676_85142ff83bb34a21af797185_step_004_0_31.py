import cadquery as cq
import math

# Parametric dimensions for the socket head cap screw
shaft_dia = 4.0
shaft_len = 35.0
head_dia = 7.5
head_len = 4.5
hex_af = 3.0
hex_depth = 2.5
tip_chamfer = 0.4
head_chamfer = 0.4
junction_fillet = 0.4

# Calculate circumscribed diameter for the hex socket polygon
hex_dia = hex_af * 2.0 / math.sqrt(3)

# Build the solid model
result = (
    cq.Workplane("XY")
    # Base head cylinder
    .circle(head_dia / 2.0)
    .extrude(head_len)
    
    # Chamfer top edge of the head
    .edges(">Z").chamfer(head_chamfer)
    
    # Add the unthreaded shaft extending downwards
    .faces("<Z")
    .workplane()
    .circle(shaft_dia / 2.0)
    .extrude(shaft_len)
    
    # Chamfer the bottom tip of the shaft
    .edges("<Z").chamfer(tip_chamfer)
    
    # Fillet the junction between head and shaft (located at Z=0)
    .edges(cq.NearestToPointSelector((shaft_dia / 2.0, 0.0, 0.0))).fillet(junction_fillet)
    
    # Cut the hex socket into the top face
    .faces(">Z")
    .workplane()
    .polygon(6, hex_dia)
    .cutBlind(-hex_depth)
)