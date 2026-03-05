import cadquery as cq

# --- Parameters ---
L = 15.5            # Main body length
W = 8.0             # Main body width
H = 16.0            # Main body height
C = 2.0             # Chamfer size for polarity
wall = 1.0          # Wall thickness of cavity
floor = 2.0         # Floor thickness of cavity
pin_dist = 7.2      # Distance between pins
px = pin_dist / 2.0 # X offset for pins

s_h = 5.0           # Bottom shroud height
s_ro = 2.5          # Bottom shroud outer radius
s_ri = 1.75         # Bottom shroud inner radius

pin_h = 12.0        # Pin height
pin_ro = 2.25       # Pin outer radius
pin_ri = 1.7        # Pin inner radius

# --- 1. Main Body ---
body = cq.Workplane("XY").box(L, W, H)
# Apply chamfer on one side to match XT60 shape
body = body.edges("|Z and >X").chamfer(C)

# --- 2. Inner Cavity ---
cavity_L = L - 2*wall
cavity_W = W - 2*wall
cavity_H = H - floor
cavity_C = C - wall

# Calculate offset so the cavity is open at the top
cavity_offset_z = (-H/2 + floor) + cavity_H/2

cavity = (
    cq.Workplane("XY")
    .workplane(offset=cavity_offset_z)
    .box(cavity_L, cavity_W, cavity_H)
)
# Match outer chamfer
cavity = cavity.edges("|Z and >X").chamfer(cavity_C)

# Cut cavity out of the main body
body = body.cut(cavity)

# Apply a small chamfer/fillet to the top edges
body = body.edges(">Z").chamfer(0.2)

# --- 3. Floor Holes (for Solder Cups) ---
floor_holes = (
    cq.Workplane("XY")
    .workplane(offset=-H/2)
    .pushPoints([(-px, 0), (px, 0)])
    .cylinder(floor * 2, s_ri)
)
body = body.cut(floor_holes)

# --- 4. Bottom Shrouds ---
# Left Shroud: Half-cylinder open inwards
shroud_left = (
    cq.Workplane("XY")
    .workplane(offset=-H/2)
    .center(-px, 0)
    .moveTo(0, s_ro)
    .threePointArc((-s_ro, 0), (0, -s_ro))
    .lineTo(0, -s_ri)
    .threePointArc((-s_ri, 0), (0, s_ri))
    .close()
    .extrude(-s_h)
)

# Right Shroud: Full cylinder
shroud_right = (
    cq.Workplane("XY")
    .workplane(offset=-H/2)
    .center(px, 0)
    .circle(s_ro)
    .circle(s_ri)
    .extrude(-s_h)
)

body = body.union(shroud_left).union(shroud_right)

# --- 5. Female Pins ---
def make_pin():
    # Base cylinder
    p = cq.Workplane("XY").cylinder(pin_h, pin_ro)
    
    # Fillet top edge to mimic bullet socket
    p = p.edges(">Z").fillet(0.4)
    
    # Central hole
    p = p.cut(cq.Workplane("XY").cylinder(pin_h + 0.1, pin_ri))
    
    # Cross slits
    slit_w = 0.5
    slit_d = 5.0
    slit_base_z = pin_h/2 - slit_d
    
    # Create slits rotated by 45 degrees
    slits_wp = cq.Workplane("XY").workplane(offset=slit_base_z).transformed(rotate=cq.Vector(0, 0, 45))
    slit1 = slits_wp.rect(pin_ro*3, slit_w).extrude(slit_d + 1.0)
    slit2 = slits_wp.rect(slit_w, pin_ro*3).extrude(slit_d + 1.0)
    
    p = p.cut(slit1).cut(slit2)
    return p

# Position pins in the cavity
pin1 = make_pin().translate((-px, 0, 0))
pin2 = make_pin().translate((px, 0, 0))
body = body.union(pin1).union(pin2)

# --- 6. Side Recess, Ribs, and Text ---
recess_l = 10.0
recess_h = 5.0
recess_d = 0.6
recess_center_z = -1.5

# Cut the rectangular recess
recess = (
    cq.Workplane("XZ")
    .workplane(offset=-W/2)
    .center(0, recess_center_z)
    .box(recess_l, recess_h, recess_d * 2)
)
body = body.cut(recess)

# Add horizontal ribs inside the recess
rib_w = 0.25
rib_d = 0.3
rib_y = -W/2 + recess_d - rib_d/2
rib_spacing = 1.0
rib_pts = [(0, recess_center_z - 1.5 + i * rib_spacing) for i in range(4)]

ribs = (
    cq.Workplane("XZ")
    .workplane(offset=rib_y)
    .pushPoints(rib_pts)
    .box(recess_l, rib_w, rib_d)
)
body = body.union(ribs)

# Add "XT60" text
text_str = "XT60"
text_wp = cq.Workplane("XZ").workplane(offset=-W/2 + recess_d)
# Extrude negatively to bring the text outwards flush with the main body
text_3d = text_wp.center(0, recess_center_z).text(text_str, 3.2, -0.6, halign="center", valign="center")
body = body.union(text_3d)

# Final Output
result = body