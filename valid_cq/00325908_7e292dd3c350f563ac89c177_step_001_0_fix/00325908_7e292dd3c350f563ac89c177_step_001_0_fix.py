import cadquery as cq

# Parameters
r = 20        # radius of cylinder
t = 10        # thickness of cylinder and arms
L1 = 40       # length of horizontal arm
L2 = 30       # length of angled arm
bw = 6        # width (cross-section) of arms
theta = -30   # angle for the second arm in degrees

# Base cylinder centered on the XY plane
cyl = cq.Workplane("XY").cylinder(height=t, radius=r).translate((0, 0, -t/2))

# First arm: horizontal, along +X
arm1 = cq.Workplane("XY") \
    .box(L1, bw, t) \
    .translate((r + L1/2, 0, 0))

# Second arm: at angle theta around Z, offset radial
arm2 = cq.Workplane("XY") \
    .transformed(offset=(r + L2/2, 0, 0), rotate=(0, 0, theta)) \
    .box(L2, bw, t)

# Combine all parts
result = cyl.union(arm1).union(arm2)