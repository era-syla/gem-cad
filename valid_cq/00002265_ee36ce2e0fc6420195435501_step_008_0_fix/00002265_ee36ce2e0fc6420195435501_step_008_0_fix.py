import cadquery as cq

# Parameters
OD1 = 50    # Outer diameter of flange
H1 = 8     # Height of flange
OD2 = 40    # Outer diameter of tube
H2 = 16    # Height of tube
t = 3      # Wall thickness

ID1 = OD1 - 2 * t  # Inner diameter in flange region
ID2 = OD2 - 2 * t  # Inner diameter in tube region

result = (
    cq.Workplane("XY")
    .circle(OD2 / 2).extrude(H2)
    .circle(OD1 / 2).extrude(H1)
    .faces(">Z").workplane()
    .circle(ID1 / 2).cutBlind(-H1)
    .workplane(offset=-H1)
    .circle(ID2 / 2).cutBlind(-H2)
)