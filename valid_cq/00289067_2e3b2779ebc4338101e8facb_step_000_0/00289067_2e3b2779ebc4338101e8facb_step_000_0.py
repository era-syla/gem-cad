import cadquery as cq

# --- Parameters ---
length = 480.0
width = 160.0
thickness = 1.5
fillet_rad = 2.0

# --- Base Plate ---
# Create the main rectangular sheet
result = cq.Workplane("XY").box(length, width, thickness)

# --- Edge Profiling ---
# Corner notches (rectangular cutouts at the four corners)
corner_notch_sz = 12.0
corner_points = [
    (length/2, width/2), (length/2, -width/2),
    (-length/2, width/2), (-length/2, -width/2)
]
result = result.faces(">Z").workplane().pushPoints(corner_points).rect(corner_notch_sz*2, corner_notch_sz*2).cutThruAll()

# Edge cutouts (tabs/reliefs along the long edges)
edge_cut_w = 30.0
edge_cut_d = 4.0
edge_points = [
    (length/3.5, width/2), (-length/3.5, width/2),
    (length/3.5, -width/2), (-length/3.5, -width/2)
]
result = result.faces(">Z").workplane().pushPoints(edge_points).rect(edge_cut_w, edge_cut_d*2).cutThruAll()

# --- Fan Vents ---
# Create the circular fan vents with spoke pattern
fan_x_offset = 145.0
fan_outer_r = 34.0
fan_hub_r = 10.0
spoke_width = 8.0

for x_pos in [fan_x_offset, -fan_x_offset]:
    # 1. Cut the main outer hole
    result = result.faces(">Z").workplane().moveTo(x_pos, 0).circle(fan_outer_r).cutThruAll()
    
    # 2. Add the central hub back
    result = result.faces(">Z").workplane().moveTo(x_pos, 0).circle(fan_hub_r).extrude(thickness)
    
    # 3. Add the three spokes connecting hub to rim
    # We create 3 rectangles rotated by 120 degrees
    for i in range(3):
        angle = i * 120
        result = (result.faces(">Z").workplane()
                  .moveTo(x_pos, 0)
                  .transformed(rotate=cq.Vector(0, 0, angle))
                  .rect(fan_outer_r * 2, spoke_width)
                  .extrude(thickness))

# --- Rectangular Slots ---
# Add various rectangular cutouts across the body
rect_slots = [
    # Centerline slots
    (0, 50, 12, 8), (0, -50, 12, 8),
    (70, 0, 15, 10), (-70, 0, 15, 10),
    # Larger slots near fans
    (90, 40, 18, 12), (90, -40, 18, 12),
    (-90, 40, 18, 12), (-90, -40, 18, 12),
    # Slots near ends
    (210, 0, 10, 25), (-210, 0, 10, 25)
]

for (x, y, w, h) in rect_slots:
    result = result.faces(">Z").workplane().moveTo(x, y).rect(w, h).cutThruAll()

# --- Mounting Holes ---
# Grid of small mounting holes
hole_dia = 3.2
hole_points = []

# Edge rows
for x in range(-200, 201, 50):
    # Avoid placing holes inside the fan area
    if not (120 < abs(x) < 170):
        hole_points.append((x, 72))
        hole_points.append((x, -72))

# Inner scattered holes
inner_holes = [
    (35, 25), (35, -25), (-35, 25), (-35, -25),
    (110, 30), (110, -30), (-110, 30), (-110, -30)
]
hole_points.extend(inner_holes)

result = result.faces(">Z").workplane().pushPoints(hole_points).circle(hole_dia/2).cutThruAll()

# --- Central Boss ---
# Small standoff in the center
boss_dia = 5.0
boss_h = 4.0
result = result.faces(">Z").workplane().circle(boss_dia).extrude(boss_h)
# Threaded hole in boss
result = result.faces(">Z").workplane().circle(2.0).cutBlind(-10)

# --- Reinforcement Rails ---
# Raised ribs running along the length
rail_y_offset = 58.0
rail_length = 320.0
rail_width = 5.0
rail_height = 2.0

# Create rails
rail_locs = [(0, rail_y_offset), (0, -rail_y_offset)]
result = result.faces(">Z").workplane().pushPoints(rail_locs).rect(rail_length, rail_width).extrude(rail_height)

# Add slots inside the rails for detail
rail_slot_len = 100.0
rail_slot_w = 2.0
result = result.faces(">Z").workplane().pushPoints(rail_locs).rect(rail_slot_len, rail_slot_w).cutBlind(-rail_height)

# --- Final Export ---
# The 'result' variable contains the final geometry