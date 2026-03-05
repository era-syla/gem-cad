import cadquery as cq

# Parameters
board_length = 80
board_width = 100
board_thickness = 2
corner_hole_dia = 3
corner_hole_offset_x = board_length/2 - 5
corner_hole_offset_y = board_width/2 - 5

# Base board
board = (
    cq.Workplane("XY")
    .rect(board_length, board_width)
    .extrude(board_thickness)
    # Notch on bottom edge
    .faces(">Z")
    .workplane()
    .pushPoints([(-30, -board_width/2 + board_thickness + 5)])
    .rect(10, 20)
    .cutThruAll()
    # Corner holes
    .faces(">Z")
    .workplane()
    .pushPoints([
        ( corner_hole_offset_x,  corner_hole_offset_y),
        (-corner_hole_offset_x,  corner_hole_offset_y),
        ( corner_hole_offset_x, -corner_hole_offset_y),
        (-corner_hole_offset_x, -corner_hole_offset_y),
    ])
    .hole(corner_hole_dia)
)

# Coax connector (simple cylindrical approximation)
coax = (
    cq.Workplane("XY")
    .circle(10)
    .extrude(20)
    .translate((-20, board_width/2 + board_thickness, 0))
)

# Small push-button switch
switch = (
    cq.Workplane("XY")
    .center(20, board_width/2)
    .rect(8, 8)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .circle(3)
    .extrude(4)
)

# Right-angle pin header (6 pins)
pin_header = (
    cq.Workplane("XY")
    .center(board_length/2, 0)
    .rect(8, 6)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .pushPoints([(-2.5 + i*1.25, 0) for i in range(6)])
    .rect(1, 1)
    .extrude(10)
)

# Rectangular socket connector (8-pin)
socket = (
    cq.Workplane("XY")
    .center(board_length/2, board_width/2 - 20)
    .rect(15, 20)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .pushPoints([(-5 + i*3, -5 + j*10) for i in range(2) for j in range(4)])
    .rect(1, 1)
    .extrude(5)
)

# Combine all parts
result = board.union(coax).union(switch).union(pin_header).union(socket)