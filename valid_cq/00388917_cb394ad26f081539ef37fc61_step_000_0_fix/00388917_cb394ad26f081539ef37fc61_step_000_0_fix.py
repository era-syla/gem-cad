import cadquery as cq

# Parameters
main_outer = 40.0
wall = 3.0
main_inner = main_outer - 2 * wall
tube_len = 120.0

flange_outer = 55.0
flange_thickness = 5.0
flange_offset = 15.0  # distance from right end

end_outer = 30.0
end_len = 10.0

stub_outer = 8.0
stub_len = 16.0
stub_z = tube_len / 2

# Main hollow tube
tube = (
    cq.Workplane("XY")
    .circle(main_outer/2)
    .circle(main_inner/2)
    .extrude(tube_len)
)

# Flange on the tube
flange = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, tube_len - flange_offset))
    .circle(flange_outer/2)
    .circle(main_outer/2)
    .extrude(flange_thickness)
)

# Right end extension (hollow)
end_piece = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, tube_len))
    .circle(end_outer/2)
    .circle(main_inner/2)
    .extrude(end_len)
)

# Top stub (radial)
stub1 = (
    cq.Workplane("XZ")
    .transformed(offset=(0, main_outer/2, stub_z))
    .circle(stub_outer/2)
    .extrude(stub_len)
)

# Bottom stub (radial)
stub2 = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -main_outer/2, stub_z))
    .circle(stub_outer/2)
    .extrude(stub_len)
)

# Combine all parts
result = tube.union(flange).union(end_piece).union(stub1).union(stub2)