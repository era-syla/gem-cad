import cadquery as cq

# Parameters
width = 30
depth = 6
height = 60
slope_angle = 25  # degrees for the front slope
boss1_d = 6       # diameter of left boss
boss2_d = 10      # diameter of right boss
boss_h = 8        # boss height
hole_d = 4        # hole diameter through the right boss

# 1) Base block
result = cq.Workplane("XY").box(width, depth, height)

# 2) Cut the front sloping surface (single plane, symmetric across X)
# Create a large box, rotate it about the X axis, position it so it intersects the front top,
# then subtract it to leave a sloping surface facing forward.
wedge = (
    cq.Workplane("XY")
      .box(width * 2, depth * 2, height * 2)           # big cutter block
      .rotate((0, 0, 0), (1, 0, 0), slope_angle)       # rotate about X to create slope
      .translate((0, (depth/2) + depth, height/2))     # move it forward and upward
)
result = result.cut(wedge)

# 3) Add two cylindrical bosses on the back/top
# Positions: along X at ±width/4, at the back edge y = -depth/2
x1 = -width / 4
x2 =  width / 4
y_boss = -depth / 2

# Left boss (solid)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(x1, y_boss)
    .circle(boss1_d / 2)
    .extrude(boss_h)
)

# Right boss (will get a hole)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(x2, y_boss)
    .circle(boss2_d / 2)
    .extrude(boss_h)
)

# 4) Drill a through-hole in the right boss
# Use hole() which will pierce through the boss and the main block
result = (
    result
    .faces(">Z")
    .workplane()
    .center(x2, y_boss)
    .hole(hole_d)
)