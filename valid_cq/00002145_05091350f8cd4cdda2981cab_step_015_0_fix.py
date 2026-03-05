import cadquery as cq

# Fan frame - 80mm PC case fan frame
# Overall dimensions: ~80x80x25mm

outer_size = 80
inner_size = 70
height = 25
wall = 5
corner_r = 4
mount_hole_d = 4
mount_boss_d = 9
fan_circle_d = 75
hub_d = 20

# Create the outer square frame shell
outer_box = (
    cq.Workplane("XY")
    .rect(outer_size, outer_size)
    .extrude(height)
)

# Cut the inner opening (large square cutout)
inner_cut = (
    cq.Workplane("XY")
    .rect(outer_size - 2*wall, outer_size - 2*wall)
    .extrude(height)
)

frame = outer_box.cut(inner_cut)

# Add corner bosses for mounting holes
def add_corner_boss(frame, x, y):
    boss = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(mount_boss_d / 2)
        .extrude(height)
    )
    return frame.union(boss)

offset = outer_size / 2 - wall / 2 - 1
for sx in [-1, 1]:
    for sy in [-1, 1]:
        frame = add_corner_boss(frame, sx * (outer_size/2 - wall/2), sy * (outer_size/2 - wall/2))

# Cut mounting holes through corners
def cut_mount_hole(frame, x, y):
    hole = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(mount_hole_d / 2)
        .extrude(height)
    )
    return frame.cut(hole)

for sx in [-1, 1]:
    for sy in [-1, 1]:
        frame = cut_mount_hole(frame, sx * (outer_size/2 - wall/2), sy * (outer_size/2 - wall/2))

# Add circular fan opening ring (cylindrical shell inside the frame)
fan_ring_outer = (
    cq.Workplane("XY")
    .circle(fan_circle_d / 2)
    .extrude(height)
)

fan_ring_inner = (
    cq.Workplane("XY")
    .circle(fan_circle_d / 2 - wall)
    .extrude(height)
)

fan_ring = fan_ring_outer.cut(fan_ring_inner)
frame = frame.union(fan_ring)

# Add struts connecting circular ring to frame corners (4 diagonal struts)
import math

strut_w = 4
strut_h = height

def make_strut(angle_deg):
    angle = math.radians(angle_deg)
    # Strut from center outward
    x1 = (fan_circle_d/2 - wall) * math.cos(angle)
    y1 = (fan_circle_d/2 - wall) * math.sin(angle)
    x2 = (outer_size/2 - wall) * math.cos(angle)
    y2 = (outer_size/2 - wall) * math.sin(angle)
    
    length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    
    strut = (
        cq.Workplane("XY")
        .center(cx, cy)
        .rect(length + 2, strut_w)
        .extrude(strut_h)
        .rotate((0, 0, 0), (0, 0, 1), angle_deg)
    )
    return strut

for angle in [45, 135, 225, 315]:
    strut = make_strut(angle)
    frame = frame.union(strut)

# Add hub circle in center
hub_outer = (
    cq.Workplane("XY")
    .workplane(offset=height * 0.2)
    .circle(hub_d / 2)
    .extrude(height * 0.6)
)

hub_inner = (
    cq.Workplane("XY")
    .workplane(offset=height * 0.2)
    .circle(hub_d / 2 - 2)
    .extrude(height * 0.6)
)

hub = hub_outer.cut(hub_inner)
frame = frame.union(hub)

# Fillet the outer edges slightly
try:
    frame = frame.edges("|Z").fillet(corner_r)
except:
    pass

result = frame