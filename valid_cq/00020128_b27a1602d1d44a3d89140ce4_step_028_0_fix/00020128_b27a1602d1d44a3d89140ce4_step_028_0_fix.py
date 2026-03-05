import cadquery as cq
import math

# Parameters
outer_dia = 40.0
outer_r = outer_dia/2
wall_t = 2.0
body_h = 100.0
base_th = 8.0
shelf_z = 50.0
shelf_th = 4.0
opening_w = 15.0
tab_w = 8.0
tab_d = 4.0
tab_h = 6.0
num_tabs = 2
base_r_extra = 6.0
slot_w = 5.0
slot_d = 3.0
slot_h = 4.0
num_slots = 4

# Main shell (hollow cylinder)
outer = cq.Workplane("XY").cylinder(body_h+base_th, outer_r)
inner = cq.Workplane("XY").cylinder(body_h+base_th, outer_r-wall_t)
shell = outer.cut(inner)

# Side opening (rectangular slot through wall)
cut1 = (
    cq.Workplane("YZ")
      .transformed(offset=(outer_r-wall_t/2, 0, base_th))
      .rect(body_h, opening_w)
      .extrude(2*outer_r)
)
shell = shell.cut(cut1)

# Internal shelf
shelf = (
    cq.Workplane("XY")
      .workplane(offset=shelf_z)
      .cylinder(shelf_th, outer_r-wall_t)
)
result = shell.union(shelf)

# Top tabs
tabs = None
for i in range(num_tabs):
    angle = i * 360.0 / num_tabs
    x = (outer_r + tab_d/2) * math.cos(math.radians(angle))
    y = (outer_r + tab_d/2) * math.sin(math.radians(angle))
    t = (
        cq.Workplane("XY")
          .box(tab_d, tab_w, tab_h)
          .translate((x, y, body_h+base_th+tab_h/2))
    )
    tabs = t if tabs is None else tabs.union(t)
result = result.union(tabs)

# Base cylinder
base_r = outer_r + base_r_extra
base = cq.Workplane("XY").cylinder(base_th, base_r)

# Base slots
slots = None
for i in range(num_slots):
    angle = i * 360.0 / num_slots
    x = (base_r - slot_w/2) * math.cos(math.radians(angle))
    y = (base_r - slot_w/2) * math.sin(math.radians(angle))
    s = (
        cq.Workplane("XY")
          .box(slot_d, slot_w, slot_h)
          .translate((x, y, slot_h/2))
    )
    slots = s if slots is None else slots.union(s)
base = base.cut(slots)

# Combine base with main body
result = result.union(base)