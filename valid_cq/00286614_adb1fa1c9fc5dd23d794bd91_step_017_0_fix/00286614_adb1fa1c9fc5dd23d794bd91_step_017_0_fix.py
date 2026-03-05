import cadquery as cq

# Parameters
L = 100    # total length
W = 20     # total width
T = 5      # plate thickness
hole_d = 6 # hole diameter
boss_d = 6 # boss diameter
boss_h = 15# boss height

# Compute slot parameters
slot_len = L - W      # straight section length of slot2D
slot_rad = W / 2.0    # semicircle radius

result = (
    cq.Workplane("XY")
      .slot2D(slot_len, slot_rad)  # create the rounded-rectangle profile
      .extrude(T)                  # extrude to plate thickness
      # Add boss on left end
      .faces(">Z")
      .workplane()
      .center(-slot_len/2.0, 0)
      .circle(boss_d/2.0)
      .extrude(boss_h)
      # Drill hole on right end
      .faces(">Z")
      .workplane()
      .center(slot_len/2.0, 0)
      .hole(hole_d)
)