import cadquery as cq

# Parameters
base_len = 200
base_wid = 60
base_h = 20
jaw_len = 20
jaw_h = 20
rail_d = 8
rail_offset = 5
rail_len = base_len - 2 * jaw_len

stationary_x = -base_len/2 + jaw_len
moving_x = 0
rails_z = base_h + rail_d/2

# Build base and jaws
result = cq.Workplane("XY").box(base_len, base_wid, base_h)
# Stationary jaw
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(stationary_x, 0, base_h/2 + jaw_h/2))
      .box(jaw_len, base_wid, jaw_h)
)
# Moving jaw
result = result.union(
    cq.Workplane("XY")
      .transformed(offset=(moving_x, 0, base_h/2 + jaw_h/2))
      .box(jaw_len, base_wid, jaw_h)
)

# Rails (guide rods)
for y in (-base_wid/2 + rail_offset + rail_d/2, base_wid/2 - rail_offset - rail_d/2):
    rod = (
        cq.Workplane("XY")
          .transformed(offset=(stationary_x, y, rails_z), rotate=(0, 90, 0))
          .circle(rail_d/2)
          .extrude(rail_len)
    )
    result = result.union(rod)

# Screw (plain cylinder)
screw_d = 10
screw_len = rail_len + 40
screw_start = stationary_x - 20
screw = (
    cq.Workplane("XY")
      .transformed(offset=(screw_start, 0, rails_z), rotate=(0, 90, 0))
      .circle(screw_d/2)
      .extrude(screw_len)
)
result = result.union(screw)

# Handle (cross-pin style)
x_end = screw_start + screw_len
handle_len = 40
handle_r = 2

# Forward half
rod_fw = (
    cq.Workplane("XZ")
      .transformed(offset=(x_end, 0, rails_z))
      .circle(handle_r)
      .extrude(handle_len/2)
)
# Backward half
rod_bw = (
    cq.Workplane("XZ")
      .transformed(offset=(x_end, 0, rails_z), rotate=(0, 180, 0))
      .circle(handle_r)
      .extrude(handle_len/2)
)
result = result.union(rod_fw).union(rod_bw)

# End knobs
knob_r = 4
sphere1 = (
    cq.Workplane("XZ")
      .transformed(offset=(x_end, handle_len/2, rails_z))
      .sphere(knob_r)
)
sphere2 = (
    cq.Workplane("XZ")
      .transformed(offset=(x_end, -handle_len/2, rails_z))
      .sphere(knob_r)
)
result = result.union(sphere1).union(sphere2)

# Disc knob on screw end
disc = (
    cq.Workplane("YZ")
      .transformed(offset=(x_end + 4, 0, rails_z))
      .circle(8)
      .extrude(4)
)
result = result.union(disc)