import cadquery as cq

# Parametric dimensions
length = 60.0    # Length of the plate
width = 30.0     # Width of the plate
thickness = 3.0  # Thickness of the plate
hole_diam = 6.0  # Diameter of the holes
hole_dist = 30.0 # Distance between hole centers (centered on the plate)

# Create the base rectangular plate
# We center it at the origin to make hole placement symmetric
base_plate = cq.Workplane("XY").box(length, width, thickness)

# Create the two holes
# Method: Select the top face, push points for hole centers, and cut holes
result = (
    base_plate
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_dist / 2, 0), (hole_dist / 2, 0)])
    .hole(hole_diam)
)