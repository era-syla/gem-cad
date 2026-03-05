import cadquery as cq
import math

# Parameters for the wavy ring segment
outer_r = 30
inner_r = 25
thickness = 5
wave_amplitude = 2
wave_periods = 5
num_points = 200

# Build the wavy half-ring
pts_inner = []
pts_outer = []
for i in range(num_points + 1):
    t = math.pi * i / num_points - math.pi/2
    r_i = inner_r + wave_amplitude * math.sin(wave_periods * t)
    x_i = r_i * math.cos(t)
    y_i = r_i * math.sin(t)
    pts_inner.append((x_i, y_i))
    r_o = outer_r
    x_o = r_o * math.cos(t)
    y_o = r_o * math.sin(t)
    pts_outer.append((x_o, y_o))

ring_wire = (
    cq.Workplane("XY")
      .polyline(pts_outer)
      .lineTo(*pts_inner[-1])
      .polyline(list(reversed(pts_inner)))
      .close()
)
part1 = ring_wire.extrude(thickness)

# Parameters for the knob
base_r = 20
base_h = 10
mid_r = 15
mid_h = 5
lobe_r = 7
lobe_h = 3
slot_depth = 3
slot_w = 5
n_tabs = 8
tab_w = 3
tab_h = base_h + mid_h + lobe_h
tab_thickness = 1.5
tab_r = base_r + 2

# Build the knob: base cylinder and mid cylinder
knob = (
    cq.Workplane("XY")
      .circle(base_r)
      .extrude(base_h)
      .faces(">Z")
      .circle(mid_r)
      .extrude(mid_h)
)

# Add three lobes on top
for i in range(3):
    ang = 360/3 * i
    cx = mid_r * math.cos(math.radians(ang))
    cy = mid_r * math.sin(math.radians(ang))
    lobe = (
        cq.Workplane("XY")
          .transformed(offset=(cx, cy, base_h + mid_h))
          .circle(lobe_r)
          .extrude(lobe_h)
    )
    knob = knob.union(lobe)

# Cut a cross slot
slot1 = (
    cq.Workplane("XY")
      .transformed(offset=(0, 0, base_h + mid_h - 1))
      .rect(base_r*1.8, slot_w)
      .extrude(slot_depth)
)
slot2 = (
    cq.Workplane("XY")
      .transformed(offset=(0, 0, base_h + mid_h - 1))
      .rect(slot_w, base_r*1.8)
      .extrude(slot_depth)
)
knob = knob.cut(slot1).cut(slot2)

# Add small tabs around the rim
for i in range(n_tabs):
    ang = 360/n_tabs * i
    tab = (
        cq.Workplane("XY")
          .transformed(offset=(tab_r, 0, tab_h/2), rotate=(0, 0, ang))
          .rect(tab_w, tab_thickness)
          .extrude(tab_h)
    )
    knob = knob.union(tab)

# Position knob next to the ring
knob = knob.translate((outer_r*3, 0, 0))

result = part1.union(knob)