import cadquery as cq

# -- Parametric Dimensions --
sphere_radius = 50.0  # Radius of the outer hemisphere
hole_diameter = 10.0  # Diameter of the central hole
hole_depth = 25.0     # Depth of the hole (or could be 'None' for through-all)

# -- Modeling --

# 1. Create a full sphere
# 2. Cut it in half to make a hemisphere using a box cut or by revolving an arc
# A simpler approach in CadQuery specifically for a hemisphere:
# Create a sphere and cut it with a large box, or create a revolved profile.
# Let's use the standard Sphere and cut method for clarity.

# Base Sphere
geo = cq.Workplane("XY").sphere(sphere_radius)

# Cut the top half off to make a hemisphere. 
# Since the default sphere is centered at (0,0,0), we want to keep the bottom half (Z < 0).
# We cut away the top half (Z > 0).
# Alternatively, we want the flat face facing UP, which is usually Z=0.
# So we want the geometry to exist in Z < 0.
cutting_box_size = sphere_radius * 3
geo = geo.cut(
    cq.Workplane("XY")
    .workplane(offset=0) # Start cut at Z=0
    .box(cutting_box_size, cutting_box_size, cutting_box_size, centered=(True, True, False))
)

# However, looking at the image, the flat face is facing the viewer. 
# Usually, we model with the flat face on the XY plane.
# The previous cut removed the top (Z>0). This leaves the bottom hemisphere (Z<0).
# The flat face is at Z=0.

# 3. Create the central hole
# Select the flat face (which is on the XY plane)
result = (
    geo.faces(">Z") # Select the top-most face (the flat one)
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutBlind(-hole_depth) # Cut downwards into the solid
)

# Note: If the hole needs to go all the way through, use .cutThruAll() instead.
# Based on the image shading, it looks like a blind hole, but `cutBlind` is safer parametrically.