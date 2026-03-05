import cadquery as cq

# Define the polygon points for the outer boundary of the part
# These points are carefully chosen to allow a smooth fillet and form the V-shape
pts = [
    (-25, -42),  # Bottom of the left arm
    (-42, -25),  # Left edge of the left arm
    (-15, 18),   # Top left curve
    (20, 18),    # Top flat edge right side
    (52, -2),    # Outer right edge
    (38, -18),   # Bottom right edge
    (10, -5),    # Inner V-notch right
    (-10, -15)   # Inner V-notch left
]

# 1. Create the main solid block and fillet the vertical edges
body = (
    cq.Workplane("XY")
    .polyline(pts).close()
    .extrude(18)
    .edges("|Z")
    .fillet(8)
)

# 2. Shell the body to create the outer walls and base plate
# Shelling inwards with a negative thickness
shelled_body = body.faces(">Z").shell(-2.5)

# 3. Create the three main structural bosses
main_bosses = (
    cq.Workplane("XY")
    .pushPoints([(0, 0), (-30, -30), (40, -5)])
    .circle(8)
    .extrude(18)
)

# 4. Create the two smaller mounting bosses inside the pocket
small_bosses = (
    cq.Workplane("XY")
    .pushPoints([(-14, -14), (15, -6)])
    .circle(3)
    .extrude(10)
)

# 5. Union all the solid components together
part = shelled_body.union(main_bosses).union(small_bosses)

# 6. Create a tool to cut all the through-holes
# We start slightly below Z=0 to ensure a clean cut through the base
cut_tool = (
    cq.Workplane("XY").workplane(offset=-5)
    .pushPoints([(0, 0), (-30, -30), (40, -5)])
    .circle(5)
    .pushPoints([(-14, -14), (15, -6)])
    .circle(1.5)
    .extrude(30)
)

# 7. Perform the cut
result = part.cut(cut_tool)