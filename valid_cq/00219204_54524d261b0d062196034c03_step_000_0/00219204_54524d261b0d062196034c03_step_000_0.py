import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
length = 120.0          # Length of the straight section
width = 24.0            # Width of the strip
thickness = 2.0         # Thickness of the plate
head_radius = width / 2.0

# Serration details
serration_pitch = 2.0
serration_depth = 2.0
num_teeth = int(width / serration_pitch)
serration_pitch = width / num_teeth  # Adjust pitch slightly to fit width exactly

# Large holes details
large_hole_dia = 8.5
large_hole_positions = [(35.0, 0), (75.0, 0)]

# Slot details
slot_width = 7.0
slot_inner_x = -3.0     # X-coordinate of the center of the slot's rounded bottom

# Small holes details
small_hole_dia = 2.2
small_hole_pattern_radius = 6.0  # Distance from center (0,0)
small_hole_angles = [25, 0, -25] # Angles in degrees for the radial pattern

# --- Geometry Construction ---

# 1. Define the outline points for the main body
# Start at top-left of the rectangular section (where the head arc ends)
pts = [(0, width/2.0)]

# Top edge line
pts.append((length, width/2.0))

# Generate serrated edge (Right end)
# Create a zig-zag pattern downwards
for i in range(num_teeth):
    y_current = width/2.0 - i * serration_pitch
    # Tooth valley (inward)
    pts.append((length - serration_depth, y_current - serration_pitch/2.0))
    # Tooth peak (outward)
    pts.append((length, y_current - serration_pitch))

# Bottom edge line
pts.append((0, -width/2.0))

# 2. Create the base solid
# Draw polyline for the body and serrations, then close with a 3-point arc for the head
result = (cq.Workplane("XY")
          .polyline(pts)
          .threePointArc((-head_radius, 0), (0, width/2.0))
          .close()
          .extrude(thickness))

# 3. Cut the Slot
# Create a cutter composed of a rectangle (opening the slot) and a circle (rounding the bottom)
# Calculate rectangle dimensions to ensure it cuts through the outer edge
rect_start_x = -head_radius - 5.0
rect_len = slot_inner_x - rect_start_x
rect_center_x = rect_start_x + rect_len / 2.0

cutter_rect = (cq.Workplane("XY")
               .moveTo(rect_center_x, 0)
               .rect(rect_len, slot_width)
               .extrude(thickness))

cutter_round = (cq.Workplane("XY")
                .moveTo(slot_inner_x, 0)
                .circle(slot_width / 2.0)
                .extrude(thickness))

slot_cutter = cutter_rect.union(cutter_round)
result = result.cut(slot_cutter)

# 4. Cut Large Holes
result = (result.faces(">Z").workplane()
          .pushPoints(large_hole_positions)
          .hole(large_hole_dia))

# 5. Cut Small Holes
# Calculate hole coordinates based on polar coordinates
small_hole_pts = []
for angle in small_hole_angles:
    rad = math.radians(angle)
    # 0 degrees is along +X axis
    x = small_hole_pattern_radius * math.cos(rad)
    y = small_hole_pattern_radius * math.sin(rad)
    small_hole_pts.append((x, y))

result = (result.faces(">Z").workplane()
          .pushPoints(small_hole_pts)
          .hole(small_hole_dia))