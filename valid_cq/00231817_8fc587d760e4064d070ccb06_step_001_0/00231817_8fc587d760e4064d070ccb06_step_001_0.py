import cadquery as cq

# Parametric dimensions
height = 80.0       # Total height of the cylinder
radius = 20.0       # Radius of the cylinder
fillet_radius = 4.0 # Radius of the fillet on top and bottom edges

# Create the cylinder and apply fillets
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
    .faces("+Z or -Z")  # Select the top and bottom faces
    .edges()            # Select the edges of those faces (the rims)
    .fillet(fillet_radius)
)