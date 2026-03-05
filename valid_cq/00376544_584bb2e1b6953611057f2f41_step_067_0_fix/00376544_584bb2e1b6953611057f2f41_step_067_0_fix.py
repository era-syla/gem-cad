import cadquery as cq

# Parameters
L = 40        # length of plate
W = 20        # width of plate
T = 5         # thickness of both plate and flange
H = 20        # height of flange (in Z direction)
hole_dia = 5  # hole diameter
hole_x_off = L/2 - 8
hole_y_off = W/2 - 5
spacing = 60  # spacing between parts in X direction

def make_bracket(flange_dir=0):
    # flange_dir: 0 = flat plate, 1 = flange on +X side, -1 = flange on -X side
    part = cq.Workplane("XY").rect(L, W).extrude(T)
    part = part.faces(">Z").workplane().pushPoints([
        ( hole_x_off,  hole_y_off),
        ( hole_x_off, -hole_y_off)
    ]).hole(hole_dia)
    if flange_dir != 0:
        # choose end face for flange
        side_face = part.faces(">X") if flange_dir > 0 else part.faces("<X")
        part = side_face.workplane().rect(W, H).extrude(flange_dir * T)
    return part

# build the three parts and position them
plate_only   = make_bracket(0).translate((0,      0, 0))
flange_left  = make_bracket(1).translate((spacing, 0, 0))
flange_right = make_bracket(-1).translate((2*spacing, 0, 0))

result = plate_only.union(flange_left).union(flange_right)