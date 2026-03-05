import cadquery as cq

# Parameters
rod_length = 100.0
rod_diameter = 12.0
rod_spacing = 60.0

# Create the model
# We sketch on the YZ plane to orient the rods horizontally along the X-axis
# The pushPoints method is used to create both circular profiles simultaneously
result = (
    cq.Workplane("YZ")
    .pushPoints([(-rod_spacing / 2, 0), (rod_spacing / 2, 0)])
    .circle(rod_diameter / 2)
    .extrude(rod_length)
)