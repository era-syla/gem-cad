import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 80.0           # Total length of the cylinder
outer_diameter = 30.0   # Outer diameter of the cylinder body
fillet_radius = 8.0     # Radius of the rounding on the ends (less than outer_radius for a flat face)
hole_diameter = 8.0     # Diameter of the central through-hole

# Create the CAD model
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(length)
    .faces("<Z or >Z")    # Select the bottom and top faces
    .edges()              # Select the edges of those faces
    .fillet(fillet_radius) # Apply fillet to create the rounded ends
    .faces(">Z")          # Select the top face to place the hole
    .workplane()
    .hole(hole_diameter)  # Cut the hole through the entire part
)