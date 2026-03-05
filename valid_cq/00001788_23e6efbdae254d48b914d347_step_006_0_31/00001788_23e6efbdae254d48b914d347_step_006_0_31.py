import cadquery as cq

# Parametric dimensions
w1 = 100.0
h1 = 140.0
w2 = 100.0
h2 = 160.0
step_y = 30.0
thickness = 3.0
margin = 6.0

# Base outline coordinates
pts = [
    (0.0, 0.0),
    (w1, 0.0),
    (w1, step_y),
    (w1 + w2, step_y),
    (w1 + w2, step_y + h2),
    (w1, step_y + h2),
    (w1, h1),
    (0.0, h1)
]

# Create base shape and fillet the vertical outer corners
base = cq.Workplane("XY").polyline(pts).close().extrude(thickness)
base = base.edges("|Z").fillet(2.0)

# Bottom rectangular notch
notch = cq.Workplane("XY").center(w1 / 2, 0).box(16, 16, thickness * 3).edges("|Z").fillet(1.0)
base = base.cut(notch)

# Vertical ventilation slots
slot_len = 39.0
slot_w = 6.0
slot_spacing = 16.0
dx_slots = [-2 * slot_spacing, -slot_spacing, 0, slot_spacing, 2 * slot_spacing]

# Left section slots
slot_y_left = 40.0
slot_pts_left = [(w1 / 2 + dx, slot_y_left) for dx in dx_slots]
base = base.faces(">Z").workplane().pushPoints(slot_pts_left).slot2D(slot_len, slot_w, 90).cutThruAll()

# Right section slots
slot_y_right = step_y + 40.0
slot_pts_right = [(w1 + w2 / 2 + dx, slot_y_right) for dx in dx_slots]
base = base.faces(">Z").workplane().pushPoints(slot_pts_right).slot2D(slot_len, slot_w, 90).cutThruAll()

# Large rectangular cutout on the left section
cutout_w = 70.0
cutout_h = 45.0
cutout_y = h1 - (cutout_h / 2) - 17.5
big_cut = cq.Workplane("XY").center(w1 / 2, cutout_y).box(cutout_w, cutout_h, thickness * 3).edges("|Z").fillet(2.0)
base = base.cut(big_cut)

# Small cutouts on the right section
c1 = cq.Workplane("XY").center(w1 + 35, step_y + 120).box(14, 22, thickness * 3).edges("|Z").fillet(1.0)
c2 = cq.Workplane("XY").center(w1 + 65, step_y + 125).box(12, 12, thickness * 3).edges("|Z").fillet(1.0)
base = base.cut(c1).cut(c2)

# Mounting holes (countersunk)
standard_holes = [
    # Left section outer corners
    (margin, h1 - margin), 
    (w1 - margin, h1 - margin),
    (margin, margin), 
    (w1 - margin, margin),
    (margin, h1 / 2),
    # Right section outer corners
    (w1 + margin, step_y + h2 - margin), 
    (w1 + w2 - margin, step_y + h2 - margin),
    (w1 + margin, step_y + margin), 
    (w1 + w2 - margin, step_y + margin),
    (w1 + w2 - margin, step_y + h2 / 2),
    # Additional surface holes
    (w1 / 2 - cutout_w / 2 - 5, cutout_y - cutout_h / 2 - 5),
    (w1 + w2 / 2, slot_y_right + 40)
]

base = base.faces(">Z").workplane().pushPoints(standard_holes).cskHole(3.2, 6.0, 90)

# Specific counterbored hole near the large cutout
cbore_x = w1 / 2 + cutout_w / 2 + 5
cbore_y = cutout_y - cutout_h / 2 - 5
base = base.faces(">Z").workplane().center(cbore_x, cbore_y).cboreHole(4.0, 8.0, 1.5)

# Final resulting geometry
result = base