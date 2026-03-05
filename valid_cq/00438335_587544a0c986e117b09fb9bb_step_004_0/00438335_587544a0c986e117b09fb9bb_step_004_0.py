import cadquery as cq

# Parametric dimensions for the model
disc_diameter = 60.0
disc_thickness = 5.0
hole_diameter = 6.0
csk_diameter = 12.0
csk_angle = 90.0
fillet_radius = 1.5

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the base cylindrical disc
    .circle(disc_diameter / 2.0)
    .extrude(disc_thickness)
    
    # 2. Create the countersunk hole in the center of the top face
    .faces(">Z")
    .workplane()
    .cskHole(hole_diameter, csk_diameter, csk_angle)
    
    # 3. Fillet the top outer edge
    # Select the top face, then filter for the edge with the largest radius
    .faces(">Z")
    .edges(cq.selectors.RadiusNthSelector(-1))
    .fillet(fillet_radius)
)