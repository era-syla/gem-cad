import cadquery as cq

th = 2
fl_h = 20
hem_l = 5
w = 40
L = 100

result = (
    cq.Workplane("XZ")
      .polyline([
          (0, 0),
          (w, 0),
          (w, -fl_h),
          (w - hem_l, -fl_h),
          (w - hem_l, -fl_h + th),
          (0, -fl_h + th),
      ])
      .close()
      .extrude(L)
)