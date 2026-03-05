import cadquery as cq
import math

# --- Parameters ---
thickness = 3.0
web_thickness = 3.0

# Dimensions for the main web profile (XZ plane)
L_straight = 160.0       # Length of the straight section
H_start = 90.0           # Height at the start (left)
L_angled_x = 180.0       # Horizontal length of the angled tail
H_tail_rise = 65.0       # How much the top edge rises
H_tail_web = 40.0        # Height of the web at the tail tip

# Derived coordinates
x_kink = L_straight
y_kink = H_start
x_end = L_straight + L_angled_x
y_end_top = H_start + H_tail_rise
y_end_bot = y_end_top - H_tail_web

# Flange dimensions
flange_width = 35.0

# --- Geometry Construction ---

# 1. Main Web
# Created in XZ plane, extruded along +Y
web_pts = [
    (0, 0),
    (x_kink, 0),
    (x_end, y_end_bot),
    (x_end, y_end_top),
    (x_kink, y_kink),
    (0, H_start)
]

web = (
    cq.Workplane("XZ")
    .polyline(web_pts)
    .close()
    .extrude(web_thickness)
)

# 2. Top Flange (Straight Section)
# Attached to the top edge of straight section, extending in -Y (Back)
# Plane Normal = X (1,0,0), Origin = (0,0,H_start)
top_flange_straight = (
    cq.Workplane(cq.Plane(origin=(0, 0, H_start), xDir=(0, 1, 0), normal=(1, 0, 0)))
    .center(-flange_width/2, thickness/2) # Align so it starts at Y=0 and goes -Y, sits on top of edge
    .rect(flange_width, thickness)
    .extrude(L_straight)
)

# 3. Top Flange (Angled Section)
# Attached to the angled top edge.
# Calculate vector and length of the angled edge
dx = x_end - x_kink
dz = y_end_top - y_kink
edge_length = math.sqrt(dx**2 + dz**2)

# Create a workplane perpendicular to the angled edge at the kink
# Origin at Kink. Normal aligned with edge vector. X-dir aligned with global Y.
# Note: xDir=(0,1,0) maps sketch X to global Y. sketch Y becomes 'up' relative to edge.
plane_angled = cq.Plane(origin=(x_kink, 0, y_kink), xDir=(0, 1, 0), normal=(dx, 0, dz))

top_flange_angled = (
    cq.Workplane(plane_angled)
    .center(-flange_width/2, thickness/2)
    .rect(flange_width, thickness)
    .extrude(edge_length)
)

# 4. Bottom Flange
# Attached to bottom straight edge, extending in +Y (Front)
# Positioned below Z=0
bottom_flange = (
    cq.Workplane("XY")
    .workplane(offset=-thickness) # Start at Z=-3
    .moveTo(L_straight/2, web_thickness + flange_width/2) # Center Y: starts at 3, width 35
    .rect(L_straight, flange_width)
    .extrude(thickness)
)

# 5. Union Main Body
body = web.union(top_flange_straight).union(top_flange_angled).union(bottom_flange)

# --- Cuts (Holes & Slots) ---

# Calculate positions for holes on the angled tail (mid-line approximation)
slope = (y_end_top - H_tail_web/2 - (H_start/2)) / L_angled_x
y_mid_start = H_start/2
h4_x = x_kink + 60
h4_y = y_mid_start + slope * 60
h5_x = x_kink + 130
h5_y = y_mid_start + slope * 130

# Cutter sketch on the front face of the web
cutter = (
    cq.Workplane("XZ")
    .workplane(offset=web_thickness) # Front face
    
    # Large Slot
    .moveTo(115, 45)
    .slot2D(55, 22, angle=90)
    
    # Holes around slot
    .moveTo(80, 25).circle(3.2)
    .moveTo(80, 65).circle(3.2)
    .moveTo(150, 45).circle(3.2)
    
    # Holes on angled tail
    .moveTo(h4_x, h4_y).circle(3.2)
    .moveTo(h5_x, h5_y).circle(3.2)
)

# Apply Cut
result = body.cut(cutter.extrude(-20)) # Cut through sufficient depth

# Optional: Fillet the internal kink corner of the web profile for better stress flow
# Selecting edges near (x_kink, y_kink) and (x_kink, 0)
# This is aesthetic/realistic but not strictly required by prompt geometry.