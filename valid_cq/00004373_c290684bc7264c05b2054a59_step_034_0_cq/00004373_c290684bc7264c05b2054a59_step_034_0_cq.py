import cadquery as cq

# Parametric dimensions
plate_width = 100.0  # Width of the rectangular plate
plate_height = 100.0 # Height of the rectangular plate
plate_thickness = 15.0 # Thickness of the plate
center_hole_diameter = 40.0 # Diameter of the large central hole

# Bolt hole parameters
bolt_hole_diameter = 6.0 # Diameter of the smaller mounting holes
# The pattern suggests two sets of holes, likely symmetric.
# Outer holes
outer_hole_dx = 80.0 # Horizontal distance between outer hole centers
outer_hole_dy = 80.0 # Vertical distance between outer hole centers
# Inner/Middle holes (the two in the middle vertically)
middle_hole_dx = 80.0 # Horizontal distance between middle hole centers
middle_hole_dy = 20.0 # Vertical distance from center (guess based on visual) - actually let's define it as a y-offset from center

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    
    # Create the large center hole
    .faces(">Z")
    .workplane()
    .hole(center_hole_diameter)
    
    # Create the 4 corner holes
    .faces(">Z")
    .workplane()
    .rect(outer_hole_dx, outer_hole_dy, forConstruction=True)
    .vertices()
    .hole(bolt_hole_diameter)
    
    # Create the 2 middle side holes
    # Based on the image, there are two additional holes between the top and bottom ones on the vertical edges.
    # They seem aligned horizontally with the corner holes.
    .faces(">Z")
    .workplane()
    .pushPoints([(outer_hole_dx/2, 0), (-outer_hole_dx/2, 0)])
    .hole(bolt_hole_diameter)
)