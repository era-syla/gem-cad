import cadquery as cq

# Parametric Dimensions
shaft_diameter = 10.0
shaft_length = 35.0
head_diameter = 18.0
head_height = 6.0
head_fillet = 5.0  # Creates the domed profile of the head
tip_chamfer = 1.0

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # 1. Create the Head
    .circle(head_diameter / 2.0)
    .extrude(head_height)
    # Round the top edge to form the button/dome head shape
    .edges(">Z")
    .fillet(head_fillet)
    
    # 2. Create the Shaft
    # Select the bottom face of the head
    .faces("<Z")
    .workplane()
    # Draw and extrude the shaft
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # 3. Detail the Shaft Tip
    # Select the furthest face in the extrusion direction (negative Z)
    .faces("<Z")
    .edges()
    .chamfer(tip_chamfer)
)