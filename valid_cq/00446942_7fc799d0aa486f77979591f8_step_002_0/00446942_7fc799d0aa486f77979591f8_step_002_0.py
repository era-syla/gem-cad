import cadquery as cq

# Geometric parameters
length = 60.0        # Total length of the capsule-like object
diameter = 25.0      # Outer diameter of the cylinder
fillet_radius = 6.0  # Radius of the rounded edges (must be less than diameter/2)

# Create the 3D model
# 1. Start with a cylinder centered at the origin aligned with the Z-axis
# 2. Select the top and bottom circular faces
# 3. Select the edges of those faces
# 4. Apply a fillet to round the ends
result = (
    cq.Workplane("XY")
    .cylinder(length, diameter / 2.0)
    .faces(">Z or <Z")
    .edges()
    .fillet(fillet_radius)
)