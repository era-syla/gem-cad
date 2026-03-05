import cadquery as cq

thickness = 3
back_h = 40
flange_len = 20
width = 80
hole_d = 4
rect_margin = 2
hole_offset = flange_len/2 - 5

result = (
    cq.Workplane("XZ")
      .polyline([
          (0, 0),
          (0, back_h),
          (flange_len, back_h),
          (flange_len, back_h - thickness),
          (thickness, back_h - thickness),
          (thickness, 0)
      ])
      .close()
      .extrude(width)
      # cut rectangular window through vertical leg
      .faces(">Y")
      .workplane()
      .rect(flange_len - 2*rect_margin, back_h - 2*rect_margin)
      .cutBlind(-thickness*2)
      # cut two mounting holes in the top flange
      .faces(">Z")
      .workplane()
      .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
      .circle(hole_d/2)
      .cutBlind(-thickness*2)
)