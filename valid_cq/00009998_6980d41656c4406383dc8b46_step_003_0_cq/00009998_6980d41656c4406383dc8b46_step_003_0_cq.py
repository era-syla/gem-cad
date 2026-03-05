import cadquery as cq

# Parametric dimensions
base_length = 80.0
base_width = 25.0
base_thickness = 5.0

cylinder_radius = 6.0
cylinder_height = 50.0

# Calculate the position for the cylinder
# Let's position it near one end. 
# Center X: moving it to one side from the center (0,0) of the base.
# If the base is centered at (0,0), its extent is -length/2 to +length/2.
# We want the cylinder near -length/2 + padding.
cylinder_x_pos = -(base_length / 2) + (base_width / 2) 

# Create the base rectangle
# Centered on XY plane for easier symmetry management
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# Create the vertical cylinder
# We select the top face of the base and draw the circle
result = (
    base.faces(">Z")
    .workplane()
    .center(cylinder_x_pos, 0)
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)

# If running in an environment that supports it (like CQ-editor), show the object
# show_object(result)