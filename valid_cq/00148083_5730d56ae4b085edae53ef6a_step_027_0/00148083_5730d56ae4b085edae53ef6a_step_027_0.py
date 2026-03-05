import cadquery as cq

# --- Parameters ---
thickness = 2.5           # Thickness of the plate
total_length = 320.0      # Approximate total length

# Left Head (Hexagonal/Pentagonal Mount)
head_front_offset = 40.0  # Distance from origin to front edge
head_width_front = 50.0   # Width at the very front
head_width_max = 90.0     # Maximum width of the head
head_straight_len = 20.0  # Length of the straight widest section
head_taper_len = 45.0     # Length of the transition taper to the beam

# Beam (Central Section)
beam_width = 38.0

# Right Tail (Rounded Mount)
tail_taper_start_x = 230.0 # X coordinate where beam starts widening
tail_center_x = 260.0      # Center of the right mount hole
tail_width = 55.0          # Width at the tail
tail_radius = tail_width / 2

# Hole Dimensions
bore_dia_large = 25.0      # Large center holes
hole_dia_small = 3.2       # Mounting screw holes
hole_dia_mid = 4.0         # Central beam hole
mount_pattern_side = 22.0  # Square pattern side length for motors

# --- Geometry Construction ---

# 1. Define the Profile Points (Top Half)
# Origin (0,0) is placed at the center of the Left Motor Mount
pts = []
# Start at the center of the front edge
pts.append((-head_front_offset, 0))
# Front corner
pts.append((-head_front_offset, head_width_front / 2))
# Angled corner to max width
pts.append((-head_front_offset + 15.0, head_width_max / 2))
# End of straight max width section
pts.append((-head_front_offset + 15.0 + head_straight_len, head_width_max / 2))
# End of taper (Start of Beam)
beam_start_x = -head_front_offset + 15.0 + head_straight_len + head_taper_len
pts.append((beam_start_x, beam_width / 2))
# End of Beam (Start of Tail Taper)
pts.append((tail_taper_start_x, beam_width / 2))
# Tail Widening point
pts.append((tail_center_x, tail_width / 2))

# 2. Draw the Outline
# Initialize Workplane
sketch = cq.Workplane("XY").moveTo(*pts[0])

# Trace top half
for p in pts[1:]:
    sketch = sketch.lineTo(*p)

# Create rounded end (180 degree arc)
sketch = sketch.threePointArc(
    (tail_center_x + tail_radius, 0),    # Mid point of arc
    (tail_center_x, -tail_width / 2)     # End point of arc
)

# Trace bottom half (Mirror of top points)
# Iterate in reverse, skipping the last point (which matches arc start)
for p in reversed(pts[:-1]):
    sketch = sketch.lineTo(p[0], -p[1])

# Close and Extrude
result = sketch.close().extrude(thickness)

# --- Machining Features (Holes) ---

# 1. Left Motor Mount (Origin)
result = (
    result.faces(">Z").workplane()
    # Large center bore
    .moveTo(0, 0)
    .circle(bore_dia_large / 2).cutThruAll()
    # Mounting Screw Pattern
    .moveTo(0, 0)
    .rect(mount_pattern_side, mount_pattern_side, forConstruction=True)
    .vertices()
    .circle(hole_dia_small / 2).cutThruAll()
)

# 2. Right Motor Mount
result = (
    result.faces(">Z").workplane()
    # Large center bore
    .moveTo(tail_center_x, 0)
    .circle(bore_dia_large / 2).cutThruAll()
    # Mounting Screw Pattern
    .moveTo(tail_center_x, 0)
    .rect(mount_pattern_side, mount_pattern_side, forConstruction=True)
    .vertices()
    .circle(hole_dia_small / 2).cutThruAll()
)

# 3. Perimeter Holes on Left Head (Visual match)
# Add small holes near the front corners
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (-head_front_offset + 5, head_width_front/2 - 5),
        (-head_front_offset + 5, -head_width_front/2 + 5)
    ])
    .circle(hole_dia_small / 2).cutThruAll()
)

# 4. Beam Central Hole
beam_mid_x = (beam_start_x + tail_taper_start_x) / 2
result = (
    result.faces(">Z").workplane()
    .moveTo(beam_mid_x, 0)
    .circle(hole_dia_mid / 2).cutThruAll()
)

# 5. Beam Edge Holes
# Calculate positions for holes along the beam edges
edge_hole_positions = []
num_pairs = 3
step = (tail_taper_start_x - beam_start_x) / (num_pairs + 1)
y_offset = beam_width / 2 - 4.0 # 4mm from edge

for i in range(1, num_pairs + 1):
    x_pos = beam_start_x + i * step
    edge_hole_positions.append((x_pos, y_offset))
    edge_hole_positions.append((x_pos, -y_offset))

result = (
    result.faces(">Z").workplane()
    .pushPoints(edge_hole_positions)
    .circle(hole_dia_small / 2).cutThruAll()
)