import cadquery as cq

# Parameters for the geometry
length = 140.0
width = 24.0
thickness = 3.0

# Feature parameters
notch_width = 8.0
notch_depth = 4.0
tab_width = 5.0
tab_protrusion = 2.0
tab_offset = 2.0  # Distance from the corner to the start of the tab

# Hole pattern parameters
hole_diameter = 2.2
hole_spacing = 6.0
grid_rows = 3
grid_cols = 3
first_hole_margin = 4.0 # Distance from notch depth to first column of holes

# Define the outer profile of the plate using a 2D polyline path
# Path is defined counter-clockwise starting from the top-left corner
pts = []

# --- Top Edge ---
# Start at top-left corner
pts.append((-length/2, width/2))
# Left tab bump
pts.append((-length/2 + tab_offset, width/2))
pts.append((-length/2 + tab_offset, width/2 + tab_protrusion))
pts.append((-length/2 + tab_offset + tab_width, width/2 + tab_protrusion))
pts.append((-length/2 + tab_offset + tab_width, width/2))
# Right tab bump
pts.append((length/2 - tab_offset - tab_width, width/2))
pts.append((length/2 - tab_offset - tab_width, width/2 + tab_protrusion))
pts.append((length/2 - tab_offset, width/2 + tab_protrusion))
pts.append((length/2 - tab_offset, width/2))
pts.append((length/2, width/2))

# --- Right Edge ---
# Notch cutout
pts.append((length/2, notch_width/2))
pts.append((length/2 - notch_depth, notch_width/2))
pts.append((length/2 - notch_depth, -notch_width/2))
pts.append((length/2, -notch_width/2))
pts.append((length/2, -width/2))

# --- Bottom Edge ---
# Right tab bump (mirrored)
pts.append((length/2 - tab_offset, -width/2))
pts.append((length/2 - tab_offset, -width/2 - tab_protrusion))
pts.append((length/2 - tab_offset - tab_width, -width/2 - tab_protrusion))
pts.append((length/2 - tab_offset - tab_width, -width/2))
# Left tab bump (mirrored)
pts.append((-length/2 + tab_offset + tab_width, -width/2))
pts.append((-length/2 + tab_offset + tab_width, -width/2 - tab_protrusion))
pts.append((-length/2 + tab_offset, -width/2 - tab_protrusion))
pts.append((-length/2 + tab_offset, -width/2))
pts.append((-length/2, -width/2))

# --- Left Edge ---
# Notch cutout (mirrored)
pts.append((-length/2, -notch_width/2))
pts.append((-length/2 + notch_depth, -notch_width/2))
pts.append((-length/2 + notch_depth, notch_width/2))
pts.append((-length/2, notch_width/2))
# Close loop back to start
pts.append((-length/2, width/2))

# Create the main solid body
result = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# --- Holes ---
# Calculate hole positions for the left grid
hole_points = []
start_x = -length/2 + notch_depth + first_hole_margin

for col in range(grid_cols):
    for row in range(grid_rows):
        # Center rows around Y=0
        y_pos = (row - (grid_rows - 1) / 2) * hole_spacing
        x_pos = start_x + (col * hole_spacing)
        hole_points.append((x_pos, y_pos))

# Generate symmetric points for the right side
all_hole_points = hole_points + [(-x, y) for x, y in hole_points]

# Cut the holes
result = result.faces(">Z").workplane().pushPoints(all_hole_points).hole(hole_diameter)