import cadquery as cq

# Define parametric dimensions
cylinder_radius = 20.0  # Radius of the cylinder base
cylinder_height = 80.0  # Total height of the cylinder

# Create the cylindrical geometry
# We create a simple cylinder aligned along the Z-axis
result = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# Note: The horizontal lines visible in the reference image are likely artifacts 
# of rendering (mesh lines) or represent a stack of separate discs. 
# A single solid cylinder is the most accurate geometric representation 
# of the overall form shown. If a stack was intended, we could loop and stack, 
# but generally, this is a cylinder.

# To export or visualize 'result' is the variable holding the CadQuery solid object