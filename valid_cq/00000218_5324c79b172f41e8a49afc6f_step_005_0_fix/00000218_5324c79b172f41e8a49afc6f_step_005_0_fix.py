import cadquery as cq

# Main servo body
body = (
    cq.Workplane("XY")
    .box(40, 20, 30)
)

# Top cap / lid area (slightly raised on top)
top_cap = (
    cq.Workplane("XY")
    .box(32, 18, 3)
    .translate((0, 0, 16.5))
)

# Mounting tabs (ears) on left and right sides
left_tab = (
    cq.Workplane("XY")
    .box(8, 28, 3)
    .translate((-24, 0, -13.5))
)

right_tab = (
    cq.Workplane("XY")
    .box(8, 28, 3)
    .translate((24, 0, -13.5))
)

# Combine body with tabs
servo = body.union(left_tab).union(right_tab)

# Add mounting flange at bottom with holes concept
# Bottom mounting plate
bottom_plate = (
    cq.Workplane("XY")
    .box(56, 28, 3)
    .translate((0, 0, -16.5))
)

servo = servo.union(bottom_plate)

# Output shaft cylinder (gear/pulley on top)
shaft_base = (
    cq.Workplane("XY")
    .cylinder(8, 9)
    .translate((-8, 0, 19))
)

# Gear teeth approximation - slightly larger cylinder
gear = (
    cq.Workplane("XY")
    .cylinder(6, 10)
    .translate((-8, 0, 19))
)

servo = servo.union(shaft_base)

# Small hub on top of gear
hub = (
    cq.Workplane("XY")
    .cylinder(4, 4)
    .translate((-8, 0, 25))
)

servo = servo.union(hub)

# Connector housing bump on side
connector = (
    cq.Workplane("XZ")
    .workplane(offset=10)
    .rect(10, 8)
    .extrude(3)
    .translate((-5, 10, -8))
)

servo = servo.union(connector)

# Cut mounting holes in bottom plate
servo = (
    servo
    .faces(">Z[-3]")
    .workplane()
    .pushPoints([(-20, -8), (-20, 8), (20, -8), (20, 8)])
    .hole(3)
)

# Cut wire hole in connector area
# Add small rectangular bump on back for wire exit
wire_bump = (
    cq.Workplane("YZ")
    .workplane(offset=20)
    .rect(8, 6)
    .extrude(3)
    .translate((20, 0, -5))
)

# Fillet the main body edges
try:
    servo = servo.edges("|Z").fillet(1.5)
except:
    pass

result = servo