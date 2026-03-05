import cadquery as cq

# Dimensions
L = 100.0
W = 45.0
H = 15.0

# Create the base block
base = cq.Workplane("XY").box(L, W, H)

# Create the rectangular notch on the back edge
notch = cq.Workplane("XY").center(5, W/2).box(18, 15, H)
base = base.cut(notch)

# Define pin locations
pin_pts = [(-35, -14), (35, 14)]

# Create the alignment pins (cylindrical body)
pins = (
    cq.Workplane("XY", origin=(0, 0, H/2))
    .pushPoints(pin_pts)
    .cylinder(8, 2.5, centered=(True, True, False))
)

# Create the spherical tops for the pins
pin_tops = (
    cq.Workplane("XY", origin=(0, 0, H/2 + 8))
    .pushPoints(pin_pts)
    .sphere(2.5)
)

# Build the cavity tool to subtract from the base
# 1. Spherical end cavity
sphere_cavity = cq.Workplane("YZ", origin=(28, 0, H/2)).sphere(6)

# 2. Narrow gate channel
cyl_gate = cq.Workplane("YZ", origin=(20, 0, H/2)).circle(2.5).extrude(8)

# 3. Flared conical runner
cone_runner = (
    cq.Workplane("YZ", origin=(-35, 0, H/2))
    .circle(1.5)
    .workplane(offset=55)
    .circle(7.0)
    .loft()
)

# 4. Inner deeper groove running along the conical runner
inner_groove = cq.Workplane("YZ", origin=(-35, 0, H/2 - 1.0)).circle(1.2).extrude(55)

# Combine the tool parts
cavity_tool = sphere_cavity.union(cyl_gate).union(cone_runner).union(inner_groove)

# Cut the cavity from the base and add the pins
result = base.cut(cavity_tool).union(pins).union(pin_tops)
