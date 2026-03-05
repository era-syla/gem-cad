import cadquery as cq

# Parametric dimensions
length = 40.0  # Length of the rectangular block
width = 20.0   # Width of the rectangular block
height = 10.0  # Height of the rectangular block
sphere_radius = 6.0 # Radius of the spherical indentation

# Create the base block
# centered=True centers the box at the origin (0,0,0)
base = cq.Workplane("XY").box(length, width, height)

# Create a sphere to be used for the cut
# The sphere needs to be positioned correctly. 
# Since the box is centered at (0,0,0), its top face is at z = height/2.
# We want the center of the sphere to be at the center of the top face.
# If we position the sphere center exactly at z = height/2, we will get a perfect hemisphere cut.
sphere_cut = (
    cq.Workplane("XY")
    .workplane(offset=height/2) # Move workplane to the top face
    .sphere(sphere_radius)      # Create a sphere centered at the new workplane origin
)

# Perform the boolean cut operation
result = base.cut(sphere_cut)

# Export or visualize the result if running in an interactive environment
# show_object(result)