import cadquery as cq

# --- Dimensions & Parameters ---
thickness = 3.0
fillet_radius = 4.0

# Left Panel Section
p1_width = 80.0
p1_height = 120.0

# Right Panel Section
p2_width = 100.0
p2_height = 160.0

total_width = p1_width + p2_width

# Mounting holes
hole_diameter = 3.2
margin = 5.0

# --- Base Geometry ---
# Define the L-shaped profile points (starting bottom-left, counter-clockwise)
# Note: Coordinate system origin at bottom-left corner
pts = [
    (0, 0),
    (total_width, 0),
    (total_width, p2_height),
    (p1_width, p2_height),
    (p1_width, p1_height),
    (0, p1_height)
]

# Create the main solid plate
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    .edges("|Z") # Select vertical edges
    .fillet(fillet_radius)
)

# --- Left Panel Features ---

# 1. LCD Window Cutout
lcd_w, lcd_h = 48.0, 32.0
lcd_center_x = p1_width / 2
lcd_center_y = p1_height - 35.0
result = result.faces(">Z").workplane().moveTo(lcd_center_x, lcd_center_y).rect(lcd_w, lcd_h).cutThruAll()

# 2. LCD Mounting Screw Holes (4 corners relative to cutout)
lcd_hole_dx = lcd_w / 2 + 3.0
lcd_hole_dy = lcd_h / 2 + 3.0
lcd_mount_pts = [
    (lcd_center_x - lcd_hole_dx, lcd_center_y - lcd_hole_dy),
    (lcd_center_x + lcd_hole_dx, lcd_center_y - lcd_hole_dy),
    (lcd_center_x - lcd_hole_dx, lcd_center_y + lcd_hole_dy),
    (lcd_center_x + lcd_hole_dx, lcd_center_y + lcd_hole_dy),
]
result = result.faces(">Z").workplane().pushPoints(lcd_mount_pts).circle(1.5).cutThruAll()

# 3. Control Component Holes (Below LCD)
ctrl_y = lcd_center_y - (lcd_h / 2) - 12.0
result = result.faces(">Z").workplane().pushPoints([
    (lcd_center_x - 12, ctrl_y),
    (lcd_center_x + 12, ctrl_y)
]).circle(2.0).cutThruAll()
# Enlarge the left hole slightly based on visual
result = result.faces(">Z").workplane().moveTo(lcd_center_x - 12, ctrl_y).circle(2.8).cutThruAll()

# 4. Vertical Vents (Left)
vent_w = 5.0
vent_h = 30.0
vent_y = 30.0
num_vents_left = 5
vent_pitch_left = 11.0
vent_start_x_left = lcd_center_x - ((num_vents_left - 1) * vent_pitch_left) / 2

for i in range(num_vents_left):
    vx = vent_start_x_left + i * vent_pitch_left
    result = result.faces(">Z").workplane().moveTo(vx, vent_y).slot2D(vent_h, vent_w, 90).cutThruAll()

# 5. Bottom Edge Notch
notch_w = 12.0
notch_h = 4.0
result = result.faces(">Z").workplane().moveTo(lcd_center_x, 0).rect(notch_w, notch_h * 2).cutThruAll()

# 6. Mounting Holes (Left Panel Perimeter)
mh_left = [
    (margin, margin),
    (p1_width - margin, margin),
    (margin, p1_height - margin),
    (p1_width - margin, p1_height - margin)
]
result = result.faces(">Z").workplane().pushPoints(mh_left).circle(hole_diameter / 2).cutThruAll()


# --- Right Panel Features ---

p2_center_x = p1_width + (p2_width / 2)

# 1. Upper Cutouts
# Vertical Rectangle
r1_x = p1_width + 25.0
r1_y = p2_height - 40.0
result = result.faces(">Z").workplane().moveTo(r1_x, r1_y).rect(12.0, 18.0).cutThruAll()

# Small Square
sq_x = p1_width + 65.0
sq_y = p2_height - 30.0
result = result.faces(">Z").workplane().moveTo(sq_x, sq_y).rect(10.0, 10.0).cutThruAll()

# 2. Vertical Vents (Right)
vent_h_right = 40.0
vent_y_right = 45.0
num_vents_right = 5
vent_pitch_right = 14.0
vent_start_x_right = p2_center_x - ((num_vents_right - 1) * vent_pitch_right) / 2

for i in range(num_vents_right):
    vx = vent_start_x_right + i * vent_pitch_right
    result = result.faces(">Z").workplane().moveTo(vx, vent_y_right).slot2D(vent_h_right, vent_w, 90).cutThruAll()

# 3. Mounting Holes (Right Panel Perimeter)
mh_right = [
    (p1_width + margin, margin),              # Bottom Left (near seam)
    (total_width - margin, margin),           # Bottom Right
    (total_width - margin, p2_height / 2),    # Middle Right Edge
    (total_width - margin, p2_height - margin), # Top Right
    (p1_width + margin, p2_height - margin)   # Top Left (near seam)
]
result = result.faces(">Z").workplane().pushPoints(mh_right).circle(hole_diameter / 2).cutThruAll()

# Final export line usually expected in CQ editors (optional)
# show_object(result)