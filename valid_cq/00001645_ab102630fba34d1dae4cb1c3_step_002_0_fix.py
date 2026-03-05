import cadquery as cq

# Part 1: The latch/cam piece (back piece with circular cam)
# Main bar
bar1 = (
    cq.Workplane("XY")
    .box(80, 15, 10)
)

# Add raised circular cam section in the middle
cam = (
    cq.Workplane("XY")
    .center(0, 0)
    .cylinder(10, 12)
)

# Combine bar with cam bump
part1 = bar1.union(cam)

# Add end blocks (raised sections at ends)
left_block = (
    cq.Workplane("XY")
    .center(-32, 0)
    .box(16, 15, 14)
)

right_block = (
    cq.Workplane("XY")
    .center(32, 0)
    .box(16, 15, 14)
)

part1 = part1.union(left_block).union(right_block)

# Cut circular profile on cam (the S-curve/cam shape)
cam_cut1 = (
    cq.Workplane("XY")
    .center(-8, 0)
    .cylinder(15, 8)
)

cam_cut2 = (
    cq.Workplane("XY")
    .center(8, 0)
    .cylinder(15, 8)
)

part1 = part1.cut(cam_cut1)

# Add mounting holes
part1 = (
    part1
    .faces(">Z")
    .workplane()
    .center(-32, 0)
    .circle(2.5)
    .cutThruAll()
)

part1 = (
    part1
    .faces(">Z")
    .workplane()
    .center(32, 0)
    .circle(2.5)
    .cutThruAll()
)

part1 = (
    part1
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(2.5)
    .cutThruAll()
)

# Translate part1 to position
part1 = part1.translate((0, 25, 0))

# Part 2: The serrated/notched piece (front piece with V-notches)
part2_base = (
    cq.Workplane("XY")
    .box(80, 15, 15)
)

# Cut V-notches on top face
# First notch
notch1 = (
    cq.Workplane("XZ")
    .center(10, 7.5)
    .polygon(3, 10)
    .extrude(15)
)

notch2 = (
    cq.Workplane("XZ")
    .center(25, 7.5)
    .polygon(3, 10)
    .extrude(15)
)

# Use a different approach for V-notches
# Create V-groove cuts using wedge shapes
def make_v_notch(x_pos, depth=5, width=8, length=15):
    pts = [
        (-width/2, 0),
        (0, -depth),
        (width/2, 0),
    ]
    notch = (
        cq.Workplane("XZ")
        .center(x_pos, 7.5)
        .polyline(pts)
        .close()
        .workplane()
        .extrude(length)
    )
    return notch

# Build part2 with notches cut from top
part2 = (
    cq.Workplane("XY")
    .box(80, 15, 15)
)

# Cut notches using box intersections to form V shapes
for x_pos in [5, 20]:
    v_pts = [
        (x_pos - 5, -8),
        (x_pos, -8 + 5),
        (x_pos + 5, -8),
        (x_pos + 5, 0),
        (x_pos - 5, 0),
    ]
    notch_solid = (
        cq.Workplane("XZ")
        .workplane(offset=-7.5)
        .polyline([(x_pos-5, 0), (x_pos, -5), (x_pos+5, 0)])
        .close()
        .extrude(15)
    )
    part2 = part2.cut(notch_solid)

# Position part2 below part1
part2 = part2.translate((0, -15, 0))

# Combine both parts
result = part1.union(part2)