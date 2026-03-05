import cadquery as cq

# Parameters
g = 2           # gap between halves
Lh = 60         # half-length (from inner cut to circle center minus radius)
R = 5           # outer circle radius
Wi = 8          # inner width of each half
Wo = 2 * R      # outer width (diameter of circle)
thickness = 3   # extrusion thickness

# Compute key X coordinates
x0 = g/2                # inner cut plane
x1 = x0 + Lh            # circle center X
x_arc_start = x1 - R    # start of circle arc tangency

# Build one half (right)
wp = cq.Workplane("XY")
profile = (
    wp.moveTo(x0, Wi/2)
      .lineTo(x_arc_start, Wo/2)
      .threePointArc((x1, 0), (x_arc_start, -Wo/2))
      .lineTo(x0, -Wi/2)
      .close()
)
right_half = profile.extrude(thickness)

# Mirror to create left half and unite
left_half = right_half.mirror(mirrorPlane="YZ")
result = right_half.union(left_half)