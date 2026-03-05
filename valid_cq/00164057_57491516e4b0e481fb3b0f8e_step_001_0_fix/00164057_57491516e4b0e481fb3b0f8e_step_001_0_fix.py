import cadquery as cq

# Parameters
housing_diam = 20.0
plug_diam    = 18.0
housing_len  = 50.0
plug_len     = 40.0
plug_insert  = 10.0
head_diam    = 40.0
head_thick   = 3.0
pin_diam     = 2.0
pin_len      = 5.0
pin_count    = 6
pin_offset   = 5.0
pin_spacing  = 6.0  # spacing between pin centers

# Outer housing cylinder
housing_outer = cq.Workplane("YZ").circle(housing_diam/2).extrude(housing_len)

# Inner bore to receive plug
inner_bore = cq.Workplane("YZ", origin=(0,0,0)).circle(plug_diam/2).extrude(housing_len+1)

# Cut‐away block to expose plug
cut_len    = housing_len * 0.6
cut_height = housing_diam / 2
cut_box = (
    cq.Workplane("XY")
      .box(cut_len, housing_diam*1.1, cut_height)
      .translate((housing_len*0.5, 0, housing_diam/2 + cut_height/2))
)

# Housing shell with cutaway
housing_shell = housing_outer.cut(inner_bore).cut(cut_box)

# Plug cylinder
plug_start = housing_len - plug_insert
plug = (
    cq.Workplane("YZ", origin=(plug_start, 0, 0))
      .circle(plug_diam/2)
      .extrude(plug_len)
)

# Key head
head = (
    cq.Workplane("YZ", origin=(plug_start + plug_len, 0, 0))
      .circle(head_diam/2)
      .extrude(head_thick)
)

# Pins on top of plug
pins = None
pin_z0 = plug_diam/2
for i in range(pin_count):
    x = plug_start + pin_offset + i*pin_spacing
    pin = (
        cq.Workplane("XY", origin=(x, 0, pin_z0))
          .circle(pin_diam/2)
          .extrude(pin_len)
    )
    pins = pin if pins is None else pins.union(pin)

# Combine all parts
result = housing_shell.union(plug).union(head)
if pins:
    result = result.union(pins)