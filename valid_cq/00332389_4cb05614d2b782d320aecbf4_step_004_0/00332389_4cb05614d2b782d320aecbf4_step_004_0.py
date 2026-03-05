import cadquery as cq

# Parametric dimensions for the rods
rod_length = 150.0       # Length of the rods
rod_diameter = 8.0       # Diameter of the rods
rod_spacing = 40.0       # Distance between the centers of the rods

# Create the 3D model
# We create a workplane on the YZ plane (side view) to sketch the cross-sections
# We use pushPoints to define the centers of both rods simultaneously
# Then we draw circles and extrude them along the X-axis
result = (
    cq.Workplane("YZ")
    .pushPoints([(-rod_spacing / 2.0, 0), (rod_spacing / 2.0, 0)])
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)