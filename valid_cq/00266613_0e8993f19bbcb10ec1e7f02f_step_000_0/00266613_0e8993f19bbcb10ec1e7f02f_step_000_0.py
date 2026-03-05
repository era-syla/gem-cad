import cadquery as cq

# Parameters for the sleeve enclosure
height = 90.0        # Total height in Z
width = 60.0         # Total width in X
depth = 12.0         # Total depth/thickness in Y
fillet_radius = 4.0  # Radius for the vertical edges
wall_thickness = 1.5 # Wall thickness for the shell

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the basic rectangular prism
    .box(width, depth, height)
    # 2. Fillet the four vertical edges to create the rounded sides
    .edges("|Z")
    .fillet(fillet_radius)
    # 3. Select the top face and shell the solid inwards to create the hollow shape
    .faces(">Z")
    .shell(-wall_thickness)
)