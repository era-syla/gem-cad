import cadquery as cq

# Parametric dimensions
L = 120.0        # Overall length
H = 24.0         # Overall height
D = 16.0         # Overall depth (front to back)
T_top = 10.0     # Thickness of the top overhang part
T_back = 6.0     # Thickness of the back vertical wall

tab_w = 10.0     # Width of the back tabs
tab_ext = 5.0    # How far the tabs extend backwards
tab_dist = 60.0  # Distance between the centers of the tabs

hole_spacing = 60.0
hole_dia = 4.5
hole_depth = 6.0
hole_y = (T_back + D) / 2.0  # Center of the front overhang

# Create the main L-shaped base body
# Profile drawn in the YZ plane and extruded along the X axis
pts = [
    (0, 0),                 # Bottom-back
    (0, H),                 # Top-back
    (D, H),                 # Top-front
    (D, H - T_top),         # Bottom-front of the thick top section
    (T_back, H - T_top),    # Inner corner of the overhang
    (T_back, 0)             # Bottom-front of the thin back section
]

base = cq.Workplane("YZ").polyline(pts).close().extrude(L / 2, both=True)

# Create the two tabs extending from the back face
tab_box = cq.Workplane("XY").box(tab_w, tab_ext, T_top)
tab1 = tab_box.translate((-tab_dist / 2, -tab_ext / 2, H - T_top / 2))
tab2 = tab_box.translate((tab_dist / 2, -tab_ext / 2, H - T_top / 2))

# Union the tabs to the base
solid_body = base.union(tab1).union(tab2)

# Create the blind holes to cut into the bottom of the top overhang
holes = (
    cq.Workplane("XY")
    .pushPoints([
        (-hole_spacing / 2, hole_y),
        (hole_spacing / 2, hole_y)
    ])
    .cylinder(hole_depth, hole_dia / 2, centered=(True, True, False))
    .translate((0, 0, H - T_top)) # Move cylinders to start at the overhang's bottom face
)

# Cut the holes from the solid body
result = solid_body.cut(holes)