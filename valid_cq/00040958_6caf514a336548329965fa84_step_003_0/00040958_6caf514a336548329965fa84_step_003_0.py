import cadquery as cq

# -----------------------------------------------------------------------------
# Parameter Definitions
# -----------------------------------------------------------------------------
# Dimensions estimated from the image (assuming units in mm)
length = 26.0          # Total length of the part (Y-axis direction)
width = 20.0           # Total width of the part (X-axis direction)
height_center = 8.0    # Maximum height at the center of the curved top
height_edge = 6.0      # Height at the straight side edges
corner_radius = 2.0    # Fillet radius for the vertical corners
hole_diameter = 10.0   # Diameter of the central threaded hole
chamfer_size = 0.5     # Size of the chamfer on the hole entrance

# -----------------------------------------------------------------------------
# Geometry Construction
# -----------------------------------------------------------------------------

# 1. Create the base profile in the XZ plane.
# The profile consists of a flat bottom, vertical sides, and a convex top arc.
# We use a 3-point arc to ensure the curve passes through the calculated heights.
profile = (
    cq.Workplane("XZ")
    .moveTo(width / 2.0, 0)
    .lineTo(width / 2.0, height_edge)
    .threePointArc((0, height_center), (-width / 2.0, height_edge))
    .lineTo(-width / 2.0, 0)
    .close()
)

# 2. Extrude the profile symmetrically along the Y-axis to create the solid block.
# This establishes the length of the part.
base_solid = profile.extrude(length / 2.0, both=True)

# 3. Fillet the four vertical corners.
# We select edges parallel to the Z-axis ("|Z") to round the rectangular footprint.
filleted_solid = base_solid.edges("|Z").fillet(corner_radius)

# 4. Create the central hole.
# We create a simple cylindrical hole through the center. 
# While the image shows threads, standard CAD modeling practice usually represents 
# these as smooth holes unless helical geometry is strictly required.
with_hole = filleted_solid.faces(">Z").workplane().hole(hole_diameter)

# 5. Chamfer the top edge of the hole.
# The top edge is a complex 3D curve (intersection of cylinder and arc).
# We select it by finding the edge on the top face nearest to the center axis.
result = (
    with_hole
    .faces(">Z")
    .edges(cq.selectors.NearestToPointSelector((0, 0, height_center)))
    .chamfer(chamfer_size)
)

# The 'result' variable now contains the final solid geometry.