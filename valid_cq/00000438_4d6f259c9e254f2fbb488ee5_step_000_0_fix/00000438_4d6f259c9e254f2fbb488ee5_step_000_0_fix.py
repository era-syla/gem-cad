import cadquery as cq

# Build a hydraulic actuator / winch assembly approximation
# Main frame base
frame = (
    cq.Workplane("XY")
    .box(120, 40, 30)
)

# Frame side walls with cutouts
left_wall = (
    cq.Workplane("XY")
    .center(-50, 0)
    .box(20, 40, 50)
)

right_wall = (
    cq.Workplane("XY")
    .center(50, 0)
    .box(20, 40, 50)
)

# Combine frame
frame = frame.union(left_wall).union(right_wall)

# Add mounting brackets on the sides
bracket_left = (
    cq.Workplane("YZ")
    .center(0, 10)
    .workplane(offset=-60)
    .rect(35, 40)
    .extrude(15)
)

bracket_right = (
    cq.Workplane("YZ")
    .center(0, 10)
    .workplane(offset=45)
    .rect(35, 40)
    .extrude(15)
)

frame = frame.union(bracket_left).union(bracket_right)

# Main hydraulic cylinder body
cylinder_body = (
    cq.Workplane("XZ")
    .center(20, 35)
    .circle(12)
    .extrude(90)
)

# Cylinder rod
cylinder_rod = (
    cq.Workplane("XZ")
    .center(20, 35)
    .circle(6)
    .workplane(offset=90)
    .circle(6)
    .loft()
)

cylinder_rod2 = (
    cq.Workplane("YZ")
    .center(0, 35)
    .workplane(offset=110)
    .circle(6)
    .extrude(30)
)

# Cylinder end caps
end_cap1 = (
    cq.Workplane("XZ")
    .center(20, 35)
    .workplane(offset=0)
    .circle(14)
    .extrude(8)
)

end_cap2 = (
    cq.Workplane("XZ")
    .center(20, 35)
    .workplane(offset=90)
    .circle(14)
    .extrude(8)
)

# Combine cylinder
cylinder = cylinder_body.union(end_cap1).union(end_cap2)

# Support ribs on frame
rib1 = (
    cq.Workplane("XY")
    .center(-20, 0)
    .box(8, 40, 50)
)

rib2 = (
    cq.Workplane("XY")
    .center(10, 0)
    .box(8, 40, 50)
)

rib3 = (
    cq.Workplane("XY")
    .center(35, 0)
    .box(8, 40, 50)
)

frame = frame.union(rib1).union(rib2).union(rib3)

# Front hook/coupler assembly
hook_base = (
    cq.Workplane("XY")
    .center(-65, 0)
    .box(25, 50, 45)
)

# Hook pin holes
hook_base = (
    hook_base
    .faces("<X")
    .workplane()
    .center(0, 5)
    .circle(8)
    .cutThruAll()
)

hook_base = (
    hook_base
    .faces("<X")
    .workplane()
    .center(0, -10)
    .circle(5)
    .cutThruAll()
)

# Round pin on hook
hook_pin = (
    cq.Workplane("XY")
    .center(-65, 25)
    .circle(8)
    .extrude(45)
    .rotate((0, 0, 0), (1, 0, 0), 90)
)

# Combine all parts
result = (
    frame
    .union(cylinder)
    .union(cylinder_rod2)
    .union(hook_base)
)

# Add top cylinder mount bracket
mount_top = (
    cq.Workplane("XY")
    .center(20, 0)
    .box(95, 10, 60)
)

# Drill frame cutouts for lightness
frame_cut1 = (
    cq.Workplane("XZ")
    .center(-35, 20)
    .rect(18, 20)
    .extrude(50)
)

frame_cut2 = (
    cq.Workplane("XZ")
    .center(22, 20)
    .rect(18, 20)
    .extrude(50)
)

result = result.cut(frame_cut1).cut(frame_cut2)

# Rear drum/winch cylinder
drum = (
    cq.Workplane("YZ")
    .center(0, 35)
    .workplane(offset=55)
    .circle(15)
    .extrude(30)
)

result = result.union(drum)

# Final bounding cleanup - ensure valid solid
result = result.union(
    cq.Workplane("XY")
    .center(0, 0)
    .box(1, 1, 1)
    .translate((200, 200, 200))
).cut(
    cq.Workplane("XY")
    .center(200, 200)
    .box(5, 5, 5)
)