import cadquery as cq

# Parameters
L1 = 50       # horizontal arm length in XY
H1 = 60       # vertical arm height in XY
bar = 10      # arm thickness in XY
thickness = 5 # extrusion thickness in Z
hole_dia = 4  # hole diameter

result = (
    cq.Workplane("XY")
    # Define L-shaped profile
    .polyline([
        (0, 0),
        (L1, 0),
        (L1, bar),
        (bar, bar),
        (bar, H1),
        (0, H1)
    ])
    .close()
    # Extrude to 3D
    .extrude(thickness)
    # Fillet all vertical edges (edges parallel to Z axis)
    .edges("|Z").fillet(3)
    # Drill holes on the top face
    .faces(">Z").workplane()
    .pushPoints([
        (L1 - 5,     bar/2),  # end of horizontal arm
        (bar,        bar),    # pivot hole at corner
        (bar/2,      35),     # mid vertical arm
        (bar/2,      H1 - 5)  # top of vertical arm
    ])
    .hole(hole_dia)
    # Engrave text on the bottom face of the horizontal arm
    .faces("<Z").workplane()
    .transformed(offset=(L1/2, bar/2, 0))
    .text("Wesley Bixen", 4, 0.8, cut=True)
)

result