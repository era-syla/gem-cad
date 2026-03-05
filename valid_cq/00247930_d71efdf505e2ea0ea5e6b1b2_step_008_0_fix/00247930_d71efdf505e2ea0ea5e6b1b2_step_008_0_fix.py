import cadquery as cq

# Parameters
W = 100.0    # total width in X
H = 80.0     # total height in Z
T = 5.0      # thickness in Y
slot_w = 20.0
slot_h = 60.0

# Offsets to position the slot flush to left and bottom
x_off = -W/2 + slot_w/2
z_off = -H/2 + slot_h/2

result = (
    cq.Workplane("XZ")
      .box(W, T, H)
      .faces(">Y")
      .workplane()
      .transformed(offset=(x_off, 0, z_off))
      .rect(slot_w, slot_h)
      .cutThruAll()
)