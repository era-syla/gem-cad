import cadquery as cq

# Main body dimensions
body_w = 40
body_h = 35
body_d = 12

# Create the main rectangular body
body = (
    cq.Workplane("XY")
    .rect(body_w, body_h)
    .extrude(body_d)
)

# Add chamfer/taper on top-right corner (the angled top)
# The body has a diagonal cut on the top-right
# Cut a triangular prism from the top-right
cutter = (
    cq.Workplane("XY")
    .polyline([
        (0, body_h/2),
        (body_w/2, body_h/2),
        (body_w/2, -body_h/2 + 10),
        (0, body_h/2)
    ])
    .close()
    .extrude(body_d + 2)
    .translate([-body_w/2, -body_h/2, -1])
)

# Actually let's build a cleaner version
# Looking at the image: rectangular plate with diagonal top-right edge,
# rectangular cutout in middle, cylinder on right side at bottom, cylinder on top-right

# Main plate with angled top
plate_pts = [
    (-body_w/2, -body_h/2),
    (body_w/2, -body_h/2),
    (body_w/2, 0),          # angled cut starts here
    (0, body_h/2),           # angled cut ends here
    (-body_w/2, body_h/2),
]

main_plate = (
    cq.Workplane("XY")
    .polyline(plate_pts)
    .close()
    .extrude(body_d)
)

# Rectangular cutout through the plate
cutout_w = 14
cutout_h = 18
cutout = (
    cq.Workplane("XY")
    .center(-3, -2)
    .rect(cutout_w, cutout_h)
    .extrude(body_d)
)

main_plate = main_plate.cut(cutout)

# Bottom-right cylinder (hinge pin area) - horizontal cylinder on right side
cyl_r = 7
cyl_len = 18

right_cyl = (
    cq.Workplane("YZ")
    .center(-body_h/2 + 8, body_d/2)
    .circle(cyl_r)
    .extrude(cyl_len)
    .translate([body_w/2 - 2, 0, 0])
)

# Top cylinder - vertical cylinder on top right
top_cyl_r = 8
top_cyl_h = 14

top_cyl = (
    cq.Workplane("XY")
    .center(body_w/2 - 5, 2)
    .circle(top_cyl_r)
    .extrude(top_cyl_h)
    .translate([0, 0, body_d])
)

# Small collar/flange under top cylinder
collar = (
    cq.Workplane("XY")
    .center(body_w/2 - 5, 2)
    .circle(top_cyl_r + 2)
    .extrude(3)
    .translate([0, 0, body_d])
)

# Inner cylinder inside the cutout (the post visible through cutout)
inner_post = (
    cq.Workplane("XY")
    .center(-3, -2)
    .circle(4)
    .extrude(body_d)
)

# Bottom right small cylinder/knob
bot_knob = (
    cq.Workplane("YZ")
    .center(-body_h/2 + 5, body_d/2)
    .circle(5)
    .extrude(8)
    .translate([body_w/2 + 8, 0, 0])
)

# Combine all parts
result = (
    main_plate
    .union(right_cyl)
    .union(top_cyl)
    .union(collar)
    .union(inner_post)
    .union(bot_knob)
)

# Add fillets to main plate edges - select only vertical edges
try:
    result = result.edges("|Z").fillet(1.5)
except:
    pass