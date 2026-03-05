import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0
width = 25.0
thickness = 10.0
hole_spacing = 60.0    # Distance between hole centers
hole_diameter = 6.0    # Inner hole diameter
cbore_diameter = 10.0  # Counterbore diameter
cbore_depth = 2.0      # Counterbore depth

# Create the rectangular bar centered at origin
# Select the top face and create counterbored holes
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)])
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)