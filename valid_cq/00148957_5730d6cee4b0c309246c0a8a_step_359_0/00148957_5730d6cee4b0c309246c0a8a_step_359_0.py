import cadquery as cq

# Parameters based on visual estimation of the flange
outer_diameter = 100.0
inner_diameter = 50.0
thickness = 10.0
bolt_circle_diameter = 75.0
bolt_hole_diameter = 12.0
num_holes = 4

# Create the CAD model
result = (
    cq.Workplane("XY")
    # Draw the outer diameter and inner diameter concentric circles
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    # Extrude to create the main ring body
    .extrude(thickness)
    # Select the top face to place the smaller mounting holes
    .faces(">Z").workplane()
    # Create a polar array (circular pattern) for the 4 holes
    .polarArray(radius=bolt_circle_diameter / 2.0, 
                startAngle=0, 
                angle=360, 
                count=num_holes)
    # Cut the holes through the entire part
    .hole(bolt_hole_diameter)
)