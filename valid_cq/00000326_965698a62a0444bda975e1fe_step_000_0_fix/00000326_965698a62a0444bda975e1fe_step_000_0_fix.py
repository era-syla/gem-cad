import cadquery as cq

# Build a hydraulic thumb/coupler assembly for an excavator
# Main frame/body
main_frame = (
    cq.Workplane("XY")
    .box(120, 40, 35)
)

# Add trapezoidal side plates
left_plate = (
    cq.Workplane("XZ")
    .center(-20, 0)
    .rect(80, 35)
    .extrude(5)
)

right_plate = (
    cq.Workplane("XZ")
    .center(-20, 0)
    .rect(80, 35)
    .extrude(5)
    .translate((0, 35, 0))
)

# Main body base - wider rectangular frame
base = (
    cq.Workplane("XY")
    .box(100, 50, 30)
)

# Add ribs/gussets on the frame
rib1 = (
    cq.Workplane("XY")
    .center(20, 0)
    .box(8, 50, 30)
)

rib2 = (
    cq.Workplane("XY")
    .center(0, 0)
    .box(8, 50, 30)
)

rib3 = (
    cq.Workplane("XY")
    .center(-20, 0)
    .box(8, 50, 30)
)

# Combine base with ribs
frame = base.union(rib1).union(rib2).union(rib3)

# Add top cylinder mount
cyl_mount = (
    cq.Workplane("XY")
    .center(0, 0)
    .box(100, 20, 10)
    .translate((0, 0, 20))
)

frame = frame.union(cyl_mount)

# Hydraulic cylinder body
hyd_cylinder = (
    cq.Workplane("YZ")
    .center(0, 25)
    .circle(8)
    .extrude(90)
    .translate((0, -10, 22))
)

# Cylinder rod
hyd_rod = (
    cq.Workplane("YZ")
    .center(0, 25)
    .circle(4)
    .extrude(110)
    .translate((-90, -10, 22))
)

# End caps for cylinder
end_cap1 = (
    cq.Workplane("YZ")
    .center(0, 25)
    .circle(12)
    .extrude(8)
    .translate((80, -10, 22))
)

end_cap2 = (
    cq.Workplane("YZ")
    .center(0, 25)
    .circle(10)
    .extrude(8)
    .translate((-10, -10, 22))
)

# Thumb jaw / bucket coupler arm
jaw_arm = (
    cq.Workplane("XZ")
    .center(-40, 0)
    .box(60, 30, 8)
    .translate((-30, -25, 0))
)

# Front hook/clevis
clevis = (
    cq.Workplane("XY")
    .center(-60, 0)
    .box(20, 30, 25)
)

# Clevis pin holes
clevis_hole = (
    cq.Workplane("XZ")
    .center(-60, 0)
    .circle(5)
    .extrude(35)
    .translate((0, -17, 0))
)

# Side mounting ears
ear_left = (
    cq.Workplane("XY")
    .center(-55, 20)
    .box(25, 8, 20)
)

ear_right = (
    cq.Workplane("XY")
    .center(-55, -20)
    .box(25, 8, 20)
)

# Pivot pin cylinders at front
pivot1 = (
    cq.Workplane("XZ")
    .center(-60, -5)
    .circle(7)
    .extrude(50)
    .translate((0, -25, 0))
)

pivot2 = (
    cq.Workplane("XZ")
    .center(-60, -5)
    .circle(4)
    .extrude(55)
    .translate((0, -27, 0))
)

# Assemble everything
result = (
    frame
    .union(hyd_cylinder)
    .union(hyd_rod)
    .union(end_cap1)
    .union(end_cap2)
    .union(clevis)
    .union(ear_left)
    .union(ear_right)
    .union(pivot1)
)

# Cut holes in clevis for pins
result = result.cut(
    cq.Workplane("XZ")
    .center(-60, -5)
    .circle(4)
    .extrude(55)
    .translate((0, -27, 0))
)

# Add rectangular cutouts to main frame for weight reduction
cutout1 = (
    cq.Workplane("XY")
    .center(20, 0)
    .box(10, 20, 40)
)

cutout2 = (
    cq.Workplane("XY")
    .center(-5, 0)
    .box(10, 20, 40)
)

cutout3 = (
    cq.Workplane("XY")
    .center(-30, 0)
    .box(10, 20, 40)
)

result = result.cut(cutout1).cut(cutout2).cut(cutout3)