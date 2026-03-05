import cadquery as cq

# Parametric dimensions
plate_width = 40.0      # Width/Length of the square plate
plate_thickness = 5.0   # Thickness of the plate
corner_radius = 4.0     # Fillet radius for the corners

hole_diameter = 8.0     # Diameter of the through hole
cbore_diameter = 16.0   # Diameter of the counterbore
cbore_depth = 2.5       # Depth of the counterbore

# Create the base plate with rounded corners
# We start with a rectangle, extrude it, and then fillet the vertical edges
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the counterbored hole
# We select the top face, then create a hole with a counterbore
result = (
    result.faces(">Z")
    .workplane()
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)