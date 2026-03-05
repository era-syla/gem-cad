import cadquery as cq

# Parametric dimensions for the flange/ring
outer_diameter = 100.0
inner_diameter = 70.0
thickness = 4.0
hole_diameter = 6.0
num_holes = 6

# Calculate the pitch circle diameter (PCD) centered on the ring face
bolt_circle_diameter = (outer_diameter + inner_diameter) / 2.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the base ring by drawing two concentric circles and extruding
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
    
    # Select the top face to create the hole pattern
    .faces(">Z")
    .workplane()
    
    # Define the locations for the holes using a polar array
    .polarArray(
        radius=bolt_circle_diameter / 2.0, 
        startAngle=0, 
        angle=360, 
        count=num_holes
    )
    
    # Cut the bolt holes through the part
    .hole(hole_diameter)
)