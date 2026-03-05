import cadquery as cq

# Parameters
D_main = 20.0
H_main = 40.0

D_cap = 15.0
H_cap = 5.0

D_button = 6.0
H_button = 1.0

D_hole = 1.5
H_hole = 1.0

# Create the 3D model
result = (
    cq.Workplane("XY")
    .cylinder(H_main, D_main / 2.0)
    .faces(">Z")
    .workplane()
    .cylinder(H_cap, D_cap / 2.0)
    .faces(">Z")
    .workplane()
    .cylinder(H_button, D_button / 2.0)
    .faces(">Z")
    .workplane()
    .hole(D_hole, depth=H_hole)
)