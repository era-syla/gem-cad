import cadquery as cq

# Parametric dimensions based on the visual estimation of the image
length = 100.0        # Distance between the two hole centers
end_radius = 10.0     # Radius of the rounded ends (width approx 20mm)
bar_width = 12.0      # Width of the central connecting bar (narrower than ends)
thickness = 5.0       # Uniform thickness of the plate
hole_radius = 4.0     # Radius of the holes at the ends
fillet_radius = 8.0   # Radius to smooth the transition between bar and ends

# 1. Create the two rounded ends
# We place two circles at the specified center-to-center distance
ends = (
    cq.Workplane("XY")
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    .circle(end_radius)
    .extrude(thickness)
)

# 2. Create the connecting bar
# A rectangular section connecting the two ends
bar = (
    cq.Workplane("XY")
    .rect(length, bar_width)
    .extrude(thickness)
)

# 3. Combine the geometry
# Union the ends and the bar into a single solid
base_geo = ends.union(bar)

# 4. Apply fillets
# Select the vertical edges (parallel to Z) created by the intersection 
# of the bar and circles to create the smooth 'neck' transition.
# The outer boundaries of the circles are faces, so edges("|Z") reliably 
# grabs the four concave corners.
filleted_geo = base_geo.edges("|Z").fillet(fillet_radius)

# 5. Cut the holes
# Select the top face, define new workplane, and cut holes at the centers
result = (
    filleted_geo.faces(">Z").workplane()
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    .circle(hole_radius)
    .cutThruAll()
)