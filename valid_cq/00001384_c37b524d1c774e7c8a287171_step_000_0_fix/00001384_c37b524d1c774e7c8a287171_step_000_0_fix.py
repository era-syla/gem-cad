import cadquery as cq

# Parameters
br_w = 30    # bracket width in Y
br_h = 80    # bracket height in Z
br_th = 5    # bracket thickness in X

plate_len = 60
plate_w = br_w
plate_th = 5

slide_len = 70
slide_w = 20
slide_th = 4
gap = 1      # gap between plates

pin_r = 2
pin_extra = 4  # extra length beyond bracket width

# Bracket with cutouts
bracket = (
    cq.Workplane("YZ")
      .rect(br_w, br_h)
      .extrude(br_th)
      # bottom rectangular cutout
      .faces(">X").workplane()
      .center(0, -20)
      .rect(18, 40)
      .cutThruAll()
      # top circular cutout
      .faces(">X").workplane()
      .center(0, 20)
      .circle(10)
      .cutThruAll()
      # flatten bottom of that circle to make D-shape
      .faces(">X").workplane()
      .center(0, 10)
      .rect(20, 10)
      .cutThruAll()
)

# Top fixed plate
topPlate = (
    cq.Workplane("XY")
      .box(plate_len, plate_w, plate_th)
      .translate((br_th + plate_len/2, 0, br_h/2 + plate_th/2))
)

# Sliding plate
# Center Z such that it sits below top plate with a gap
slide_center_z = br_h/2 - (plate_th + gap + slide_th)/2
slidePlate = (
    cq.Workplane("XY")
      .box(slide_len, slide_w, slide_th)
      .translate((br_th + slide_len/2, 0, slide_center_z))
)

# Hinge pin
pin = (
    cq.Workplane("XZ")
      .workplane(origin=(br_th, 0, slide_center_z))
      .circle(pin_r)
      .extrude(br_w + pin_extra)
)

result = bracket.union(topPlate).union(slidePlate).union(pin)