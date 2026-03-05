import cadquery as cq

# Main PCB board
pcb = (
    cq.Workplane("XY")
    .box(68, 53, 2)
)

# Main enclosure/housing
housing = (
    cq.Workplane("XY")
    .box(68, 53, 35)
    .translate((0, 0, 17))
)

# Combine PCB and housing as base
result = pcb.union(housing)

# Left connector rail (tall vertical connector strip)
left_rail = (
    cq.Workplane("XY")
    .box(6, 50, 40)
    .translate((-37, 0, 20))
)

# Right connector rail
right_rail = (
    cq.Workplane("XY")
    .box(6, 50, 40)
    .translate((37, 0, 20))
)

result = result.union(left_rail).union(right_rail)

# USB connector on top right
usb_connector = (
    cq.Workplane("XY")
    .box(12, 10, 11)
    .translate((18, -21, 39))
)

result = result.union(usb_connector)

# Top left connector block
top_left_block = (
    cq.Workplane("XY")
    .box(10, 8, 12)
    .translate((-24, -21, 39))
)

result = result.union(top_left_block)

# Bottom connector strip (center-left area)
bottom_connector = (
    cq.Workplane("XY")
    .box(14, 6, 20)
    .translate((-10, 20, 15))
)

result = result.union(bottom_connector)

# Small components on top surface - IC chip
ic_chip = (
    cq.Workplane("XY")
    .box(10, 10, 3)
    .translate((-5, -5, 36))
)

result = result.union(ic_chip)

# Capacitor left side
cap1 = (
    cq.Workplane("XY")
    .cylinder(6, 3.5)
    .translate((-20, 5, 37))
)

result = result.union(cap1)

# Small connector pins bottom center
pins = (
    cq.Workplane("XY")
    .box(8, 5, 8)
    .translate((5, 22, 12))
)

result = result.union(pins)

# Left side mounting bracket
left_bracket = (
    cq.Workplane("XY")
    .box(4, 55, 45)
    .translate((-42, 0, 20))
)

result = result.union(left_bracket)

# Right side mounting bracket  
right_bracket = (
    cq.Workplane("XY")
    .box(4, 55, 45)
    .translate((42, 0, 20))
)

result = result.union(right_bracket)

# Cutout in left bracket
left_cutout = (
    cq.Workplane("XY")
    .box(6, 40, 30)
    .translate((-42, 0, 22))
)

result = result.cut(left_cutout)

# Cutout in right bracket
right_cutout = (
    cq.Workplane("XY")
    .box(6, 40, 30)
    .translate((42, 0, 22))
)

result = result.cut(right_cutout)

# Re-add bracket edges
left_edge = (
    cq.Workplane("XY")
    .box(4, 55, 45)
    .translate((-42, 0, 20))
    .shell(-1.5)
)

# Additional small components
small_comp = (
    cq.Workplane("XY")
    .box(6, 4, 4)
    .translate((10, -18, 36))
)

result = result.union(small_comp)

# Header pins on right side of board
header_right = (
    cq.Workplane("XY")
    .box(3, 45, 8)
    .translate((33, 0, 38))
)

result = result.union(header_right)

# Header pins on left side of board
header_left = (
    cq.Workplane("XY")
    .box(3, 45, 8)
    .translate((-33, 0, 38))
)

result = result.union(header_left)