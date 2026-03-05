import cadquery as cq

# Build a camera/electronics mount bracket assembly
# Main components: vertical back plate, horizontal base plate, side walls, mounting features

# --- Back plate (vertical) ---
back_plate = (
    cq.Workplane("XY")
    .rect(60, 50)
    .extrude(3)
)

# Window cutout in back plate
back_plate = (
    back_plate
    .faces(">Z")
    .workplane()
    .rect(40, 32)
    .cutThruAll()
)

# Mounting tabs on back plate corners
def add_mount_holes(wp):
    return (
        wp.faces(">Z")
        .workplane()
        .pushPoints([(-25, 20), (25, 20), (-25, -20), (25, -20)])
        .circle(2.5)
        .cutThruAll()
    )

back_plate = add_mount_holes(back_plate)

# --- Base/bottom frame (horizontal) ---
base_frame = (
    cq.Workplane("XZ")
    .center(0, -3)
    .rect(60, 40)
    .extrude(3)
)

# Cutout in base frame
base_frame = (
    base_frame
    .faces(">Y")
    .workplane()
    .rect(42, 30)
    .cutThruAll()
)

# --- Left side wall (angled support) ---
pts = [(0, 0), (35, 0), (35, 3), (3, 3), (0, 0)]
left_wall = (
    cq.Workplane("YZ")
    .center(-25, -3)
    .polyline(pts)
    .close()
    .extrude(3)
)

# --- Right side wall ---
right_wall = (
    cq.Workplane("YZ")
    .center(22, -3)
    .polyline(pts)
    .close()
    .extrude(3)
)

# --- Front frame lip ---
front_lip = (
    cq.Workplane("XY")
    .center(0, -40)
    .rect(60, 6)
    .extrude(3)
)

# --- Bottom support triangle (left) ---
tri_pts = [(0, 0), (30, 0), (0, 25)]
tri_left = (
    cq.Workplane("XZ")
    .center(-25, -3)
    .polyline(tri_pts)
    .close()
    .extrude(3)
)

# --- Bottom support triangle (right) ---
tri_right = (
    cq.Workplane("XZ")
    .center(22, -3)
    .polyline(tri_pts)
    .close()
    .extrude(3)
)

# --- Small mounting boss cylinders ---
boss1 = (
    cq.Workplane("XY")
    .center(-22, -38)
    .circle(4)
    .extrude(6)
)

boss2 = (
    cq.Workplane("XY")
    .center(22, -38)
    .circle(4)
    .extrude(6)
)

# Holes in bosses
boss1 = boss1.faces(">Z").workplane().circle(1.5).cutThruAll()
boss2 = boss2.faces(">Z").workplane().circle(1.5).cutThruAll()

# --- Side clips/rails ---
rail_left = (
    cq.Workplane("XY")
    .center(-32, -20)
    .rect(4, 20)
    .extrude(8)
)

rail_right = (
    cq.Workplane("XY")
    .center(32, -20)
    .rect(4, 20)
    .extrude(8)
)

# --- Small detail blocks on front ---
detail1 = (
    cq.Workplane("XY")
    .center(15, -30)
    .rect(8, 6)
    .extrude(8)
)

detail2 = (
    cq.Workplane("XY")
    .center(22, -22)
    .rect(5, 5)
    .extrude(10)
)

# --- Combine all parts ---
result = (
    back_plate
    .union(base_frame)
    .union(left_wall)
    .union(right_wall)
    .union(front_lip)
    .union(tri_left)
    .union(tri_right)
    .union(boss1)
    .union(boss2)
    .union(rail_left)
    .union(rail_right)
    .union(detail1)
    .union(detail2)
)