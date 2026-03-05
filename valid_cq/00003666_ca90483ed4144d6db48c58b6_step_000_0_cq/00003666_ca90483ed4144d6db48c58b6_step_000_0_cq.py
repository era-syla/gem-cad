import cadquery as cq

# Define parametric dimensions
box_width = 50.0   # Width of the rectangular prism
box_height = 80.0  # Height of the rectangular prism
box_thickness = 30.0 # Thickness of the rectangular prism

sphere_radius = 15.0 # Radius of the spherical cutout
cutout_x_offset = 10.0 # Offset from the center in X
cutout_y_offset = -20.0 # Offset from the center in Y (towards bottom)
cutout_depth_ratio = 0.6 # How deep the sphere cuts into the face relative to its radius

# Create the base rectangular prism
# Centered at (0,0,0) makes positioning features easier relative to the center
base = cq.Workplane("XY").box(box_width, box_height, box_thickness)

# Create the sphere for the cutout
# We position the sphere relative to the front face of the box.
# The front face is at z = box_thickness / 2.
sphere_z_center = (box_thickness / 2) 

# Create a sphere solid
# We create a sphere and translate it to the desired cut location
sphere_cutter = cq.Workplane("XY").sphere(sphere_radius).translate((cutout_x_offset, cutout_y_offset, sphere_z_center))

# Cut the sphere from the base box
result = base.cut(sphere_cutter)

# Export or visualization
if 'show_object' in globals():
    show_object(result)