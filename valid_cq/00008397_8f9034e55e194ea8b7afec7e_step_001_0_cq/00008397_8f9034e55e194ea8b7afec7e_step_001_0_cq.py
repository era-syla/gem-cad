import cadquery as cq

# Parameters for the long rectangular bar
length = 200.0  # Overall length of the bar
width = 20.0    # Width of the bar
thickness = 10.0 # Thickness/Height of the bar

# Parameters for the holes
hole_diameter = 8.0     # Diameter of the through holes
counterbore_diameter = 14.0 # Diameter of the counterbore
counterbore_depth = 4.0     # Depth of the counterbore
hole_spacing_from_end = 15.0 # Distance from the end edge to the hole center

# Calculate the distance between hole centers based on spacing from ends
hole_x_position = length / 2 - hole_spacing_from_end

# Create the base rectangular block
# We center the part at the origin for easier hole placement
base = cq.Workplane("XY").box(length, width, thickness)

# Create the holes with counterbores
# We select the top face to start the holes
# We push points to the locations of the two holes
result = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(-hole_x_position, 0), (hole_x_position, 0)])
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)