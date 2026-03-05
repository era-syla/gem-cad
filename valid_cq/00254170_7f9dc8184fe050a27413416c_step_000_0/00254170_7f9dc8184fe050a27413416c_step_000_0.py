import cadquery as cq
import math

# --- Parameters ---
thickness = 10.0      # Total thickness of the gun frame
wall_thick = 2.5      # Thickness of the side walls
gap = thickness - 2 * wall_thick # Internal gap for mechanism
fillet_radius = 1.0   # Edge softening radius

# --- Helper Functions ---
def star_profile(center, r_outer, r_inner, num_points):
    """Generates points for a star shape"""
    pts = []
    for i in range(2 * num_points):
        angle = math.pi * i / num_points + math.pi/2  # Rotate to align nicely
        r = r_outer if i % 2 == 0 else r_inner
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        pts.append((x, y))
    return pts

# --- 1. Main Frame Body ---
# Define the side profile of the gun frame
# Coordinate system origin approx near trigger pivot
frame_pts = [
    (-55, -35), # Handle bottom rear
    (-15, -15), # Handle meets body
    (25, -15),  # Front bottom
    (25, 5),    # Front face top
    (15, 5),    # Barrel top start
    (5, 12),    # Top of cylinder hump
    (-5, 10),   # Body top dip
    (-10, 22),  # Rise to hammer ear
    (-24, 22),  # Hammer ear top
    (-24, 12),  # Hammer ear back undercut
    (-55, -22)  # Handle top rear
]

# Create base solid
frame = (
    cq.Workplane("XY")
    .polyline(frame_pts)
    .close()
    .extrude(thickness)
)

# Smooth the edges
frame = frame.edges("|Z").fillet(fillet_radius)

# --- 2. Internal Slot ---
# Cut out the center to form the two side plates
slot_pts = [
    (-56, -36), # Start outside handle
    (-14, -16), 
    (15, -16),  # Stop before front block
    (15, 30),   # Up through top
    (-30, 30),
    (-30, 11),
    (-56, -23)
]

slot_solid = (
    cq.Workplane("XY")
    .polyline(slot_pts)
    .close()
    .extrude(gap)
    .translate((0, 0, wall_thick))
)

frame = frame.cut(slot_solid)

# --- 3. Cylinder / Boss Features ---
# Add cylindrical bosses on the sides
boss_center = (5, 0)
boss_radius = 7.0
boss_height = 2.5

boss_right = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .moveTo(*boss_center)
    .circle(boss_radius)
    .extrude(boss_height)
)

boss_left = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(*boss_center)
    .circle(boss_radius)
    .extrude(-boss_height)
)

frame = frame.union(boss_right).union(boss_left)

# Add a small hole in the handle (seen in image)
handle_hole = (
    cq.Workplane("XY")
    .moveTo(-35, -25)
    .circle(1.2)
    .extrude(thickness)
)
frame = frame.cut(handle_hole)

# --- 4. Hammer (Star Wheel) ---
hammer_pos = (-17, 17)
hammer_pts = star_profile(hammer_pos, r_outer=8, r_inner=4.5, num_points=10)

hammer = (
    cq.Workplane("XY")
    .polyline(hammer_pts)
    .close()
    .extrude(gap - 0.5) # Slightly thinner than gap for clearance
    .translate((0, 0, wall_thick + 0.25))
)

# Hammer Pivot Pin
hammer_pin = (
    cq.Workplane("XY")
    .moveTo(*hammer_pos)
    .circle(2.0)
    .extrude(thickness)
)
frame = frame.union(hammer_pin)
hammer = hammer.cut(hammer_pin) # Hole in hammer

# --- 5. Trigger ---
trig_pivot = (-2, -5)
# Define a hook shape for the trigger
trigger_pts = [
    (trig_pivot[0], trig_pivot[1]),
    (trig_pivot[0] + 5, trig_pivot[1]),
    (trig_pivot[0] + 6, trig_pivot[1] - 5),
    (trig_pivot[0] + 2, trig_pivot[1] - 10),
    (trig_pivot[0] - 2, trig_pivot[1] - 10),
    (trig_pivot[0] - 1, trig_pivot[1] - 4),
]

trigger = (
    cq.Workplane("XY")
    .polyline(trigger_pts)
    .close()
    .extrude(gap - 0.5)
    .edges("|Z").fillet(0.5)
    .translate((0, 0, wall_thick + 0.25))
)

# Trigger Pivot Pin
trig_pin = (
    cq.Workplane("XY")
    .moveTo(trig_pivot[0] + 1, trig_pivot[1] - 2)
    .circle(1.5)
    .extrude(thickness)
)
frame = frame.union(trig_pin)
trigger = trigger.cut(trig_pin)

# --- Final Assembly ---
result = frame.union(hammer).union(trigger)