import cadquery as cq

# Parameters derived from visual estimation of the rectangular link
length = 100.0       # Total length of the plate
width = 30.0         # Width (vertical height in the image)
thickness = 6.0      # Thickness of the plate
hole_diameter = 8.0  # Diameter of the through holes
hole_spacing = 80.0  # Distance between hole centers (centered on the part)

# Create the base rectangular geometry centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# Cut the two holes through the thickness of the plate
# We select the top face (>Z), create a workplane, define the hole centers, and cut
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_spacing / 2.0, 0), 
        (hole_spacing / 2.0, 0)
    ])
    .hole(hole_diameter)
)