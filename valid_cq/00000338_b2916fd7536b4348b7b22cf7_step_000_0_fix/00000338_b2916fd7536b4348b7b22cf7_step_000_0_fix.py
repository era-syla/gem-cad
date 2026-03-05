import cadquery as cq

# Build a robotic arm / bracket assembly from scratch
# Components: base, vertical column, elbow joint, upper arm, head/mount

# --- Base plate ---
base = (
    cq.Workplane("XY")
    .box(60, 40, 8)
)

# Add feet/rails on bottom of base
base = (
    base
    .faces("<Z")
    .workplane()
    .rect(50, 30)
    .extrude(3)
)

# --- Vertical column ---
column = (
    cq.Workplane("XY")
    .workplane(offset=8)
    .rect(22, 18)
    .extrude(90)
)

# Taper the column slightly by adding a transition piece
col_transition = (
    cq.Workplane("XY")
    .workplane(offset=6)
    .rect(35, 25)
    .extrude(6)
)

# --- Elbow joint area (ornamental connector) ---
elbow_base = (
    cq.Workplane("XY")
    .workplane(offset=98)
    .rect(38, 30)
    .extrude(12)
)

# Circular cutouts on elbow sides
elbow_left = (
    cq.Workplane("XZ")
    .workplane(offset=15)
    .circle(9)
    .extrude(8)
)

elbow_right = (
    cq.Workplane("XZ")
    .workplane(offset=-15)
    .circle(9)
    .extrude(8)
)

# --- Upper arm (angled bracket from elbow to head) ---
upper_arm = (
    cq.Workplane("XY")
    .workplane(offset=110)
    .transformed(offset=(10, 0, 0))
    .rect(16, 14)
    .extrude(50)
)

# --- Head/mount box ---
head = (
    cq.Workplane("XY")
    .workplane(offset=155)
    .transformed(offset=(18, 0, 0))
    .rect(40, 35)
    .extrude(40)
)

# Add mounting plate on front of head
mount_plate = (
    cq.Workplane("XZ")
    .workplane(offset=17.5 + 18)
    .transformed(offset=(0, 175, 0))
    .rect(35, 38)
    .extrude(4)
)

# Head side bracket
head_bracket_r = (
    cq.Workplane("XY")
    .workplane(offset=155)
    .transformed(offset=(38, 0, 0))
    .rect(8, 35)
    .extrude(40)
)

# Combine all parts
result = (
    base
    .union(col_transition)
    .union(column)
    .union(elbow_base)
    .union(upper_arm)
    .union(head)
    .union(head_bracket_r)
)

# Cut circular hole in elbow joint
result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints([(0, 104)])
    .circle(7)
    .cutThruAll()
)

# Cut rectangular window in head
result = (
    result
    .faces(">Y")
    .workplane()
    .transformed(offset=(18, 175, 0))
    .rect(20, 22)
    .cutThruAll()
)

# Add hole in head mount
result = (
    result
    .faces(">X")
    .workplane()
    .transformed(offset=(0, 175, 0))
    .circle(8)
    .cutThruAll()
)

# Fillet the column edges
result = (
    result
    .edges("|Z")
    .fillet(2)
)