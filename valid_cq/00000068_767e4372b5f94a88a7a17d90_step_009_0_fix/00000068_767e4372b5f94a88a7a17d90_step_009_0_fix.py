import cadquery as cq

# I-bracket / H-bracket plate with mounting holes
# Overall dimensions estimated from image

total_width = 80      # total length in X
bar_height = 12       # width of the horizontal connecting bar in Y
tab_width = 20        # width of each end tab in X
tab_height = 30       # total height of end tabs in Y
thickness = 5         # plate thickness in Z
hole_diameter = 6     # mounting hole diameter
corner_radius = 4     # corner rounding radius

# The shape looks like an I-beam / H shape viewed from top:
# Two wide end tabs connected by a narrow center bar

# Build the profile as a 2D shape then extrude

# Center bar: narrow strip connecting the two end tabs
# End tabs: wider rectangles at each end

# Coordinates for the I/H shape outline
# Let's place center at origin
# Total width = 80, tab_width = 20, bar connects them

half_w = total_width / 2       # 40
half_bar = bar_height / 2      # 6
half_tab = tab_height / 2      # 15
tab_x_inner = half_w - tab_width  # 20 (inner edge of tab)

# Build using 2D wire with lines
pts = [
    (-half_w, -half_tab),
    (-half_w, half_tab),
    (-tab_x_inner, half_tab),
    (-tab_x_inner, half_bar),
    (tab_x_inner, half_bar),
    (tab_x_inner, half_tab),
    (half_w, half_tab),
    (half_w, -half_tab),
    (tab_x_inner, -half_tab),
    (tab_x_inner, -half_bar),
    (-tab_x_inner, -half_bar),
    (-tab_x_inner, -half_tab),
]

# Create the base shape
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Add corner fillets on the outer edges (select vertical edges)
result = result.edges("|Z").fillet(corner_radius)

# Add mounting holes - 4 holes, one in each corner of the end tabs
hole_inset = 8  # distance from edge to hole center
hole_x = half_w - hole_inset
hole_y = half_tab - hole_inset

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_x, hole_y),
        (-hole_x, -hole_y),
        (hole_x, hole_y),
        (hole_x, -hole_y),
    ])
    .circle(hole_diameter / 2)
    .cutThruAll()
)