import cadquery as cq

# Create the base block
base = cq.Workplane("XY").box(60, 20, 10)

# Create the cylindrical cutout
cutout_cylinder = cq.Workplane("XY").workplane(offset=5).circle(15).extrude(10)

# Subtract the cylindrical cutout from the base
result = base.cut(cutout_cylinder)

# Create the slot cutout
slot_cutout = cq.Workplane("XY").workplane(offset=5).rect(10, 20).extrude(10)
result = result.cut(slot_cutout)

# Create the side cutouts
side_cutout = cq.Workplane("XZ").workplane(offset=10).circle(2.5).extrude(20)
result = result.cut(side_cutout.mirror("YZ"))

# Final result
result = result.rotate((0, 0, 0), (0, 0, 1), 90)