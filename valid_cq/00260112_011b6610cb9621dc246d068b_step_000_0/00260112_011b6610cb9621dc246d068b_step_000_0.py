import cadquery as cq

# Parameters for the stepped shaft model
shaft_diameter = 20.0      # Diameter of the top and bottom sections
collar_diameter = 24.0     # Diameter of the middle enlarged section
bottom_height = 25.0       # Height of the bottom section
collar_height = 45.0       # Height of the middle section
top_height = 35.0          # Height of the top section

# Generate the geometry using stacked extrusions
result = (
    cq.Workplane("XY")
    # 1. Create the bottom shaft section
    .circle(shaft_diameter / 2.0)
    .extrude(bottom_height)
    
    # 2. Select the top face of the previous extrusion and create the collar
    .faces(">Z").workplane()
    .circle(collar_diameter / 2.0)
    .extrude(collar_height)
    
    # 3. Select the top face of the collar and create the top shaft section
    .faces(">Z").workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(top_height)
)