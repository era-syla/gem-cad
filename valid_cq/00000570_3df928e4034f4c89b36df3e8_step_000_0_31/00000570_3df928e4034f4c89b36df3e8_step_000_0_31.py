import cadquery as cq

# --- Parameters ---
PYLON_RADIUS = 12
PYLON_LENGTH = 130
DAMPER_HEIGHT = 100
ANKLE_OFFSET_Z = 0
DAMPER_START_Z = PYLON_LENGTH

# --- 1. Foot Blades ---
# Left Toe
toe_l = (
    cq.Workplane("XZ")
    .moveTo(0, -10)
    .threePointArc((60, -60), (140, -80))
    .lineTo(135, -88)
    .threePointArc((60, -68), (-10, -15))
    .close()
    .extrude(14)
    .translate((0, 5, 0))
)

# Right Toe
toe_r = (
    cq.Workplane("XZ")
    .moveTo(0, -10)
    .threePointArc((60, -60), (140, -80))
    .lineTo(135, -88)
    .threePointArc((60, -68), (-10, -15))
    .close()
    .extrude(-14)
    .translate((0, -5, 0))
)

# Heel
heel = (
    cq.Workplane("XZ")
    .moveTo(-5, -15)
    .threePointArc((-30, -40), (-60, -50))
    .lineTo(-55, -58)
    .threePointArc((-30, -48), (5, -20))
    .close()
    .extrude(20, both=True)
)

# --- 2. Ankle Bracket ---
ankle_base = cq.Workplane("XY").workplane(offset=-15).box(42, 45, 30)

ankle_side_profile = (
    cq.Workplane("XZ")
    .moveTo(-22, 0)
    .lineTo(22, 0)
    .lineTo(28, -35)
    .lineTo(-28, -35)
    .close()
)
ankle_bracket = ankle_side_profile.extrude(45, both=True).intersect(ankle_base)

# Hollow out the ankle bracket
ankle_hollow = (
    cq.Workplane("XZ")
    .moveTo(-8, -5)
    .lineTo(8, -5)
    .lineTo(16, -40)
    .lineTo(-16, -40)
    .close()
    .extrude(26, both=True)
)
ankle_bracket = ankle_bracket.cut(ankle_hollow)

# Ankle cross-hole
ankle_hole = cq.Workplane("YZ").center(0, -15).circle(8).extrude(50, both=True)
ankle_bracket = ankle_bracket.cut(ankle_hole)

# Pylon collar and flare
ankle_collar = cq.Workplane("XY").circle(PYLON_RADIUS + 6).extrude(15)
ankle_flare = (
    cq.Workplane("XY")
    .workplane(offset=15)
    .circle(PYLON_RADIUS + 6)
    .workplane(offset=10)
    .circle(PYLON_RADIUS)
    .loft()
)
ankle_bracket = ankle_bracket.union(ankle_collar).union(ankle_flare)

foot_assembly = toe_l.union(toe_r).union(heel).union(ankle_bracket)

# --- 3. Pylon ---
pylon = (
    cq.Workplane("XY")
    .workplane(offset=25)
    .circle(PYLON_RADIUS)
    .extrude(PYLON_LENGTH - 25)
)

# --- 4. Upper Leg (Damper Unit) ---
# Lower Bracket
lower_bracket = cq.Workplane("XY").workplane(offset=DAMPER_START_Z).box(36, 46, 20)
damper_flare = (
    cq.Workplane("XY")
    .workplane(offset=DAMPER_START_Z - 15)
    .circle(PYLON_RADIUS)
    .workplane(offset=15)
    .circle(PYLON_RADIUS + 6)
    .loft()
)
lower_bracket = lower_bracket.union(damper_flare)

# Main Cylinder
damper_cyl = (
    cq.Workplane("XY")
    .workplane(offset=DAMPER_START_Z + 20)
    .circle(20)
    .extrude(DAMPER_HEIGHT - 40)
)
damper_rod = (
    cq.Workplane("XY")
    .workplane(offset=DAMPER_START_Z + DAMPER_HEIGHT - 20)
    .circle(12)
    .extrude(20)
)

# Upper Bracket
upper_bracket = cq.Workplane("XY").workplane(offset=DAMPER_START_Z + DAMPER_HEIGHT).box(42, 50, 20)

# Side Frames
frame_profile = (
    cq.Workplane("XZ")
    .moveTo(-10, DAMPER_START_Z + 10)
    .lineTo(15, DAMPER_START_Z + 10)
    .lineTo(25, DAMPER_START_Z + DAMPER_HEIGHT + 10)
    .lineTo(-15, DAMPER_START_Z + DAMPER_HEIGHT + 10)
    .close()
)
frame_plate = frame_profile.extrude(6)

frame_cutout = (
    cq.Workplane("XZ")
    .moveTo(-2, DAMPER_START_Z + 25)
    .lineTo(8, DAMPER_START_Z + 25)
    .lineTo(16, DAMPER_START_Z + DAMPER_HEIGHT - 10)
    .lineTo(-6, DAMPER_START_Z + DAMPER_HEIGHT - 10)
    .close()
    .extrude(10, both=True)
)
frame_plate = frame_plate.cut(frame_cutout)

frame_l = frame_plate.translate((0, 23, 0))
frame_r = frame_plate.translate((0, -29, 0))

# Pivot Pins
pin1 = cq.Workplane("YZ").center(0, DAMPER_START_Z + 10).circle(6).extrude(32, both=True)
pin2 = cq.Workplane("YZ").center(0, DAMPER_START_Z + DAMPER_HEIGHT + 10).circle(6).extrude(32, both=True)

damper_assembly = (
    lower_bracket.union(damper_cyl).union(damper_rod).union(upper_bracket)
    .union(frame_l).union(frame_r).union(pin1).union(pin2)
)

# --- 5. Knee Interface (Top Mount) ---
TOP_Z = DAMPER_START_Z + DAMPER_HEIGHT + 20
HINGE_X = 12
HINGE_Z = TOP_Z + 10

# Hinge base on top bracket
hinge_mount = cq.Workplane("XY").workplane(offset=TOP_Z).center(HINGE_X, 0).box(20, 24, 15)

# Tilted Socket Plate
plate_body = (
    cq.Workplane("XY")
    .box(65, 45, 8)
    .faces(">Z").workplane().rect(55, 35).extrude(2)
)
# Position hinge pivot at origin, tilt, and move to final position
plate_body = plate_body.translate((-25, 0, 4))
plate_body = plate_body.rotate((0, 0, 0), (0, 1, 0), -12)
plate_body = plate_body.translate((HINGE_X, 0, HINGE_Z))

# Top Hinge Pin
pin3 = cq.Workplane("YZ").workplane(offset=HINGE_X).center(0, HINGE_Z).circle(5).extrude(22, both=True)

top_assembly = hinge_mount.union(plate_body).union(pin3)

# --- Final Assembly ---
result = foot_assembly.union(pylon).union(damper_assembly).union(top_assembly)