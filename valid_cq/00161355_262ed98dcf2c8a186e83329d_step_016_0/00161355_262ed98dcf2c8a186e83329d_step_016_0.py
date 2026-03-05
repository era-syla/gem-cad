import cadquery as cq

# Parameters for the geometry
tube_length = 200.0
tube_width = 30.0
tube_height = 30.0
wall_thickness = 2.0
fillet_radius = 3.0
boss_diameter = 15.0
boss_height = 10.0

# Generate the model
result = (
    cq.Workplane("XY")
    # 1. Create the main rectangular solid
    .box(tube_length, tube_width, tube_height)
    
    # 2. Round the longitudinal edges to create the tube profile
    .edges("|X")
    .fillet(fillet_radius)
    
    # 3. Add the cylindrical boss to the top face
    .faces(">Z")
    .workplane()
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    
    # 4. Shell the object to make it hollow
    # We select the top face of the boss (>Z) and the two ends of the tube (>X, <X)
    # to be removed, creating the openings.
    .faces(">Z or >X or <X")
    .shell(-wall_thickness)
)