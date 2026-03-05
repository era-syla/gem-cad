import cadquery as cq

# Main box dimensions
box_w = 80
box_d = 60
box_h = 20
wall = 3
floor_h = 3
corner_r = 5

# Create the outer shell (box with rounded corners)
outer = (
    cq.Workplane("XY")
    .rect(box_w, box_d)
    .extrude(box_h)
)

# Round the outer vertical edges
outer = outer.edges("|Z").fillet(corner_r)
# Round the bottom edges slightly
outer = outer.edges("<Z").fillet(1.5)
# Round the top outer edges slightly
outer = outer.edges(">Z").fillet(1.0)

# Create the inner cavity
inner_w = box_w - 2 * wall
inner_d = box_d - 2 * wall
inner_h = box_h - floor_h

inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=floor_h)
    .rect(inner_w, inner_d)
    .extrude(inner_h + 1)
)
inner_cut = inner_cut.edges("|Z").fillet(corner_r - wall)

# Subtract inner cavity
result = outer.cut(inner_cut)

# Add mounting holes at corners
hole_r = 2.5
hole_inset = corner_r + 1.5

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        ( box_w/2 - hole_inset,  box_d/2 - hole_inset),
        (-box_w/2 + hole_inset,  box_d/2 - hole_inset),
        ( box_w/2 - hole_inset, -box_d/2 + hole_inset),
        (-box_w/2 + hole_inset, -box_d/2 + hole_inset),
    ])
    .circle(hole_r)
    .cutBlind(-box_h)
)

# Add a small rectangular tab/rib on the inside wall (visible in image, right side)
rib_w = 1.5
rib_l = 12
rib_h = 8

rib = (
    cq.Workplane("XY")
    .workplane(offset=floor_h)
    .center(inner_w/2 - rib_w, 5)
    .rect(rib_w, rib_l)
    .extrude(rib_h)
)

result = result.union(rib)