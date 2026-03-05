import cadquery as cq

# -- Parameters --
# Main dimensions
length_straight = 60.0    # Length of the rectangular section
length_tip = 30.0         # Length of the triangular front section
width_overall = 80.0      # Total width of the part
height_rail = 12.0        # Height of the main frame (rails)
width_rail = 10.0         # Width of the side and center rails
thickness_web = 4.0       # Thickness of the connecting plates

# Pins
pin_diameter = 6.0
pin_length = 10.0

# -- Calculations --
# Y-coordinates
y_back = 0.0
y_front_straight = length_straight
y_tip = length_straight + length_tip

# X-coordinates
x_center = 0.0
x_side_left_outer = -width_overall / 2
x_side_left_inner = x_side_left_outer + width_rail
x_side_right_outer = width_overall / 2
x_side_right_inner = x_side_right_outer - width_rail
x_center_left = -width_rail / 2
x_center_right = width_rail / 2

# Intersection Calculation for the V-shape
# The outer diagonal line goes from (x_side_left_outer, y_front_straight) to (0, y_tip)
# We need to find where this line intersects the side of the center rail (x = x_center_left)
# Line equation: y - y1 = m * (x - x1)
dy = y_tip - y_front_straight
dx = 0 - x_side_left_outer
slope = dy / dx
y_intersect_outer = y_tip + slope * (x_center_left - 0)

# Inner intersection point for the diagonal strut
# We approximate the inner Y on the center rail to maintain visual thickness
y_intersect_inner = y_intersect_outer - (width_rail / slope) * 0.8 # Empirical adjustment for strut thickness

# -- Modeling --

# 1. Main Straight Rails
left_rail = (cq.Workplane("XY")
             .center((x_side_left_outer + x_side_left_inner) / 2, length_straight / 2)
             .rect(width_rail, length_straight)
             .extrude(height_rail))

right_rail = (cq.Workplane("XY")
              .center((x_side_right_outer + x_side_right_inner) / 2, length_straight / 2)
              .rect(width_rail, length_straight)
              .extrude(height_rail))

# 2. Center Rail (with pointed tip)
# Defined as a polygon to handle the tapered front
pts_center = [
    (x_center_left, 0),
    (x_center_right, 0),
    (x_center_right, y_intersect_outer),
    (0, y_tip),
    (x_center_left, y_intersect_outer)
]
center_rail = (cq.Workplane("XY")
               .polyline(pts_center)
               .close()
               .extrude(height_rail))

# 3. Diagonal Struts
# Left Diagonal
pts_diag_left = [
    (x_side_left_outer, y_front_straight),
    (x_center_left, y_intersect_outer),
    (x_center_left, y_intersect_inner),
    (x_side_left_inner, y_front_straight)
]
diag_left = (cq.Workplane("XY")
             .polyline(pts_diag_left)
             .close()
             .extrude(height_rail))

# Right Diagonal (Mirror of left)
diag_right = diag_left.mirror("YZ")

# 4. Webs (Thinner plates between rails)
# Left Web
web_left = (cq.Workplane("XY")
            .center((x_side_left_inner + x_center_left) / 2, length_straight / 2)
            .rect(x_center_left - x_side_left_inner, length_straight)
            .extrude(thickness_web))

# Right Web
web_right = (cq.Workplane("XY")
             .center((x_side_right_inner + x_center_right) / 2, length_straight / 2)
             .rect(x_side_right_inner - x_center_right, length_straight)
             .extrude(thickness_web))

# 5. Pins
# Located on the back face (XZ plane), protruding backwards (-Y)
pins = (cq.Workplane("XZ")
        .workplane(offset=-y_back) # Ensure we are on the back face
        .pushPoints([
            ((x_side_left_outer + x_side_left_inner) / 2, height_rail / 2),
            (0, height_rail / 2),
            ((x_side_right_outer + x_side_right_inner) / 2, height_rail / 2)
        ])
        .circle(pin_diameter / 2)
        .extrude(-pin_length))

# -- Assembly --
result = (left_rail
          .union(right_rail)
          .union(center_rail)
          .union(diag_left)
          .union(diag_right)
          .union(web_left)
          .union(web_right)
          .union(pins))