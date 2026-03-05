import cadquery as cq

# Extrusion length
extrusion_length = 75

# Create the profile in the XZ plane and mirror it to create a symmetric closed wire
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    # Bottom base
    .lineTo(14, 0)
    .lineTo(14, 1)
    .lineTo(16, 1)
    .lineTo(16, 3)
    # Concave side wall
    .threePointArc((12, 10), (16, 17))
    # Crown molding section (zig-zag pattern)
    .lineTo(24, 17)
    .lineTo(24, 19)
    .lineTo(21, 21)
    .lineTo(25, 24)
    .lineTo(21, 27)
    .lineTo(23, 29)
    # Slope to top surface
    .lineTo(18, 32)
    .lineTo(15, 32)
    # Raised top ridge
    .lineTo(14, 34)
    .lineTo(12, 34)
    .lineTo(11, 32)
    # Center flat area
    .lineTo(0, 32)
    # Mirror across Y-axis (which is X=0 in the XZ plane) to complete the shape
    .mirrorY()
)

# Extrude the profile to form the 3D solid
result = profile.extrude(extrusion_length)