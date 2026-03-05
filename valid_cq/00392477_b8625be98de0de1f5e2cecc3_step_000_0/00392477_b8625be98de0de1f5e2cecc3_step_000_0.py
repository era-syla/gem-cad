import cadquery as cq

# -- Parametric Dimensions --
# Estimated based on the visual proportions of the image
link_width = 30.0               # Width of the rounded ends
center_distance = 80.0          # Distance between the two hole centers
plate_thickness = 5.0           # Thickness of the link
hole_diameter = 12.0            # Diameter of the through-holes

# -- Modeling --

# 1. Create the main body
# We use slot2D which creates a profile consisting of two semicircles 
# connected by straight lines. 'length' is the center-to-center distance.
result = (
    cq.Workplane("XY")
    .slot2D(center_distance, link_width)
    .extrude(plate_thickness)
)

# 2. Create the holes
# Select the top face, define the center points for the holes, 
# and cut through the entire solid.
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-center_distance / 2.0, 0), 
        (center_distance / 2.0, 0)
    ])
    .hole(hole_diameter)
)

# Optional: Add a small chamfer to all non-vertical edges for a realistic look
# matching the rendered image style
result = result.edges("not |Z").chamfer(0.5)