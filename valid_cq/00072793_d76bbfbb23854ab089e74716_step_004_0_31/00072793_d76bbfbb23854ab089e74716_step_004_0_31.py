import cadquery as cq

# Parametric dimensions for the model
L = 120.0          # Total length (X-axis)
W = 60.0           # Total width (Y-axis)
T = 3.0            # Wall and base thickness
H_front = 12.0     # Height of the front long wall
H_side = 25.0      # Height of the left and right side walls
tab_length = 15.0  # Length of the downward tab along Y-axis
tab_drop = 8.0     # How far the tab extends below the base

# 1. Main base plate
base = cq.Workplane("XY").box(L, W, T, centered=(False, False, False))

# 2. Front short wall (extends full length L)
front_wall = cq.Workplane("XY").box(L, T, H_front, centered=(False, False, False))

# 3. Left tall wall (extends from back of front wall to open back edge)
left_wall = (
    cq.Workplane("XY")
    .transformed(offset=(0, T, 0))
    .box(T, W - T, H_side, centered=(False, False, False))
)

# 4. Right tall wall (extends from back of front wall to open back edge)
right_wall = (
    cq.Workplane("XY")
    .transformed(offset=(L - T, T, 0))
    .box(T, W - T, H_side, centered=(False, False, False))
)

# 5. Downward mounting tab on the front-left corner
tab = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -tab_drop))
    .box(T, tab_length, tab_drop, centered=(False, False, False))
)

# Combine all components into a single solid
result = base.union(front_wall).union(left_wall).union(right_wall).union(tab)