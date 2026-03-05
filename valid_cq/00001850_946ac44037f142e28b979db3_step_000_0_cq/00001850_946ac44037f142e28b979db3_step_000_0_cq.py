import cadquery as cq

# Parametric dimensions
length = 50.0  # Total length of the object
diameter = 10.0  # Diameter of the cylinder
radius = diameter / 2.0

# Create the main cylinder
# We will create a cylinder that is slightly shorter than the total length 
# to accommodate the rounded ends, or we can fillet the ends.
# Based on the image, it looks like a capsule, which is a cylinder with hemispherical ends.
# One common way to make a capsule in CadQuery is to make a cylinder and fillet the edges 
# with the radius of the cylinder.

# Method 1: Cylinder + Fillet
# This is robust and simple. We create a cylinder of the full length.
# Then we select the edges at both ends (Z direction usually) and fillet them.
# If the fillet radius is equal to the cylinder radius, it forms a perfect hemisphere.

# Creating the base cylinder centered at the origin
# Note: To get a true capsule of total length 'L', the cylinder length needs to be L.
# If we fillet fully (radius = cylinder_radius), the length remains L, 
# but the cylindrical part becomes L - 2*R.
result = (
    cq.Workplane("XY")
    .cylinder(height=length, radius=radius)
    .edges()  # Select edges of the cylinder (top and bottom circles)
    .fillet(radius - 0.001) # Fillet with the radius (slightly less to avoid kernel issues with self-intersection)
)

# Alternatively, if the prompt implies a specific capsule shape where the ends might not be perfectly hemispherical
# or simply rounded, parametric control is good. The image shows very smooth, hemispherical-looking ends.
# A fillet of exactly the radius usually works, but sometimes kernels struggle with the singularity at the pole.
# Using a slightly smaller radius (e.g., radius - 0.001) is a common trick. 
# However, CadQuery/OCCT often handles the exact radius well for simple shapes. Let's try exact radius first,
# but stick to the "slightly less" convention for robustness in generated code if exact isn't strictly required.
# Actually, looking at the image, the right side end looks distinctively dark, possibly a flat face on a rounded end? 
# No, that's likely just the lighting/shading of a rendering. It looks like a standard capsule.

# Let's refine the approach to be perfectly safe and standard for a capsule.
result = (
    cq.Workplane("XY")
    .cylinder(length, radius)
    .edges()
    .fillet(radius - 0.01) # Use a near-exact fillet for a rounded capsule look
)