import cadquery as cq

# Parametric dimensions estimated from the image
base_width = 40.0    # Total width of the base (points on left and right)
base_depth = 20.0    # Depth of the base
height = 25.0        # Vertical height of the transition
top_radius = 8.0     # Radius of the top circular profile

# Create the solid geometry
# 1. Define the base rectangle on the XY plane
# 2. Define the target circle on a plane offset by the height
# 3. Loft between the two profiles to create the transition
#    ruled=True is used to create linear edges (creases) connecting the
#    corners of the rectangle to the circle, matching the visual style.
result = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .workplane(offset=height)
    .circle(top_radius)
    .loft(ruled=True, combine=True)
)