import cadquery as cq

# Build a mechanical bracket/suspension arm assembly
# Main components: central hub, two arms extending down, horizontal shaft, and a caliper/bracket on the right

# Central hub/body
hub = (
    cq.Workplane("XY")
    .box(40, 30, 20)
)

# Create the main body as a trapezoid-like shape
body = (
    cq.Workplane("XY")
    .rect(40, 20)
    .extrude(15)
)

# Left arm - angled down-left
left_arm = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 0))
    .box(8, 80, 8)
)

# Build the assembly from scratch with primitive shapes

# Central mounting plate
result = cq.Workplane("XY").box(35, 25, 12)

# Add left lower arm 1
arm1 = (
    cq.Workplane("XY")
    .center(-15, -20)
    .box(8, 60, 7)
)

# Add left lower arm 2
arm2 = (
    cq.Workplane("XY")
    .center(5, -20)
    .box(8, 60, 7)
)

# Combine with union
result = result.union(arm1).union(arm2)

# Add foot pads at bottom of arms
foot1 = (
    cq.Workplane("XY")
    .center(-15, -52)
    .box(18, 12, 7)
)

foot2 = (
    cq.Workplane("XY")
    .center(5, -52)
    .box(18, 12, 7)
)

result = result.union(foot1).union(foot2)

# Add horizontal shaft going right
shaft = (
    cq.Workplane("YZ")
    .center(0, 6)
    .circle(4)
    .extrude(80)
)

result = result.union(shaft)

# Add caliper/brake body on the right side
caliper_body = (
    cq.Workplane("XY")
    .center(55, 5)
    .box(25, 30, 35)
)

result = result.union(caliper_body)

# Add mounting ears to caliper
ear1 = (
    cq.Workplane("XY")
    .center(55, 22)
    .box(30, 10, 8)
)

ear2 = (
    cq.Workplane("XY")
    .center(55, -12)
    .box(30, 10, 8)
)

result = result.union(ear1).union(ear2)

# Add connecting bracket between shaft and caliper
bracket = (
    cq.Workplane("XY")
    .center(35, 5)
    .box(15, 20, 20)
)

result = result.union(bracket)

# Add top cross member
cross = (
    cq.Workplane("XY")
    .center(-5, 5)
    .box(30, 8, 8)
)

result = result.union(cross)

# Add bolts/cylinders on caliper
bolt1 = (
    cq.Workplane("XZ")
    .center(55, 15)
    .circle(3)
    .extrude(35)
)

bolt2 = (
    cq.Workplane("XZ")
    .center(55, 15)
    .circle(3)
    .extrude(-5)
)

# Add small mounting holes representation as cylinders on feet
# Foot holes
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(0.8)
)