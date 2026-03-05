import cadquery as cq

# Build a simple robot figure using basic primitives

# --- Body (torso) ---
body = (
    cq.Workplane("XY")
    .box(14, 8, 18)
)

# --- Head (dome on top of body) ---
head_base = (
    cq.Workplane("XY")
    .workplane(offset=9)
    .box(10, 8, 8)
)

head_dome = (
    cq.Workplane("XY")
    .workplane(offset=17)
    .sphere(5)
)

# Antenna on head
antenna = (
    cq.Workplane("XY")
    .workplane(offset=22)
    .cylinder(3, 0.8)
)
antenna_ball = (
    cq.Workplane("XY")
    .workplane(offset=25.5)
    .sphere(1.2)
)

# --- Neck ---
neck = (
    cq.Workplane("XY")
    .workplane(offset=9)
    .cylinder(2, 1.5)
)

# --- Left arm (extending left) ---
left_upper_arm = (
    cq.Workplane("YZ")
    .workplane(offset=7)
    .cylinder(8, 1.2)
)

left_lower_arm = (
    cq.Workplane("YZ")
    .workplane(offset=18)
    .cylinder(8, 0.9)
)

left_hand = (
    cq.Workplane("XY")
    .workplane(offset=2)
    .transformed(offset=cq.Vector(18, 0, 2))
    .box(4, 2, 1.5)
)

# --- Right arm (extending right) ---
right_upper_arm = (
    cq.Workplane("YZ")
    .workplane(offset=-7)
    .cylinder(8, 1.2)
)

right_lower_arm = (
    cq.Workplane("YZ")
    .workplane(offset=-18)
    .cylinder(8, 0.9)
)

right_hand = (
    cq.Workplane("XY")
    .workplane(offset=2)
    .transformed(offset=cq.Vector(-18, 0, 2))
    .box(4, 2, 1.5)
)

# --- Legs ---
left_leg = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(4, 0, -14))
    .cylinder(10, 1.5)
)

right_leg = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-4, 0, -14))
    .cylinder(10, 1.5)
)

# --- Feet ---
left_foot = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(4, 1, -19))
    .box(5, 7, 2.5)
)

right_foot = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-4, 1, -19))
    .box(5, 7, 2.5)
)

# --- Shoulder joints ---
left_shoulder = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(7, 0, 2))
    .sphere(2.5)
)

right_shoulder = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-7, 0, 2))
    .sphere(2.5)
)

# Elbow joints
left_elbow = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(15, 0, 2))
    .sphere(1.5)
)

right_elbow = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-15, 0, 2))
    .sphere(1.5)
)

# Combine all parts using union
result = (
    body
    .union(head_base)
    .union(head_dome)
    .union(antenna)
    .union(antenna_ball)
    .union(neck)
    .union(left_upper_arm)
    .union(left_lower_arm)
    .union(left_hand)
    .union(right_upper_arm)
    .union(right_lower_arm)
    .union(right_hand)
    .union(left_leg)
    .union(right_leg)
    .union(left_foot)
    .union(right_foot)
    .union(left_shoulder)
    .union(right_shoulder)
    .union(left_elbow)
    .union(right_elbow)
)