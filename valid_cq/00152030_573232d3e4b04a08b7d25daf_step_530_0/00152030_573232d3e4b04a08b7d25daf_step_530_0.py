import cadquery as cq

# Model parameters
outer_diameter = 100.0
inner_diameter = 50.0
thickness = 10.0
bolt_circle_diameter = 75.0
hole_diameter = 12.0
num_holes = 4

# Create the flange geometry
result = (
    cq.Workplane("XY")
    # Create the main disc body with the central hole
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
    # Select the top face to add the bolt holes
    .faces(">Z")
    .workplane()
    # Create the pattern of holes
    .polarArray(bolt_circle_diameter / 2.0, 0, 360, num_holes)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)