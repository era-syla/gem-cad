import cadquery as cq
import math

# --- Parameters ---
length = 300.0        # Length of the extrusion
size = 20.0           # Width/Height of the profile (20mm)
corner_radius = 1.0   # Radius of the outer corners
center_hole_dia = 5.0 # Diameter of the central hole

# T-Slot Dimensions (approximate for 2020 profile)
slot_opening = 6.0    # Width of the slot opening
slot_lip = 1.5        # Depth of the narrow opening part
slot_inner_w = 9.0    # Width of the inner cavity
slot_depth = 5.5      # Total depth of the slot from the face

# --- Helper Function ---
def get_slot_polygon(angle_deg):
    """
    Generates the coordinates for a T-slot cutout polygon, 
    rotated by the given angle.
    """
    # Define points for the top slot (centered at X=0, Y=size/2)
    # The shape is an inverted T projecting downwards from the top edge
    pts = [
        (slot_opening / 2, size / 2),
        (slot_opening / 2, size / 2 - slot_lip),
        (slot_inner_w / 2, size / 2 - slot_lip),
        (slot_inner_w / 2, size / 2 - slot_depth),
        (-slot_inner_w / 2, size / 2 - slot_depth),
        (-slot_inner_w / 2, size / 2 - slot_lip),
        (-slot_opening / 2, size / 2 - slot_lip),
        (-slot_opening / 2, size / 2)
    ]
    
    # Rotate points around origin (0,0)
    rad = math.radians(angle_deg)
    rot_pts = []
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    for x, y in pts:
        rx = x * cos_a - y * sin_a
        ry = x * sin_a + y * cos_a
        rot_pts.append((rx, ry))
        
    return rot_pts

# --- Geometry Construction ---

# 1. Create the base profile sketch
# Start with a square, round the corners, and subtract the center hole
profile_sketch = (
    cq.Sketch()
    .rect(size, size)
    .vertices()
    .fillet(corner_radius)
    .circle(center_hole_dia / 2, mode='s')
)

# 2. Subtract the T-slots on all 4 sides
for angle in [0, 90, 180, 270]:
    slot_points = get_slot_polygon(angle)
    profile_sketch = profile_sketch.polygon(slot_points, mode='s')

# 3. Extrude the sketch to create the 3D solid
result = cq.Workplane("XY").placeSketch(profile_sketch).extrude(length)