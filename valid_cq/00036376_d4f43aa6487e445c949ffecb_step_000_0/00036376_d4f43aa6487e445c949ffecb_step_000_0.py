import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
width = 100.0           # Horizontal length of the bracket
height = 100.0          # Vertical length of the bracket
thickness = 12.0        # Thickness of the plate
tip_flat = 20.0         # Length of the flattened segments at the triangle tips
wall_width = 16.0       # Width of the material border around the cutout
fillet_radius = 10.0    # Radius of the cutout's rounded corners
hole_dia = 6.0          # Diameter of the mounting holes
hole_depth = 25.0       # Depth of the mounting holes
hole_spacing = 30.0     # Spacing between the holes

# -----------------------------------------------------------------------------
# Geometry Generation
# -----------------------------------------------------------------------------

# 1. Define Outer Profile
# The shape is a right triangle with flattened tips (chamfered).
# Coordinates defined counter-clockwise starting from origin (0,0).
pts = [
    (0, 0),                     # Bottom-Left corner (90 deg)
    (width, 0),                 # Bottom edge end
    (width, tip_flat),          # Right vertical tip edge
    (tip_flat, height),         # Top horizontal tip edge
    (0, height)                 # Top-Left corner
]

# 2. Create Base Solid
# Draw profile on XY plane and extrude to thickness
base = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# 3. Create Cutout
# We generate a "tool" solid to subtract from the base.
# The tool profile is an inward offset of the base profile.
cutout_tool = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .offset2D(-wall_width, kind="intersection")  # Inward offset with sharp corners
    .extrude(thickness)
    .edges("|Z")            # Select vertical edges of the prism
    .fillet(fillet_radius)  # Apply fillets to round the corners
)

# Subtract the cutout tool from the base
body = base.cut(cutout_tool)

# 4. Create Mounting Holes
# The holes are located on the vertical face at X=0 (the "spine" of the bracket).
# We select the face with normal <X, create a workplane, and drill holes.
# Note: On this face, the local coordinates align such that points are distributed along the Y-axis (length).
result = (
    body
    .faces("<X")
    .workplane()
    .pushPoints([
        (0, 0),                 # Center hole
        (hole_spacing, 0),      # Top hole (relative to workplane center)
        (-hole_spacing, 0)      # Bottom hole (relative to workplane center)
    ])
    .hole(hole_dia, depth=hole_depth)
)