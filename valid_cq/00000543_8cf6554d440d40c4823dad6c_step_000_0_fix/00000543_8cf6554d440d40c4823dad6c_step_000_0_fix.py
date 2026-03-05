import cadquery as cq
import math

# Parameters
L = 120        # total length of the wave section
W = 20         # total width of the part
H = 10         # base height of the wave section
A = 5          # amplitude of the wave
cycles = 1.5   # number of full sine cycles
n = 100        # number of sampling points for the sine

# Generate the wave profile points in the XZ plane
pts = [(-L/2, 0)]
for i in range(n+1):
    x = -L/2 + (L * i / n)
    z = H + A * math.sin(2 * math.pi * cycles * i / n)
    pts.append((x, z))
pts.append((L/2, 0))

# Build the wave-shaped extruded core
result = (
    cq.Workplane("XZ")
      .polyline(pts)
      .close()
      .extrude(W, both=True)
)

# End-block parameters
tb = 8    # thickness of end blocks
hb = H + 8  # height of end blocks

# Create left and right end blocks and fuse them to the core
left_block = (
    cq.Workplane("XY")
      .box(tb, W, hb)
      .translate((-L/2 - tb/2, 0, hb/2))
)
right_block = (
    cq.Workplane("XY")
      .box(tb, W, hb)
      .translate(( L/2 + tb/2, 0, hb/2))
)
result = result.union(left_block).union(right_block)

# Slot cut parameters for the underside of end blocks
slot_w = W * 0.3
slot_h = hb * 0.4
slot_l = tb * 1.5

# Create and cut slots in left and right blocks
left_slot = (
    cq.Workplane("XY")
      .box(slot_l, slot_w, slot_h)
      .translate((-L/2 - tb/2, 0, slot_h/2))
)
right_slot = left_slot.translate((L + tb, 0, 0))

result = result.cut(left_slot).cut(right_slot)