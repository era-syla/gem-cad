import cadquery as cq

# Parametric Dimensions
L_stem = 150.0        # Length of the main flat stem
W_stem = 40.0         # Width of the main flat stem
T_stem = 10.0         # Thickness of the main flat stem

L_cb = 120.0          # Total length of the crossbar
W_cb = 20.0           # Width of the crossbar
T_cb_end = 10.0       # Thickness of the crossbar at the ends
T_cb_center = 25.0    # Thickness of the crossbar in the center
taper_w = 15.0        # Width of the angled transition section

hole_dia = 8.0        # Diameter of the mounting holes
hole_offset_x = L_cb / 2 - 12.5  # X distance from center to hole

# Build Crossbar profile on XZ plane
# Profile traces the front face, which is then extruded along Y
pts = [
    (L_cb/2, 0),
    (L_cb/2, -T_cb_end),
    (W_stem/2 + taper_w, -T_cb_end),
    (W_stem/2, -T_cb_center),
    (-W_stem/2, -T_cb_center),
    (-(W_stem/2 + taper_w), -T_cb_end),
    (-L_cb/2, -T_cb_end),
    (-L_cb/2, 0)
]

crossbar = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(W_cb)
)

# Build Stem on XY plane
# Set the top face flush with Z=0 and align it to the crossbar
stem = (
    cq.Workplane("XY")
    .workplane(offset=-T_stem/2)
    .center(0, -L_stem/2)
    .box(W_stem, L_stem, T_stem)
)

# Combine the crossbar and the stem
base_solid = crossbar.union(stem)

# Add mounting holes to the crossbar ends
result = (
    cq.Workplane("XY")
    .add(base_solid)
    .pushPoints([
        (hole_offset_x, W_cb/2), 
        (-hole_offset_x, W_cb/2)
    ])
    .hole(hole_dia)
)