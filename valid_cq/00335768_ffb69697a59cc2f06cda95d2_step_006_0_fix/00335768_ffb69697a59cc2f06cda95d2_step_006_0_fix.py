import cadquery as cq

result = (
    cq.Workplane("YZ")
    .rect(40, 20)        # plate size: 40 wide, 20 high
    .extrude(3)          # plate thickness
    .faces(">X")         # select front face of plate
    .workplane()
    .pushPoints([(-10, 0), (10, 0)])  # hole positions in plate
    .hole(5)             # create two 5mm holes through plate
    .faces(">X")         # select front face again for rod
    .workplane()
    .circle(3)           # rod radius 3mm
    .extrude(60)         # rod length 60mm
    .faces(">X")         # select rod front face for disk
    .workplane()
    .circle(10)          # disk radius 10mm
    .extrude(5)          # disk thickness 5mm
    .faces(">X")         # select disk front face
    .workplane()
    .hole(6, 5)          # hole 6mm diameter through the disk thickness
)