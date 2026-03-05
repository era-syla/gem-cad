import cadquery as cq

# Parametric dimensions
main_diameter = 20.0
main_height = 35.0
end_diameter = 14.0
end_height = 8.0

# Construct the model using a stack of extrusions
result = (
    cq.Workplane("XY")
    # 1. Create the bottom cylindrical section
    .circle(end_diameter / 2.0)
    .extrude(end_height)
    
    # 2. Create the central, larger cylindrical section
    # Select the top face (>Z) of the previous extrusion to start the next one
    .faces(">Z").workplane()
    .circle(main_diameter / 2.0)
    .extrude(main_height)
    
    # 3. Create the top cylindrical section
    # Again, select the top face of the current geometry
    .faces(">Z").workplane()
    .circle(end_diameter / 2.0)
    .extrude(end_height)
)