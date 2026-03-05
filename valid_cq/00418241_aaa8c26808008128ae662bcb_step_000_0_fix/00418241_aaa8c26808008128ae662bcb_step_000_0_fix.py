import cadquery as cq

# Parameters
th = 3            # top plate thickness
base_h = 5        # base block height
vert_h = 25       # vertical plate height above top plate
top_len = 60      # length of top plate
depth = 10        # extrusion depth (Y direction)
base_left_ext = 15   # base extension under top plate to the left of vertical
base_right_ext = 5   # base extension under top plate to the right of vertical
fillet_r = 1      # fillet radius
arc_r = base_left_ext/2

# Top plate
top = (
    cq.Workplane("XY")
    .box(top_len, depth, th)
    .translate((top_len/2, 0, base_h + th/2))
)

# Vertical plate (on the right end of the top plate)
vert = (
    cq.Workplane("XY")
    .box(th, depth, vert_h)
    .translate((top_len - th/2, 0, base_h + th + vert_h/2))
)

# Base block under the joint area
base_min_x = top_len - base_left_ext
base_max_x = top_len + base_right_ext
base_w = base_max_x - base_min_x
base = (
    cq.Workplane("XY")
    .box(base_w, depth, base_h)
    .translate(( (base_min_x + base_max_x)/2, 0, base_h/2 ))
)

# Arch cut under the top plate (semicircular cut through its underside)
arc = (
    cq.Workplane("XZ")
    .center((base_min_x + base_max_x)/2, base_h)
    .circle(arc_r)
    .extrude(depth)
    .translate((0, -depth/2, 0))
)

# Combine and apply fillets
result = (
    top.union(vert)
       .union(base)
       .cut(arc)
       .edges().fillet(fillet_r)
)