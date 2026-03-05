import cadquery as cq

# --- Parameter Definitions ---
# Base Plate Dimensions
base_length = 130.0
base_width = 80.0
base_thickness = 5.0
corner_fillet = 10.0

# Boss (Cylinder) Dimensions
diam_large = 55.0
diam_medium = 32.0
diam_small = 20.0
boss_height = 2.0      # Height protruding from the base
hole_diameter = 4.0    # Center hole diameter
boss_spacing = 3.0     # Gap between adjacent boss edges

# Tab (Stop Block) Dimensions
tab_thickness = 5.0
tab_width = 18.0
tab_height = 15.0

# Pin Dimensions
pin_diameter = 4.0
pin_length = 50.0
pin_offset = 25.0      # Distance from base edge

# --- Geometry Construction ---

# 1. Create the Base Plate
# Centered at origin
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_thickness)
    .edges("|Z")
    .fillet(corner_fillet)
)

# 2. Calculate Boss Positions (Small, Medium, Large)
# Radii
r_small = diam_small / 2.0
r_medium = diam_medium / 2.0
r_large = diam_large / 2.0

# Distances between centers
dist_sm_md = r_small + boss_spacing + r_medium
dist_md_lg = r_medium + boss_spacing + r_large

# Position calculation: Place Medium boss slightly left of center
x_medium = -10.0
x_small = x_medium - dist_sm_md
x_large = x_medium + dist_md_lg

boss_data = [
    (x_small, diam_small),
    (x_medium, diam_medium),
    (x_large, diam_large)
]

# 3. Add Bosses to Base
current_geo = base
for x_pos, diam in boss_data:
    boss = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness/2.0)
        .center(x_pos, 0)
        .circle(diam/2.0)
        .extrude(boss_height)
    )
    current_geo = current_geo.union(boss)

# 4. Add Rectangular Tabs
# Left Tab: Near the small boss, front side (negative Y)
left_tab_x = x_small
left_tab_y = -(base_width / 2.0) + (tab_width / 2.0) + 2.0 

left_tab = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2.0)
    .center(left_tab_x, left_tab_y)
    .box(tab_thickness, tab_width, tab_height, centered=(True, True, False))
)
current_geo = current_geo.union(left_tab)

# Right Tab: Near the large boss, back side (positive Y)
right_tab_x = (base_length / 2.0) - (tab_thickness / 2.0) - 5.0
right_tab_y = (base_width / 2.0) - (tab_width / 2.0) - 2.0

right_tab = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2.0)
    .center(right_tab_x, right_tab_y)
    .box(tab_thickness, tab_width, tab_height, centered=(True, True, False))
)
current_geo = current_geo.union(right_tab)

# 5. Cut Holes through Bosses and Base
hole_centers = [(x, 0) for x, d in boss_data]

current_geo = (
    current_geo.faces(">Z").workplane()
    .pushPoints(hole_centers)
    .circle(hole_diameter/2.0)
    .cutThruAll()
)

# 6. Create the Separate Pin
pin_x_pos = -(base_length / 2.0) - pin_offset
pin = (
    cq.Workplane("XY")
    .center(pin_x_pos, 0)
    .circle(pin_diameter/2.0)
    .extrude(pin_length)
)

# 7. Final Result
result = current_geo.union(pin)