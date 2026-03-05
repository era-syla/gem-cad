import cadquery as cq

# Parameters
base_length = 100.0
base_width = 30.0
base_thickness = 5.0

cylinder_radius = 8.0
cylinder_height = 50.0

# Create the base plate
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Add the cylinder
# Position it near one end of the base plate
x_offset = -base_length / 2 + cylinder_radius + 5.0 # 5mm from the edge

result = (
    base
    .faces(">Z").workplane()
    .center(x_offset, 0)
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)