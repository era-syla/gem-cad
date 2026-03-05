import cadquery as cq

# Parametric dimensions
length = 100.0
width = 30.0
height = 15.0
wall_thickness = 2.0
fillet_radius = 8.0

# Create the 3D model
# 1. Start with a solid rectangular block
# 2. Fillet the bottom longitudinal edges to create the rounded hull shape
# 3. Shell the object from the top face to create the internal cavity
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|X and <Z")     # Select edges parallel to X-axis at the bottom (min Z)
    .fillet(fillet_radius)
    .faces(">Z")            # Select the top face
    .shell(-wall_thickness) # Create hollow shell with inward thickness
)