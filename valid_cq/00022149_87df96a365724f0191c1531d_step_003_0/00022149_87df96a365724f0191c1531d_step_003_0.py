import cadquery as cq

# Parametric dimensions
body_diameter = 50.0
body_height = 95.0
neck_diameter = 32.0
neck_height = 15.0
boss_diameter = 15.0
boss_height = 2.5
hole_diameter = 4.0
hole_depth = 10.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the main cylindrical body
    .circle(body_diameter / 2.0)
    .extrude(body_height)
    
    # Select the top face and create the neck
    .faces(">Z")
    .workplane()
    .circle(neck_diameter / 2.0)
    .extrude(neck_height)
    
    # Select the top face of the neck and create the small top boss
    .faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    
    # Select the very top face and cut the center hole
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutBlind(-hole_depth)
)