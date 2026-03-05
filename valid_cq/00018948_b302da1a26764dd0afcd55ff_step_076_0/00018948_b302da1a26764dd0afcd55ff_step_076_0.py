import cadquery as cq
import math

# --- Parameters ---
# Plate dimensions
plate_width = 70.0
plate_height = 100.0
plate_thickness = 4.0
corner_radius = 5.0

# Motor mounting (approx NEMA 17/23 style)
motor_center_y = -20.0     # Offset from center of plate
mount_spacing = 31.0       # Distance between screw holes
center_hole_dia = 32.0     # Main pilot hole diameter
notch_dia = 4.0            # Diameter of relief notches on pilot hole
screw_hole_dia = 3.5       # Clearance for M3/M4
csk_dia = 7.0              # Countersink diameter
csk_angle = 90.0           # Countersink angle

# Ventilation slots
slot_count = 5
slot_width = 5.0
slot_length = 32.0
slot_pitch = 9.0           # Center-to-center spacing
slot_center_y = 25.0       # Vertical position of slots center

# --- Geometry Generation ---

# 1. Base Plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Motor Cutouts (Central hole + Notches)
# Calculate notch positions (45 degrees on the perimeter of the central hole)
notch_radius = center_hole_dia / 2.0
notch_locs = []
for angle in [45, 135, 225, 315]:
    rad = math.radians(angle)
    x = notch_radius * math.cos(rad)
    y = notch_radius * math.sin(rad)
    notch_locs.append((x, y))

# Create workplane centered on motor position
motor_wp = result.faces(">Z").workplane().center(0, motor_center_y)

# Cut the central large hole
result = motor_wp.circle(center_hole_dia / 2.0).cutThruAll()

# Cut the relief notches around the central hole
result = (
    result.faces(">Z")
    .workplane()
    .center(0, motor_center_y)
    .pushPoints(notch_locs)
    .circle(notch_dia / 2.0)
    .cutThruAll()
)

# 3. Mounting Holes (Countersunk)
mount_locs = [
    (mount_spacing / 2.0, mount_spacing / 2.0),
    (-mount_spacing / 2.0, mount_spacing / 2.0),
    (-mount_spacing / 2.0, -mount_spacing / 2.0),
    (mount_spacing / 2.0, -mount_spacing / 2.0),
]

result = (
    result.faces(">Z")
    .workplane()
    .center(0, motor_center_y)
    .pushPoints(mount_locs)
    .cskHole(screw_hole_dia, csk_dia, csk_angle)
)

# 4. Ventilation Slots
# Calculate x-positions for the slots to be centered horizontally
start_x = -((slot_count - 1) * slot_pitch) / 2.0
slot_locs = [(start_x + i * slot_pitch, 0) for i in range(slot_count)]

result = (
    result.faces(">Z")
    .workplane()
    .center(0, slot_center_y)
    .pushPoints(slot_locs)
    .slot2D(slot_length, slot_width, angle=90)
    .cutThruAll()
)