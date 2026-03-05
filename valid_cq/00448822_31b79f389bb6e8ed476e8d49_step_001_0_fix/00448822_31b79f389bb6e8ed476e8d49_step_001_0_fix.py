import cadquery as cq

# Parameters
R_base = 25.0        # Base outer radius
t_base = 3.0         # Base thickness
slope_h = 5.0        # Height of the sloped transition
R_cyl = 5.0          # Outer radius of the upright cylinder
h_cyl = 60.0         # Height of the upright cylinder
wall_thick = 2.0     # Wall thickness of the bore

R_i = R_cyl - wall_thick  # Inner radius of the bore

# Build the profile in the X-Z plane and revolve around Z axis
result = (
    cq.Workplane("XZ")
      .polyline([
          (0.0, 0.0),                       # p1: bottom center
          (R_base, 0.0),                    # p2: base outer edge
          (R_base, t_base),                 # p3: top of base
          (R_cyl, t_base + slope_h),        # p4: start of cylinder
          (R_cyl, t_base + slope_h + h_cyl),# p5: top of cylinder
          (R_i, t_base + slope_h + h_cyl),  # p6: inner bore top
          (R_i, t_base + slope_h),          # p7: inner bore bottom
          (0.0, t_base + slope_h)           # p8: center at bottom of bore
      ])
      .close()
      .revolve(360, (0, 0, 0), (0, 0, 1))
)