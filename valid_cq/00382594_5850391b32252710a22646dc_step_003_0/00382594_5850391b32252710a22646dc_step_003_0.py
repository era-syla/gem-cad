import cadquery as cq

# Define parameters for the washer
outer_diameter = 30.0
inner_diameter = 20.0
thickness = 5.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)  # Outer circle
    .circle(inner_diameter / 2.0)  # Inner circle to form the hole
    .extrude(thickness)            # Extrude the area between circles
)