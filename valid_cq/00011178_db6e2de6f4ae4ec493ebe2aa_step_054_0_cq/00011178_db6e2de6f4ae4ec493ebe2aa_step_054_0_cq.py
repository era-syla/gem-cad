import cadquery as cq

# Parametric dimensions
cylinder_diameter = 50.0
cylinder_length = 60.0
chamfer_length = 15.0  # The length along the cylinder axis to be chamfered
chamfer_radius_reduction = 10.0 # How much radius is removed at the tip

# Derived dimensions
tip_diameter = cylinder_diameter - (2 * chamfer_radius_reduction)
straight_length = cylinder_length - chamfer_length

# Create the main cylindrical body
# Method 1: Create a cylinder and then chamfer one edge
# This is often the most robust way if the geometry is simple
result = cq.Workplane("XY").circle(cylinder_diameter / 2).extrude(cylinder_length)

# Select the edge on the top face (Z-positive) to chamfer
# We select the face at Z=cylinder_length, then its outer wire/edge
result = result.faces(">Z").edges().chamfer(chamfer_length, chamfer_radius_reduction)

# Alternative Method (Revolve):
# Create a profile and revolve it. This gives explicit control over the angle.
# points = [
#     (0, 0),
#     (cylinder_diameter/2, 0),
#     (cylinder_diameter/2, straight_length),
#     (tip_diameter/2, cylinder_length),
#     (0, cylinder_length)
# ]
# result = cq.Workplane("XZ").polyline(points).close().revolve()

# Return the result
if 'show_object' in globals():
    show_object(result)