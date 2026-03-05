import cadquery as cq

# Define parametric dimensions
outer_diameter = 50.0
inner_diameter = 25.0
thickness = 5.0
notch_radius = 1.5

# Create the 3D model
result = (
    cq.Workplane("XY")
    # Step 1: Create the base washer shape (outer circle and inner hole)
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
    # Step 2: Create the notch/keyway
    # Select the top face to start a new sketch
    .faces(">Z")
    .workplane()
    # Move to the perimeter of the inner circle
    .moveTo(inner_diameter / 2.0, 0)
    # Create the cutting profile for the notch
    .circle(notch_radius)
    # Cut through the entire thickness of the part
    .cutThruAll()
)