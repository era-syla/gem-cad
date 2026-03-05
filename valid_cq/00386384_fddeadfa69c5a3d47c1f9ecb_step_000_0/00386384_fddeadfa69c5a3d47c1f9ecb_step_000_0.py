import cadquery as cq

# Parametric dimensions based on visual estimation
shaft_diameter = 4.0
shaft_length = 80.0
head_diameter = 7.0
head_height = 4.0
tip_chamfer_size = 0.5

# Create the model
# 1. Start with the head (cylinder)
result = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(head_height)

# 2. Add the shaft
# Select the top face of the head, create a workplane, draw the shaft circle, and extrude
result = (
    result.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# 3. Detail the tip
# Select the face at the very end of the shaft (highest Z) and chamfer its edges
result = result.faces(">Z").edges().chamfer(tip_chamfer_size)