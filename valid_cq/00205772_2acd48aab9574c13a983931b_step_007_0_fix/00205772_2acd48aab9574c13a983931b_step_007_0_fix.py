import cadquery as cq

# Create the vertical extrusion
vslot = cq.Workplane("XZ").rect(20, 100).extrude(200)

# Create the slot for the outer part
outer_slot = cq.Workplane("XY").circle(10).extrude(5).translate((0, 0, 55))

# Create the cutout in the middle
cutout_slot = cq.Workplane("XY").rect(10, 50).extrude(5).translate((0, 0, 75))

# Create the horizontal arms
arm = (cq.Workplane("XZ")
       .rect(70, 10)
       .extrude(5)
       .translate((0, 0, 100))
       .edges('|Z').fillet(2))

result = vslot.cut(outer_slot).cut(cutout_slot).union(arm)