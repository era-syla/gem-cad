import cadquery as cq

# Parameter definitions based on visual estimation
shaft_diameter = 10.0      # Base diameter for the shaft sections
stub_length = 10.0         # Length of the short stub (left side)
flange_diameter = 30.0     # Diameter of the large collar/flange
flange_thickness = 8.0     # Thickness of the flange
shaft_length = 50.0        # Length of the main shaft section
groove_diameter = 8.0      # Diameter of the groove cut
groove_width = 3.0         # Width of the groove
end_length = 15.0          # Length of the end section (right side)

# Generate the geometry by stacking extrusions along the Z-axis
result = (
    cq.Workplane("XY")
    # 1. Create the initial short stub
    .circle(shaft_diameter / 2.0)
    .extrude(stub_length)
    
    # 2. Create the flange on the top face of the stub
    .faces(">Z").workplane()
    .circle(flange_diameter / 2.0)
    .extrude(flange_thickness)
    
    # 3. Create the long main shaft section
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    
    # 4. Create the groove (reduced diameter section)
    .faces(">Z").workplane()
    .circle(groove_diameter / 2.0)
    .extrude(groove_width)
    
    # 5. Create the final end section
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(end_length)
)