import cadquery as cq

# Parametric dimensions based on the visual estimation of the image
height = 70.0               # Total height of the cylinder
outer_diameter = 30.0       # Outer diameter of the main body
inner_diameter = 18.0       # Diameter of the through-hole
top_fillet_radius = 2.5     # Radius of the rounded top edge
bottom_chamfer_size = 2.0   # Size of the chamfered bottom edge

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the base solid cylinder
    .circle(outer_diameter / 2.0)
    .extrude(height)
    
    # 2. Fillet the top edge
    # Selecting faces(">Z") grabs the top face. 
    # .edges() on a solid cylinder's top face selects the single outer rim.
    .faces(">Z").edges().fillet(top_fillet_radius)
    
    # 3. Chamfer the bottom edge
    # Selecting faces("<Z") grabs the bottom face.
    .faces("<Z").edges().chamfer(bottom_chamfer_size)
    
    # 4. Create the hollow core
    # We establish a workplane on the top face and cut a hole through the entire part.
    # Doing this last ensures the fillet/chamfer logic doesn't have to distinguish between inner/outer circles.
    .faces(">Z").workplane().hole(inner_diameter)
)