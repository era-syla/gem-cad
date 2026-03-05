import cadquery as cq

# Build a fuel filter / inline filter shape
# The part consists of:
# - A central cylindrical body (main filter housing)
# - Two end caps (smaller cylinders) on each end
# - Two inlet/outlet stubs (small cylinders) extending from each end
# - A groove/neck between the main body and end caps

# Dimensions (approximate, based on image proportions)
main_body_r = 18
main_body_len = 50

end_cap_r = 12
end_cap_len = 12

neck_r = 8
neck_len = 6

stub_r = 4
stub_len = 20

# Left stub has a hex-like or squared shape - approximate with small cylinder
# Right stub is round cylinder

# Build by revolving a profile around the X axis
# Profile defined in the XY plane, revolved around X

# Use loft/union approach to combine cylinders

result = (
    cq.Workplane("YZ")
    .circle(main_body_r)
    .extrude(main_body_len)
)

# Center the main body at origin along X
# main body goes from x=0 to x=main_body_len, shift to center
result = (
    cq.Workplane("YZ")
    .circle(main_body_r)
    .extrude(main_body_len)
)

# Rebuild centered approach using XY workplane and positioning
total_len = stub_len + neck_len + end_cap_len + main_body_len + end_cap_len + neck_len + stub_len
cx = total_len / 2.0

def make_cylinder_x(radius, length, x_start):
    """Create a cylinder along X axis starting at x_start"""
    return (
        cq.Workplane("YZ")
        .transformed(offset=(0, 0, x_start))
        .circle(radius)
        .extrude(length)
    )

# Build all segments
x = 0

# Left stub
seg1 = make_cylinder_x(stub_r, stub_len, x)
x += stub_len

# Left neck
seg2 = make_cylinder_x(neck_r, neck_len, x)
x += neck_len

# Left end cap
seg3 = make_cylinder_x(end_cap_r, end_cap_len, x)
x += end_cap_len

# Main body
seg4 = make_cylinder_x(main_body_r, main_body_len, x)
x += main_body_len

# Right end cap
seg5 = make_cylinder_x(end_cap_r, end_cap_len, x)
x += end_cap_len

# Right neck
seg6 = make_cylinder_x(neck_r, neck_len, x)
x += neck_len

# Right stub
seg7 = make_cylinder_x(stub_r, stub_len, x)

# Union all segments
result = (
    seg1
    .union(seg2)
    .union(seg3)
    .union(seg4)
    .union(seg5)
    .union(seg6)
    .union(seg7)
)

# Add a groove ring on the main body ends (decorative groove - slight indent)
groove_r = main_body_r - 2
groove_w = 4

groove_x1 = stub_len + neck_len + end_cap_len
groove_x2 = stub_len + neck_len + end_cap_len + main_body_len - groove_w

groove1 = make_cylinder_x(groove_r, groove_w, groove_x1)
groove2 = make_cylinder_x(groove_r, groove_w, groove_x2)

# Cut grooves from result
result = result.cut(
    cq.Workplane("YZ")
    .transformed(offset=(0, 0, groove_x1))
    .circle(main_body_r + 1)
    .circle(groove_r)
    .extrude(groove_w)
)

result = result.cut(
    cq.Workplane("YZ")
    .transformed(offset=(0, 0, groove_x2))
    .circle(main_body_r + 1)
    .circle(groove_r)
    .extrude(groove_w)
)