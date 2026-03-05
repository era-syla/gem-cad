import cadquery as cq

# Define the 2D outline of the spade‐like shape
pts = [
    (-20, 0),
    (-15, 10),
    (-8, 18),
    (5, 20),
    (18, 10),
    (12, -5),
    (5, -18),
    (-5, -15),
    (-12, -5),
    (-20, 0),
]

# Extrude the outer solid
outer = cq.Workplane("XY").spline(pts).close().extrude(6)

# Add the rectangular tab on the left
# The tab is 8 × 6 mm, centered on y=0, flush with the tip at x = -20
tab = (
    cq.Workplane("XY")
    .center(-20 - 4, 0)  # move left half the tab width from the tip
    .rect(8, 6)
    .extrude(6)
)

base = outer.union(tab)

# Create the inner cutout by offsetting the same outline inward and extruding less height
inner = (
    cq.Workplane("XY")
    .spline(pts)
    .close()
    .offset2D(-3)  # 3 mm wall thickness
    .extrude(4)    # recess depth
)

result = base.cut(inner)