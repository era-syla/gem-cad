import cadquery as cq

# Parameters for the geometry
base_r = 15.0
base_h = 15.0
shaft_r = 5.0
shaft_h = 50.0
knob_r = 14.0
knob_h = 20.0
hole_r = 4.0
num_teeth = 12
tooth_r = 3.0

# Build the 3D model
result = (
    cq.Workplane("XY")
    # Create the bottom cylindrical base
    .circle(base_r)
    .extrude(base_h)
    
    # Create the middle shaft
    .faces(">Z")
    .workplane()
    .circle(shaft_r)
    .extrude(shaft_h)
    
    # Create the top knob base
    .faces(">Z")
    .workplane()
    .circle(knob_r)
    .extrude(knob_h)
    
    # Cut the flutes/teeth into the top knob
    .faces(">Z")
    .workplane()
    .polarArray(knob_r, 0, 360, num_teeth)
    .circle(tooth_r)
    .cutBlind(-knob_h)
    
    # Cut the central through-hole
    .faces(">Z")
    .workplane()
    .circle(hole_r)
    .cutThruAll()
)