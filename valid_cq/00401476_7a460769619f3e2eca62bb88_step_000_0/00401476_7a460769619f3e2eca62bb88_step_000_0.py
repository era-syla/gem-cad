import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 300.0          # Length of the extrusion profile
profile_size = 20.0     # Width/Height of the square profile (20mm standard)
fillet_radius = 1.5     # Radius of the external corners

# Hole dimensions
center_hole_d = 5.0     # Diameter of the central bore
corner_hole_d = 2.0     # Diameter of the small corner holes

# T-Slot dimensions
slot_opening = 6.2      # Width of the slot opening (surface)
slot_depth = 6.0        # Total depth of the slot
inner_w = 11.0          # Width of the internal T-cavity
inner_h = 2.0           # Height of the internal T-cavity
neck_h = slot_depth - inner_h  # Calculated height of the slot neck

# --- Modeling Process ---

# Initialize a Sketch for the 2D cross-section
s = cq.Sketch()

# 1. Base Geometry: Square with rounded corners
s = s.rect(profile_size, profile_size)
s = s.vertices().fillet(fillet_radius)

# 2. Subtract the Center Hole
s = s.circle(center_hole_d / 2, mode='s')

# 3. Subtract Corner Holes
# Positioned diagonally towards the corners
offset = (profile_size / 2) - 3.5  # Offset from center
s = s.rarray(2 * offset, 2 * offset, 2, 2).circle(corner_hole_d / 2, mode='s')

# 4. Subtract T-Slots
# We create the T-shape cutouts on all four sides (Top, Bottom, Left, Right).
# Each T-slot is modeled as two rectangles: the 'Neck' and the 'Inner' cavity.

# Top Slot (Y+)
s = s.push([(0, profile_size/2 - neck_h/2)])
s = s.rect(slot_opening, neck_h, mode='s')
s = s.push([(0, profile_size/2 - neck_h - inner_h/2)])
s = s.rect(inner_w, inner_h, mode='s')

# Bottom Slot (Y-)
s = s.push([(0, -(profile_size/2 - neck_h/2))])
s = s.rect(slot_opening, neck_h, mode='s')
s = s.push([(0, -(profile_size/2 - neck_h - inner_h/2))])
s = s.rect(inner_w, inner_h, mode='s')

# Right Slot (X+)
# Dimensions are swapped (width becomes height) for horizontal slots
s = s.push([(profile_size/2 - neck_h/2, 0)])
s = s.rect(neck_h, slot_opening, mode='s')
s = s.push([(profile_size/2 - neck_h - inner_h/2, 0)])
s = s.rect(inner_h, inner_w, mode='s')

# Left Slot (X-)
s = s.push([(-(profile_size/2 - neck_h/2), 0)])
s = s.rect(neck_h, slot_opening, mode='s')
s = s.push([(-(profile_size/2 - neck_h - inner_h/2), 0)])
s = s.rect(inner_h, inner_w, mode='s')

# --- Extrusion ---
# Place the 2D sketch on the XY plane and extrude along Z to form the bar
result = cq.Workplane("XY").placeSketch(s).extrude(length)