import cadquery as cq

# Build a futuristic armored pod/housing shape
# Main body - elongated hexagonal prism with tapered ends

length = 80
width = 35
height = 25

# Create main body using loft between profiles
result = (
    cq.Workplane("XY")
    .box(length, width, height)
)

# Taper the front and back ends
# Use a shell-like approach with chamfered edges

# Start fresh with a more accurate shape
# The object looks like a coffin/pod shape - longer in one axis,
# with angled top and chamfered corners

def make_pod():
    # Create the main elongated body with chamfered profile
    pts_top = [
        (-35, 0),
        (-28, 14),
        (28, 14),
        (35, 0),
        (28, -14),
        (-28, -14),
    ]
    
    # Base profile (wider)
    base = (
        cq.Workplane("XY")
        .polyline(pts_top)
        .close()
        .extrude(20)
    )
    
    return base

# Create main body as an extruded hexagon
body = (
    cq.Workplane("XY")
    .polygon(6, 75)
    .extrude(22)
)

# Stretch it along X axis by creating proper shape
# Main elongated body
main_body = (
    cq.Workplane("XZ")
    .rect(80, 22)
    .extrude(30)
)

# Create the top angled surface by cutting
cutter_top = (
    cq.Workplane("XY")
    .workplane(offset=22)
    .transformed(rotate=(15, 0, 0))
    .rect(100, 50)
    .extrude(20)
)

# Build from scratch with proper shape
# Coffin/pod shape: hexagonal cross-section, elongated
w = cq.Workplane("YZ")
profile_pts = [
    (0, 0),
    (30, 0),
    (35, 8),
    (30, 22),
    (5, 26),
    (-5, 26),
    (-12, 18),
    (-12, 8),
]

main = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(78)
)

# Taper front end
front_cut = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(39, 0, 13), rotate=(0, -35, 0))
    .rect(60, 60)
    .extrude(40)
)

back_cut = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(-39, 0, 13), rotate=(0, 35, 0))
    .rect(60, 60)
    .extrude(40)
)

main = main.cut(front_cut).cut(back_cut)

# Add ventilation slots on top
slot_depth = 3
slots = []
for i in range(7):
    x_pos = -25 + i * 8
    slot = (
        cq.Workplane("XY")
        .workplane(offset=24)
        .transformed(offset=(x_pos, 5, 0), rotate=(0, 0, 30))
        .rect(1.5, 10)
        .extrude(5)
    )
    slots.append(slot)

for slot in slots:
    main = main.cut(slot)

# Side ventilation slots
for i in range(5):
    x_pos = -15 + i * 8
    slot_side = (
        cq.Workplane("XZ")
        .workplane(offset=18)
        .transformed(offset=(x_pos, 10, 0))
        .rect(1.5, 12)
        .extrude(5)
    )
    main = main.cut(slot_side)

# Add small cylinder on front (barrel/nozzle)
nozzle = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(42, -8, 5))
    .circle(3)
    .extrude(5)
)

main = main.union(nozzle)

# Fillet edges
result = main.edges("|Z").fillet(2)