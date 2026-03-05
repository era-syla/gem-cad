import cadquery as cq

# Parameters
n_total = 14
n_thick = 7
n_thin = n_total - n_thick
pitch = 2.54
thick_depth = 3.5
thin_depth = 2.0
thick_height = 4.0
thin_height = 3.0
hole_dia = 1.3
pin_dia = 0.64
pin_down_length = 6.0
pin_side_length = 8.0

# Compute block dimensions
thick_len = n_thick * pitch
thin_len = n_thin * pitch
total_len = thick_len + thin_len
x_start = -total_len / 2.0
thick_cx = x_start + thick_len / 2.0
thin_cx = x_start + thick_len + thin_len / 2.0

# Build thick section
thick = (
    cq.Workplane("XY")
    .rect(thick_len, thick_depth)
    .extrude(thick_height)
    .translate((thick_cx, 0, 0))
)

# Build thin section
thin = (
    cq.Workplane("XY")
    .rect(thin_len, thin_depth)
    .extrude(thin_height)
    .translate((thin_cx, 0, 0))
)

# Combine body
result = thick.union(thin)

# Cut female holes in thick section
for k in range(n_thick):
    x = (k - (n_thick - 1) / 2.0) * pitch
    result = result.faces(">Z").workplane().center(x, 0).hole(hole_dia)

# Add downward pins
down_points = [((k - (n_total - 1) / 2.0) * pitch, 0) for k in range(n_total)]
result = result.faces("<Z").workplane().pushPoints(down_points).cylinder(pin_down_length, pin_dia)

# Add side pins on thin section
side_points = [((k - (n_total - 1) / 2.0) * pitch, 0) for k in range(n_thick, n_total)]
result = result.faces(">Y").workplane().pushPoints(side_points).cylinder(pin_side_length, pin_dia)