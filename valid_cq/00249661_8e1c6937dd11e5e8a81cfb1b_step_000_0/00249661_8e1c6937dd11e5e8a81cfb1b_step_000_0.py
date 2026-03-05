import cadquery as cq

# --- Parameters ---
length = 120.0
width_center = 24.0
width_end = 8.0
thickness = 4.0
slot_width = 1.5
step = 6.0  # Spacing/pitch of the zigzag pattern
notch_width = 1.5
notch_depth = 1.0

# --- 1. Base Shape Generation ---
# Define points for the tapered, lozenge-like profile
pts = [
    (-length/2, width_end/2),
    (0, width_center/2),
    (length/2, width_end/2),
    (length/2, -width_end/2),
    (0, -width_center/2),
    (-length/2, -width_end/2)
]

# Create the main solid body
base = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# --- 2. Internal Serpentine Cut (Left/Center) ---
path_pts = []
# Start the pattern slightly to the right of the center
current_x = 12.0  
limit_x = -length/2 + 10  # Stop before reaching the very left tip
direction = 1  # 1 for Up, -1 for Down

# Start point on centerline, connecting to the straight slot
path_pts.append((current_x, 0))

while current_x > limit_x:
    # Calculate local width at current_x to ensure cut stays inside
    # Linear interpolation: y = mx + c (based on absolute distance from center)
    local_half_width = ((width_end - width_center) / length) * 2 * abs(current_x) + width_center/2
    
    # Determine turning point (margin from edge)
    turn_y = local_half_width - 3.5 
    
    # Add vertical segment point
    path_pts.append((current_x, direction * turn_y))
    
    # Add horizontal segment point
    next_x = current_x - step
    path_pts.append((next_x, direction * turn_y))
    
    # Update for next iteration
    current_x = next_x
    direction *= -1

# Create the wire path and thicken it into a slot
zigzag_wire = cq.Workplane("XY").polyline(path_pts)
# offset2D creates a face by thickening the wire. 'intersection' gives sharp corners.
zigzag_cut = zigzag_wire.offset2D(slot_width/2, kind='intersection').extrude(thickness)

# --- 3. Right Side Straight Slot (Fork) ---
# Calculates dimensions to run from the start of zigzag to the right tip
right_slot_start = 12.0
right_slot_len = (length/2) - right_slot_start + 2 # +2 to ensure it cuts through the end
right_slot = (cq.Workplane("XY")
              .rect(right_slot_len, slot_width)
              .translate((right_slot_start + right_slot_len/2 - 0.1, 0)) # -0.1 overlap
              .extrude(thickness))

# --- 4. Edge Notches ---
# Generate positions for notches along the tapered edges
notch_locs = []
# Align notches with the zigzag step for visual consistency
start_notch_x = -length/2 + step
end_notch_x = length/2 - step
num_notches = int((end_notch_x - start_notch_x) / step)

for i in range(num_notches + 1):
    x = start_notch_x + i * step
    
    # Calculate Y on the edge at this X
    local_half_width = ((width_end - width_center) / length) * 2 * abs(x) + width_center/2
    
    # Add notch locations for top and bottom
    notch_locs.append((x, local_half_width))
    notch_locs.append((x, -local_half_width))

# Create the cutting volume for notches
# Depth is doubled so a center-aligned rect cuts fully into the edge
edge_notches = (cq.Workplane("XY")
                .pushPoints(notch_locs)
                .rect(notch_width, notch_depth * 2)
                .extrude(thickness))

# --- 5. Final Boolean Operations ---
result = base.cut(zigzag_cut).cut(right_slot).cut(edge_notches)