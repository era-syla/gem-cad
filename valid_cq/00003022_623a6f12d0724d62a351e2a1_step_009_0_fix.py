import cadquery as cq

# Create a shape that looks like a house/arrow pointing left with a C-shaped cutout on the right side
# The overall shape is like a pentagon (arrow/house shape) with a rectangular notch cut from the right side

# Dimensions
width = 80
depth = 60
height = 20
notch_width = 30
notch_depth = 35
notch_height = height  # full height cutout

# Create the base pentagon shape (arrow pointing left / house shape)
# Points for the profile viewed from top
# Starting from bottom-left, going clockwise
pts = [
    (-width/2, -depth/2),      # bottom-left
    (width/2, -depth/2),       # bottom-right
    (width/2, depth/2),        # top-right
    (0, depth/2 + depth/2),    # apex (top point - making it a triangle top)
    (-width/2, depth/2),       # top-left
]

# Actually looking at the image more carefully:
# It's a rectangular base with the front-left corner cut at 45 degrees (making a pentagon)
# with a U/C shaped notch cut from the right side

# Let me redesign:
# Base shape: rectangle with one corner beveled (bottom-left corner cut diagonally)
# Then a rectangular slot cut from the right side (open on the right)

bw = 80  # base width (x)
bd = 60  # base depth (y)
h = 20   # height (z)

# The shape viewed from top:
# Top-left corner is the apex point
# It looks like a right-pointing arrow or chevron with notch

# From the image: the shape has a pointed left side (like a house roof viewed from top)
# with a rectangular C-cutout on the right portion

# Pentagon shape: pointed on left, flat on right
pts = [
    (0, 0),           # left apex point
    (bw, bd*0.3),     # bottom-right
    (bw, bd*0.7),     # top-right  
    # but with notch...
]

# Simpler approach: make rectangle, cut a triangle from left, cut notch from right
result = (
    cq.Workplane("XY")
    .rect(bw, bd)
    .extrude(h)
)

# Cut triangle from left side to make pointed shape
# Triangle cut: remove the left portion to create a point
triangle_pts = [
    (-bw/2, -bd/2),
    (-bw/2, bd/2),
    (0, 0),
]

cut_tri = (
    cq.Workplane("XY")
    .polyline(triangle_pts)
    .close()
    .extrude(h)
)

# Actually let's build the profile directly
# Profile (top view): pointed on left side
profile_pts = [
    (-bw/2, 0),           # left apex
    (0, -bd/2),           # bottom-left-mid
    (bw/2, -bd/2),        # bottom-right
    (bw/2, bd/2),         # top-right
    (0, bd/2),            # top-left-mid
]

base = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(h)
)

# Cut a rectangular notch from the right side (C-shape / U-shape opening to right)
notch_w = bw * 0.4   # notch width in x
notch_d = bd * 0.45  # notch depth in y
notch_x = bw/2 - notch_w/2  # center x of notch
notch_y = 0          # centered in y

notch = (
    cq.Workplane("XY")
    .center(notch_x, notch_y)
    .rect(notch_w + 1, notch_d)
    .extrude(h + 2)
    .translate((0, 0, -1))
)

result = base.cut(notch)

# Add small fillets on vertical edges
result = (
    result
    .edges("|Z")
    .fillet(3)
)