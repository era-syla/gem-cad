import cadquery as cq

# Main dimensions
total_width = 20
total_depth = 12
total_height = 14

# Build the main body - trapezoidal profile (wider at bottom, angled top front)
# The connector has a sloped front face

# Create base profile as a polygon for the side profile
# Bottom width = total_depth, top is angled

body = (
    cq.Workplane("XY")
    .rect(total_width, total_depth)
    .extrude(total_height)
)

# Create the sloped front - cut a wedge from the front top
# The front top slopes back
slope_cut = (
    cq.Workplane("XZ")
    .workplane(offset=-total_depth/2)
    .transformed(offset=cq.Vector(0, 0, 0))
)

# Use vertices to define the slope cut
# Cut from the front top edge going back
front_slope = (
    cq.Workplane("YZ")
    .workplane(offset=-total_width/2)
    .polyline([(total_depth/2, total_height), 
               (total_depth/2, total_height - 3),
               (-total_depth/2 + 3, total_height),
               (total_depth/2, total_height)])
    .close()
    .extrude(total_width)
)

body = body.cut(front_slope)

# Add small side tabs/rails on left and right
tab_w = 1.5
tab_h = 4
tab_d = 2

left_tab = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-total_width/2 - tab_w/2, 0, 1))
    .rect(tab_w, total_depth - 2)
    .extrude(tab_h)
)

right_tab = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(total_width/2 + tab_w/2, 0, 1))
    .rect(tab_w, total_depth - 2)
    .extrude(tab_h)
)

body = body.union(left_tab).union(right_tab)

# Cut the front cavities - two rectangular openings in the front face
cavity_w = 7
cavity_h = 9
cavity_d = 9
cavity_spacing = 10

# Left cavity
left_cavity = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-cavity_spacing/2, -total_depth/2, 1))
    .rect(cavity_w, cavity_d)
    .extrude(cavity_h)
)

# Right cavity  
right_cavity = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(cavity_spacing/2, -total_depth/2, 1))
    .rect(cavity_w, cavity_d)
    .extrude(cavity_h)
)

body = body.cut(left_cavity).cut(right_cavity)

# Add center divider already exists as part of body
# Cut a slot between the two cavities from front
center_slot = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, -total_depth/2, 1))
    .rect(1.5, cavity_d)
    .extrude(cavity_h)
)
body = body.cut(center_slot)

# Drill the two holes from the top for wire insertion
hole_radius = 2.8
hole_depth = 8
hole_y = 1  # slightly toward back from center

left_hole = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-cavity_spacing/2, hole_y, total_height))
    .circle(hole_radius)
    .extrude(-hole_depth)
)

right_hole = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(cavity_spacing/2, hole_y, total_height))
    .circle(hole_radius)
    .extrude(-hole_depth)
)

body = body.cut(left_hole).cut(right_hole)

# Small bottom notches on the front bottom
notch_w = 2
notch_h = 2
notch_d = 1

left_notch = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-cavity_spacing/2, -total_depth/2, 0))
    .rect(notch_w + 2, notch_d * 2)
    .extrude(notch_h)
)

right_notch = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(cavity_spacing/2, -total_depth/2, 0))
    .rect(notch_w + 2, notch_d * 2)
    .extrude(notch_h)
)

body = body.cut(left_notch).cut(right_notch)

result = body