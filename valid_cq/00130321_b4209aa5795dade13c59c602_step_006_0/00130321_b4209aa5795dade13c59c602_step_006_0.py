import cadquery as cq

# Parametric dimensions
head_diameter = 12.0      # Diameter of the cylindrical ends
head_length = 12.0        # Length of the cylindrical ends
shaft_diameter = 5.0      # Diameter of the connecting rod
shaft_length = 60.0       # Length of the connecting rod

# Create the model using sequential extrusion
result = (
    cq.Workplane("XY")
    # 1. Create the first head
    .circle(head_diameter / 2.0)
    .extrude(head_length)
    
    # 2. Select the top face and create the connecting shaft
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # 3. Select the top face of the shaft and create the second head
    .faces(">Z").workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_length)
)