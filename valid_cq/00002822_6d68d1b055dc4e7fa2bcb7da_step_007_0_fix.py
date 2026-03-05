import cadquery as cq

# Main bracket body - vertical plate
vertical_plate = (
    cq.Workplane("XY")
    .box(8, 50, 60)
    .translate((0, 0, 30))
)

# Mounting plate at top (horizontal flange)
top_plate = (
    cq.Workplane("XY")
    .box(40, 50, 6)
    .translate((16, 0, 57))
)

# Combine vertical plate and top plate
bracket_main = vertical_plate.union(top_plate)

# Add mounting holes to top plate
bracket_main = (
    bracket_main
    .cut(
        cq.Workplane("XY")
        .circle(4)
        .extrude(10)
        .translate((8, 15, 54))
    )
    .cut(
        cq.Workplane("XY")
        .circle(4)
        .extrude(10)
        .translate((8, -15, 54))
    )
)

# Horizontal arm extending right
h_arm = (
    cq.Workplane("XY")
    .box(45, 20, 14)
    .translate((30, 0, 28))
)

bracket_main = bracket_main.union(h_arm)

# Round end cap on horizontal arm
end_cap = (
    cq.Workplane("YZ")
    .circle(10)
    .extrude(12)
    .translate((52, 0, 28))
)

bracket_main = bracket_main.union(end_cap)

# Hole in end cap
bracket_main = bracket_main.cut(
    cq.Workplane("YZ")
    .circle(5)
    .extrude(14)
    .translate((51, 0, 28))
)

# Central connector block (black square piece)
connector_block = (
    cq.Workplane("XY")
    .box(16, 16, 16)
    .translate((0, 0, 20))
)

# Add holes to connector block face
connector_block = (
    connector_block
    .cut(
        cq.Workplane("YZ")
        .circle(2)
        .extrude(8)
        .translate((-1, 5, 25))
    )
    .cut(
        cq.Workplane("YZ")
        .circle(2)
        .extrude(8)
        .translate((-1, -5, 25))
    )
    .cut(
        cq.Workplane("YZ")
        .circle(2)
        .extrude(8)
        .translate((-1, 5, 15))
    )
    .cut(
        cq.Workplane("YZ")
        .circle(2)
        .extrude(8)
        .translate((-1, -5, 15))
    )
)

bracket_main = bracket_main.union(connector_block)

# Lower tabs/feet extending left
left_tab1 = (
    cq.Workplane("XY")
    .box(20, 5, 6)
    .translate((-14, 8, 6))
)

left_tab2 = (
    cq.Workplane("XY")
    .box(20, 5, 6)
    .translate((-14, -8, 6))
)

bracket_main = bracket_main.union(left_tab1).union(left_tab2)

# Hinge/pin connectors between vertical plate and horizontal arm
hinge1 = (
    cq.Workplane("XZ")
    .circle(3)
    .extrude(12)
    .translate((0, 8, 35))
)

hinge2 = (
    cq.Workplane("XZ")
    .circle(3)
    .extrude(12)
    .translate((0, -8, 35))
)

bracket_main = bracket_main.union(hinge1).union(hinge2)

# Small gusset/rib on vertical plate
gusset = (
    cq.Workplane("XY")
    .box(6, 50, 4)
    .translate((7, 0, 50))
)

bracket_main = bracket_main.union(gusset)

# Clean up with chamfers on top plate edges
result = bracket_main