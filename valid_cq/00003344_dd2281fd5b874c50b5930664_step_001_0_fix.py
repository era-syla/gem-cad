import cadquery as cq

# Main base plate
length = 80
width = 60
height = 8
corner_radius = 4

# Create the main body
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# Add rounded corners to main body
result = result.edges("|Z").fillet(corner_radius)

# Add a tab/connector section on one side (the front protrusion)
tab_length = 20
tab_width = 40
tab_height = 6

tab = (
    cq.Workplane("XY")
    .center(-length/2 - tab_length/2 + 2, 0)
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

tab = tab.edges("|Z").fillet(3)

result = result.union(tab)

# Create a slot/channel in the tab area
slot_length = 14
slot_width = 8
slot_depth = 4

result = (
    result
    .faces(">Z")
    .workplane()
    .center(-length/2 - tab_length/2 + 4, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Add a small pin/cylinder in the slot area
pin_x = -length/2 - tab_length/2 + 4
pin_y = 0
pin_radius = 2
pin_height = 4

pin = (
    cq.Workplane("XY")
    .center(pin_x, pin_y)
    .circle(pin_radius)
    .extrude(tab_height + pin_height)
)

result = result.union(pin)

# Add screw holes on the main plate
hole_radius = 2
hole_depth = height

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-length/2 + 10, width/2 - 8), (-length/2 + 10, -width/2 + 8)])
    .circle(hole_radius)
    .cutBlind(-hole_depth)
)

# Add a rectangular recess/slot connecting tab to main body
recess_width = slot_width
recess_length = 10
recess_depth = 3

result = (
    result
    .faces(">Z")
    .workplane()
    .center(-length/2 + recess_length/2, 0)
    .rect(recess_length, recess_width)
    .cutBlind(-recess_depth)
)