import cadquery as cq

# Parametric dimensions for the Rectangular Hollow Section (RHS) tube
length = 150.0       # Total length of the tube
width = 40.0         # Width of the cross-section
height = 60.0        # Height of the cross-section
thickness = 4.0      # Wall thickness
fillet_radius = 6.0  # Radius of the exterior corners

# Create the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the base solid block
    .box(width, height, length)
    # 2. Select the edges running along the length (Z-axis)
    .edges("|Z")
    # 3. Apply fillets to rounded the outer corners
    .fillet(fillet_radius)
    # 4. Select the top and bottom faces (ends of the tube)
    .faces(">Z or <Z")
    # 5. Shell the solid inward to create the hollow tube, removing the selected faces
    .shell(-thickness)
)