import cadquery as cq

# -- Parametric Dimensions --
# Main body dimensions
thickness = 5.0
outer_radius = 20.0
hole_radius = 10.0

# Vertical Tab dimensions (Top)
# The tab is defined to be tangent to the left edge of the circle 
# and slightly crossing the vertical center line.
v_tab_top_y = 40.0              # Height from center to top edge
v_tab_left_x = -outer_radius    # Aligned with left edge of circle
v_tab_right_x = 5.0             # Position of the right edge
v_tab_width = v_tab_right_x - v_tab_left_x
v_tab_height = v_tab_top_y      # Rectangle height (starts from y=0)
v_tab_center_x = (v_tab_left_x + v_tab_right_x) / 2.0
v_tab_center_y = v_tab_height / 2.0

# Horizontal Tab dimensions (Right)
h_tab_right_x = 40.0            # Length from center to tip
h_tab_width = 12.0              # Width of the tab (dimension in Y)
h_tab_length = h_tab_right_x    # Rectangle length (starts from x=0)
h_tab_center_x = h_tab_length / 2.0
h_tab_center_y = 0.0

# -- Model Construction --

# 1. Base Disk (The washer body)
base = cq.Workplane("XY").circle(outer_radius).extrude(thickness)

# 2. Vertical Tab Geometry
# Created as a separate solid to be unioned.
# Positioned to overlap with the base circle.
v_tab = (
    cq.Workplane("XY")
    .center(v_tab_center_x, v_tab_center_y)
    .rect(v_tab_width, v_tab_height)
    .extrude(thickness)
)

# 3. Horizontal Tab Geometry
# Created as a separate solid to be unioned.
h_tab = (
    cq.Workplane("XY")
    .center(h_tab_center_x, h_tab_center_y)
    .rect(h_tab_length, h_tab_width)
    .extrude(thickness)
)

# 4. Final Boolean Operations
# Union the tabs to the base, then cut the central hole.
result = (
    base
    .union(v_tab)
    .union(h_tab)
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutThruAll()
)