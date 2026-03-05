import cadquery as cq

# Parameters
cyl_d = 8
cyl_h = 20
hex_flat = 14
hex_h = 2
r_large_d = 12
r_large_h = 1
r_med_d = 10
r_med_h = 0.5
r_small_d = 8
r_small_h = 0.5
dome_d = 10
pin_length = 5
pin_len_rad = 3
pin_width = 2

# Build the main body: cylinder, hex, rings
body = (
    cq.Workplane("XY")
      .circle(cyl_d/2).extrude(cyl_h)
      .faces(">Z").workplane()
      .polygon(6, hex_flat).extrude(hex_h)
      .faces(">Z").workplane()
      .circle(r_large_d/2).extrude(r_large_h)
      .faces(">Z").workplane()
      .circle(r_med_d/2).extrude(r_med_h)
      .faces(">Z").workplane()
      .circle(r_small_d/2).extrude(r_small_h)
)

# Add hemisphere dome on top
z_base = cyl_h + hex_h + r_large_h + r_med_h + r_small_h
sphere = cq.Workplane("XY").sphere(dome_d).translate((0, 0, z_base + dome_d/2))
body = body.union(sphere)

# Create two bottom pins
pin1 = (
    cq.Workplane("XY")
      .rect(pin_len_rad, pin_width)
      .extrude(-pin_length)
      .translate((cyl_d/2 + pin_len_rad/2, 0, 0))
)
pin2 = (
    cq.Workplane("XY")
      .rect(pin_len_rad, pin_width)
      .extrude(-pin_length)
      .translate((-(cyl_d/2 + pin_len_rad/2), 0, 0))
)

# Final result
result = body.union(pin1).union(pin2)