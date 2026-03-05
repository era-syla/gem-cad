import cadquery as cq
import math

# Parameters
thickness = 3.0
mount_hole_r = 3.5
mount_hole_offset_x = 45.0
mount_hole_offset_y = 30.0

# Create the base plate using spline-like shape
# The shape is a 4-pointed star/cross with rounded arms

# Build the outline of the cross shape using a series of points
# The shape has 4 mounting tabs at corners and narrow waist between them

def make_cross_plate():
    # Overall dimensions roughly 110 wide x 75 tall
    w = 55  # half width
    h = 35  # half height
    
    # Tab radius
    tab_r = 10
    
    # Waist narrowing - the cross narrows between the tabs
    waist_x = 18  # half width at center vertical
    waist_y = 12  # half height at center horizontal
    
    # Create the outline as a series of arcs and lines
    # Using a loft or spline approach
    
    # Points for the cross outline (going clockwise from top)
    # The shape is symmetric
    
    # Build with spline through key points
    pts = [
        (0, h + 2),          # top center
        (waist_x, waist_y),  # upper right inner
        (w, 0),              # right center  
        (waist_x, -waist_y), # lower right inner
        (0, -(h + 2)),       # bottom center
        (-waist_x, -waist_y),# lower left inner
        (-w, 0),             # left center
        (-waist_x, waist_y), # upper left inner
    ]
    
    result = (
        cq.Workplane("XY")
        .spline(pts, periodic=True)
        .close()
        .extrude(thickness)
    )
    return result

# Build main body using ellipses/rectangles combined
# Use a different approach: create cross from intersecting rounded rectangles + corner tabs

# Main horizontal bar
h_bar = (cq.Workplane("XY")
         .rect(100, 24)
         .extrude(thickness))

# Main vertical bar  
v_bar = (cq.Workplane("XY")
         .rect(24, 64)
         .extrude(thickness))

# Corner mounting tabs (circles at corners)
tab_positions = [
    (45, 30),
    (-45, 30),
    (45, -30),
    (-45, -30),
]

tabs = cq.Workplane("XY")
for (x, y) in tab_positions:
    tabs = tabs.union(
        cq.Workplane("XY")
        .center(x, y)
        .circle(10)
        .extrude(thickness)
    )

# Combine all parts
body = h_bar.union(v_bar).union(tabs)

# Fillet the overall shape edges on top/bottom faces
# Apply fillets to vertical edges
body = body.edges("|Z").fillet(4.0)

# Cut the two rectangular slots in the center
slot_w = 28
slot_h = 7
slot_gap = 4

slot1 = (cq.Workplane("XY")
         .center(0, (slot_gap/2 + slot_h/2))
         .rect(slot_w, slot_h)
         .extrude(thickness))

slot2 = (cq.Workplane("XY")
         .center(0, -(slot_gap/2 + slot_h/2))
         .rect(slot_w, slot_h)
         .extrude(thickness))

body = body.cut(slot1).cut(slot2)

# Cut mounting holes at each corner tab
for (x, y) in tab_positions:
    hole = (cq.Workplane("XY")
            .center(x, y)
            .circle(mount_hole_r)
            .extrude(thickness))
    body = body.cut(hole)

# Apply small fillets to slot edges
try:
    body = body.edges("|Z").fillet(1.5)
except:
    pass

result = body