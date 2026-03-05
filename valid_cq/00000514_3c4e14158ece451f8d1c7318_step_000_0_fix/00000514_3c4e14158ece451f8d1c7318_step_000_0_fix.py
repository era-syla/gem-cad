import cadquery as cq

# CNC Router / Milling Machine Frame
# Building a simplified but recognizable CNC router frame

def make_extrusion_profile(w, h):
    """Create a rectangular extrusion profile"""
    return (cq.Workplane("XY")
            .rect(w, h)
            .extrude(1))

# Main base frame
base_length = 200
base_width = 140
base_height = 8
rail_h = 12
rail_w = 12

# Base frame - two long rails (X direction)
left_rail = (cq.Workplane("XY")
             .box(base_length, rail_w, rail_h)
             .translate((0, -base_width/2 + rail_w/2, rail_h/2)))

right_rail = (cq.Workplane("XY")
              .box(base_length, rail_w, rail_h)
              .translate((0, base_width/2 - rail_w/2, rail_h/2)))

# Cross rails (Y direction)
front_cross = (cq.Workplane("XY")
               .box(rail_w, base_width, rail_h)
               .translate((-base_length/2 + rail_w/2, 0, rail_h/2)))

rear_cross = (cq.Workplane("XY")
              .box(rail_w, base_width, rail_h)
              .translate((base_length/2 - rail_w/2, 0, rail_h/2)))

# Middle cross supports
mid_cross1 = (cq.Workplane("XY")
              .box(rail_w, base_width, rail_h)
              .translate((-30, 0, rail_h/2)))

mid_cross2 = (cq.Workplane("XY")
              .box(rail_w, base_width, rail_h)
              .translate((30, 0, rail_h/2)))

# Combine base frame
base = (left_rail.val().fuse(right_rail.val())
        .fuse(front_cross.val())
        .fuse(rear_cross.val())
        .fuse(mid_cross1.val())
        .fuse(mid_cross2.val()))

base_wp = cq.Workplane("XY").add(base)

# Gantry uprights - two vertical columns
upright_h = 80
upright_w = 12
upright_d = 12

left_upright = (cq.Workplane("XY")
                .box(upright_d, upright_w, upright_h)
                .translate((base_length/2 - upright_d/2 - 10, -base_width/2 + upright_w/2 + 5, rail_h + upright_h/2)))

right_upright = (cq.Workplane("XY")
                 .box(upright_d, upright_w, upright_h)
                 .translate((base_length/2 - upright_d/2 - 10, base_width/2 - upright_w/2 - 5, rail_h + upright_h/2)))

# Gantry top beam (X axis rail)
gantry_beam = (cq.Workplane("XY")
               .box(upright_d, base_width - 10, upright_w)
               .translate((base_length/2 - upright_d/2 - 10, 0, rail_h + upright_h - upright_w/2)))

# Diagonal braces
brace_left = (cq.Workplane("XY")
              .box(upright_d * 0.8, upright_w * 0.8, upright_h * 0.6)
              .translate((base_length/2 - upright_d/2 - 10 - 15, -base_width/2 + upright_w/2 + 5, rail_h + upright_h * 0.3)))

brace_right = (cq.Workplane("XY")
               .box(upright_d * 0.8, upright_w * 0.8, upright_h * 0.6)
               .translate((base_length/2 - upright_d/2 - 10 - 15, base_width/2 - upright_w/2 - 5, rail_h + upright_h * 0.3)))

# Z-axis carriage plate
carriage = (cq.Workplane("XY")
            .box(upright_d + 6, 35, 45)
            .translate((base_length/2 - upright_d/2 - 10, 0, rail_h + upright_h * 0.55)))

# Spindle motor (cylinder)
spindle = (cq.Workplane("XY")
           .cylinder(35, 8)
           .translate((base_length/2 - upright_d/2 - 10, 0, rail_h + upright_h * 0.45)))

# Y-axis rails on base (two long rails running front to back)
y_rail1 = (cq.Workplane("XY")
           .box(base_length - 30, rail_w * 0.8, rail_h * 0.7)
           .translate((0, -base_width/4, rail_h + rail_h * 0.35)))

y_rail2 = (cq.Workplane("XY")
           .box(base_length - 30, rail_w * 0.8, rail_h * 0.7)
           .translate((0, base_width/4, rail_h + rail_h * 0.35)))

# Fuse all parts
result_shape = (base
                .fuse(left_upright.val())
                .fuse(right_upright.val())
                .fuse(gantry_beam.val())
                .fuse(brace_left.val())
                .fuse(brace_right.val())
                .fuse(carriage.val())
                .fuse(spindle.val())
                .fuse(y_rail1.val())
                .fuse(y_rail2.val()))

result = cq.Workplane("XY").add(result_shape)