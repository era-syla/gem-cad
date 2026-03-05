import cadquery as cq

# Parametric dimensions
length = 80.0       # Total length of the rod
radius = 0.5        # Radius of the rod (thin to represent a line)
angle = -30.0       # Rotation angle to match the diagonal orientation (top-left to bottom-right)

# Create the 3D model
# We start with a cylinder primitive which defaults to alignment along the Z-axis.
# We then rotate it to lie on the XY plane and adjust its angle.
result = (
    cq.Workplane("XY")
    .cylinder(length, radius)           # Create cylinder centered at origin, aligned with Z
    .rotate((0, 0, 0), (0, 1, 0), 90)   # Rotate 90 deg around Y to align with X-axis
    .rotate((0, 0, 0), (0, 0, 1), angle)# Rotate around Z to match the visual diagonal
)