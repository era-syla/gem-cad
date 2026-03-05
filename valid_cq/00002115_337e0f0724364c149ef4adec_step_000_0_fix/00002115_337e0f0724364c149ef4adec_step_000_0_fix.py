import cadquery as cq

# Parameters
L = 150.0      # length of main bar
W = 10.0       # width (and thickness) of bar and feet
H = 10.0       # height of bar and feet
foot_len = 40.0
foot_thick = W
post_height = 40.0
post_width = 10.0
post_thick = 2.0
pin_dia = 2.0
pin_height = 2.0
pin_positions = [-30.0, 0.0, 30.0]

# Main horizontal bar
result = cq.Workplane("XY").box(L, W, H).translate((0, 0, H/2))

# Feet at both ends
left_foot = cq.Workplane("XY").box(foot_thick, foot_len, H).translate(
    (-L/2 - foot_thick/2, 0, H/2)
)
right_foot = cq.Workplane("XY").box(foot_thick, foot_len, H).translate(
    ( L/2 + foot_thick/2, 0, H/2)
)
result = result.union(left_foot).union(right_foot)

# Vertical posts
for x in (-L/4, L/4):
    post = cq.Workplane("XY").box(post_width, post_thick, post_height).translate(
        (x, 0, H + post_height/2)
    )
    result = result.union(post)

# Small pins on top of bar
for x in pin_positions:
    pin = cq.Workplane("XY").cylinder(pin_height, pin_dia/2).translate(
        (x, 0, H + pin_height/2)
    )
    result = result.union(pin)